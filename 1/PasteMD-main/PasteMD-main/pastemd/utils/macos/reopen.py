"""macOS "reopen app" event handler.

On macOS, launching an already-running .app from Finder/Launchpad often does NOT
start a second process. Instead, the system sends a "reopen" AppleEvent to the
existing process. For menu-bar style apps (Dock icon hidden), this typically
results in "nothing happens" unless we handle the event explicitly.
"""

from __future__ import annotations

import sys
from typing import Callable, Optional

from Foundation import NSObject
import objc

from ..logging import log
from ...core.state import app_state


def install_reopen_handler(on_reopen: Callable[[], None]) -> bool:
    """
    Install a handler for the "reopen application" AppleEvent (macOS only).

    Returns:
        True if installed, False otherwise.
    """
    if sys.platform != "darwin":
        return False

    try:
        from Foundation import NSAppleEventManager
    except Exception as exc:  # pragma: no cover
        log(f"Failed to import AppleEvent APIs: {exc}")
        return False

    def _fourcc(code: str) -> int:
        # AppleEvents use 4-char OSType codes stored as a big-endian 32-bit int.
        # Avoid relying on the deprecated/partial `Carbon` python module.
        raw = code.encode("ascii", errors="strict")
        if len(raw) != 4:
            raise ValueError("fourcc must be exactly 4 ASCII chars")
        return int.from_bytes(raw, byteorder="big", signed=False)

    kCoreEventClass = _fourcc("aevt")
    kAEReopenApplication = _fourcc("rapp")

    class _ReopenHandler(NSObject):
        def initWithCallback_(self, callback):  # noqa: N802 (ObjC-style)
            self = objc.super(_ReopenHandler, self).init()
            if self is None:
                return None
            self._callback = callback
            return self

        def handleReopen_withReplyEvent_(self, event, replyEvent):  # noqa: N802
            try:
                if callable(getattr(self, "_callback", None)):
                    self._callback()
            except Exception as exc:
                log(f"Reopen handler error: {exc}")

    try:
        manager = NSAppleEventManager.sharedAppleEventManager()
        handler: Optional[NSObject] = _ReopenHandler.alloc().initWithCallback_(on_reopen)
        if handler is None:
            return False

        # Keep a strong reference to avoid GC.
        app_state.macos_reopen_handler = handler
        manager.setEventHandler_andSelector_forEventClass_andEventID_(
            handler,
            "handleReopen:withReplyEvent:",
            kCoreEventClass,
            kAEReopenApplication,
        )
        return True
    except Exception as exc:
        log(f"Failed to install reopen handler: {exc}")
        return False
