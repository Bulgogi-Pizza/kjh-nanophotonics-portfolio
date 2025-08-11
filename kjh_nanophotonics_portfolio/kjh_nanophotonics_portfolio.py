import reflex as rx

from .admin import publication_admin  # noqa: F401

# 다른 파일에 정의된 페이지들을 Reflex가 인식할 수 있도록 임포트합니다.
from .pages import index, publications  # noqa: F401

# State도 명시적으로 임포트해주는 것이 좋습니다.
from .state import state  # noqa: F401

# 앱 객체 생성
app = rx.App()