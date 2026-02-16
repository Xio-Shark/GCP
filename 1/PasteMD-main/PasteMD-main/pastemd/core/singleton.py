"""Single instance check to prevent multiple application instances."""

import os
import sys
from abc import ABC, abstractmethod

from .state import app_state
from ..utils.logging import log
from ..utils.system_detect import is_windows, is_macos


class SingleInstanceChecker(ABC):
    """单实例检查器基类"""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
    
    @abstractmethod
    def is_already_running(self) -> bool:
        """检查是否已有实例在运行"""
        pass
    
    @abstractmethod
    def acquire_lock(self) -> bool:
        """获取应用锁"""
        pass
    
    @abstractmethod
    def release_lock(self) -> None:
        """释放应用锁"""
        pass


class WindowsSingleInstanceChecker(SingleInstanceChecker):
    """Windows 平台单实例检查器 - 使用 Windows Mutex"""
    
    def __init__(self, app_name: str = "Global\\PasteMD-Mutex"):
        super().__init__(app_name)
        self.mutex_handle = None
        
        # Windows API
        import ctypes
        self.kernel32 = ctypes.windll.kernel32
        self.ERROR_ALREADY_EXISTS = 183
    
    def is_already_running(self) -> bool:
        """检查是否已有实例在运行（使用 Windows Mutex）"""
        try:
            # 创建或打开一个命名互斥体
            self.mutex_handle = self.kernel32.CreateMutexW(
                None,  # 默认安全属性
                True,  # 初始拥有者
                self.app_name  # 互斥体名称
            )
            
            if self.mutex_handle:
                last_error = self.kernel32.GetLastError()
                if last_error == self.ERROR_ALREADY_EXISTS:
                    log("Mutex already exists, another instance is running")
                    return True
                else:
                    log("Mutex created successfully")
                    return False
            else:
                log("Failed to create mutex")
                return False
                
        except Exception as e:
            log(f"Error checking single instance: {e}")
            return False
    
    def acquire_lock(self) -> bool:
        """获取应用锁"""
        if self.mutex_handle:
            log("Mutex lock acquired")
            return True
        return False
    
    def release_lock(self) -> None:
        """释放应用锁"""
        try:
            if self.mutex_handle:
                self.kernel32.ReleaseMutex(self.mutex_handle)
                self.kernel32.CloseHandle(self.mutex_handle)
                self.mutex_handle = None
                log("Mutex released")
        except Exception as e:
            log(f"Error releasing mutex: {e}")


class MacOSSingleInstanceChecker(SingleInstanceChecker):
    """macOS 平台单实例检查器 - 使用文件锁"""
    
    def __init__(self, app_name: str = "PasteMD"):
        super().__init__(app_name)
        self.lock_file = None
        self.lock_fd = None
        
        # 使用临时目录创建锁文件
        import tempfile
        self.lock_path = os.path.join(tempfile.gettempdir(), f"{app_name}.lock")
    
    def is_already_running(self) -> bool:
        """检查是否已有实例在运行（使用文件锁）"""
        try:
            import fcntl
            
            # 打开或创建锁文件
            self.lock_fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR)
            
            try:
                # 尝试获取非阻塞的排他锁
                fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                
                # 写入当前进程 ID
                os.ftruncate(self.lock_fd, 0)
                os.write(self.lock_fd, str(os.getpid()).encode())
                
                log(f"Lock file created: {self.lock_path}")
                return False
                
            except BlockingIOError:
                # 无法获取锁，说明已有实例在运行
                log(f"Lock file already locked, another instance is running")
                os.close(self.lock_fd)
                self.lock_fd = None
                return True
                
        except Exception as e:
            log(f"Error checking single instance: {e}")
            if self.lock_fd is not None:
                try:
                    os.close(self.lock_fd)
                except Exception:
                    pass
                self.lock_fd = None
            return False
    
    def acquire_lock(self) -> bool:
        """获取应用锁"""
        if self.lock_fd is not None:
            log("File lock acquired")
            return True
        return False
    
    def release_lock(self) -> None:
        """释放应用锁"""
        try:
            if self.lock_fd is not None:
                import fcntl
                fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
                os.close(self.lock_fd)
                self.lock_fd = None
                
                # 尝试删除锁文件
                try:
                    if os.path.exists(self.lock_path):
                        os.remove(self.lock_path)
                except Exception:
                    pass
                
                log("File lock released")
        except Exception as e:
            log(f"Error releasing file lock: {e}")


def check_single_instance() -> bool:
    """
    检查并确保应用只有一个实例运行
    
    Returns:
        bool: 如果这是第一个实例返回 True，否则返回 False
    """
    # 根据操作系统选择合适的单实例检查器
    if is_windows():
        checker = WindowsSingleInstanceChecker()
    elif is_macos():
        checker = MacOSSingleInstanceChecker()
    else:
        # Linux 等其他平台也使用文件锁
        checker = MacOSSingleInstanceChecker()
    
    # 检查是否已有实例在运行
    if checker.is_already_running():
        log("Another instance of the application is already running")
        return False
    
    # 尝试获取锁
    if not checker.acquire_lock():
        log("Failed to acquire application lock")
        return False
    
    # 保存检查器实例以便后续释放锁
    app_state.instance_checker = checker
    
    return True
