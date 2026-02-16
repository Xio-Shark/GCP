"""macOS platform utilities."""

try:
    from .hotkey_checker import HotkeyChecker
    from .dpi import set_dpi_awareness, get_dpi_scale
    __all__ = ['HotkeyChecker', 'set_dpi_awareness', 'get_dpi_scale']
except ImportError:
    # 如果在非 macOS 系统上导入，提供一个占位符
    __all__ = []
