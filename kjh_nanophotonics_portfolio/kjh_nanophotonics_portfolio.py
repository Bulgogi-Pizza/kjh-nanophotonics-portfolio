import reflex as rx

from .admin import publication_admin, media_admin, cv_admin
from .pages import index, publications, media, cv

from .state import base_state, cv_state, media_state, publication_state

# 앱 객체 생성
app = rx.App()