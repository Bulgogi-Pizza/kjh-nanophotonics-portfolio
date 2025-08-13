import reflex as rx

from .admin import publication_admin, media_admin, cv_admin
from .pages import index, publications, media, cv

from .state import state

# 앱 객체 생성
app = rx.App()