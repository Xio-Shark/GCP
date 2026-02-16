"""Cross-platform DPI utilities."""

from .system_detect import is_windows, is_macos
from .logging import log


def set_dpi_awareness():
    """设置 DPI 感知（跨平台）"""
    if is_windows():
        try:
            from .win32.dpi import set_dpi_awareness as win_set_dpi
            win_set_dpi()
        except ImportError as e:
            log(f"Failed to import Windows DPI utilities: {e}")
    elif is_macos():
        try:
            from .macos.dpi import set_dpi_awareness as mac_set_dpi
            mac_set_dpi()
        except ImportError as e:
            log(f"Failed to import macOS DPI utilities: {e}")
    else:
        log("DPI awareness not supported on this platform")


def get_dpi_scale():
    """
    获取当前屏幕的 DPI 缩放比例（跨平台）
    
    Returns:
        float: 缩放比例 (例如 1.0, 1.25, 1.5, 2.0)
    """
    if is_windows():
        try:
            from .win32.dpi import get_dpi_scale as win_get_dpi
            return win_get_dpi()
        except ImportError as e:
            log(f"Failed to import Windows DPI utilities: {e}")
            return 1.0
    elif is_macos():
        try:
            from .macos.dpi import get_dpi_scale as mac_get_dpi
            return mac_get_dpi()
        except ImportError as e:
            log(f"Failed to import macOS DPI utilities: {e}")
            return 1.0
    else:
        log("DPI scale detection not supported on this platform")
        return 1.0
