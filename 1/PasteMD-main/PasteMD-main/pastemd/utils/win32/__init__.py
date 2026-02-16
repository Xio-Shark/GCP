"""Windows platform utilities."""

try:
    from .window import cleanup_background_wps_processes
    from .hotkey_checker import HotkeyChecker
    from .dpi import set_dpi_awareness, get_dpi_scale

    __all__ = ['cleanup_background_wps_processes', 'HotkeyChecker', 'set_dpi_awareness', 'get_dpi_scale']
except ImportError:
    # 如果在非 Windows 系统上导入，提供一个占位符
    __all__ = []