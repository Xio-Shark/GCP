"""macOS DPI awareness utilities."""

from AppKit import NSScreen
from ..logging import log


def set_dpi_awareness():
    """
    macOS 的 DPI 感知设置。
    macOS 自动处理 Retina 显示，因此这个函数主要是为了保持接口一致性。
    """
    # macOS 自动处理 Retina 显示，无需手动设置
    log("macOS handles DPI automatically (Retina support)")


def get_dpi_scale():
    """
    获取当前屏幕的缩放比例。
    
    Returns:
        float: 缩放比例 (例如 1.0 表示标准显示, 2.0 表示 Retina 显示)
    """
    try:
        # 获取主屏幕
        main_screen = NSScreen.mainScreen()
        if main_screen:
            # backingScaleFactor 返回 Retina 缩放因子
            scale = main_screen.backingScaleFactor()
            return float(scale)
        return 1.0
    except Exception as e:
        log(f"Failed to get DPI scale: {e}")
        return 1.0
