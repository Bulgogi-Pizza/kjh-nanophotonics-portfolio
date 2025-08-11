from __future__ import annotations

import os
from typing import Any

"""
테스트 환경에서 reflex 임포트 충돌을 피하기 위한 얇은 션트(shim).
- 환경변수 RX_SHIM_FORCE_STUB="1" 이면 강제로 스텁 사용
"""

rx: Any  # 한 번만 선언

try:
    if os.getenv("RX_SHIM_FORCE_STUB") == "1":
        raise ImportError("force stub")
    import reflex as _rx  # pragma: no cover
    rx = _rx # pragma: no cover
except Exception:
    class _State:
        """Reflex가 없을 때 사용할 최소 베이스 클래스."""
        pass

    def _var(func):
        """@rx.var 대체: 클래스 내에서 property처럼 동작하게."""
        return property(func)

    class _Rx:
        State = _State
        var = staticmethod(_var)

    rx = _Rx()