from .publication_state import PublicationState
from .media_state import MediaState
from .cv_state import CVState

class State(PublicationState, MediaState, CVState):
    """
    앱 전체의 상태를 통합 관리하는 메인 State.
    기능별 State를 모두 상속받습니다.
    """
    pass