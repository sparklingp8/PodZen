from django.urls import path
from .views import home_view, show_link_view

urlpatterns = [
    path('', home_view, name='home'),
    path('show-link/<path:link>/', show_link_view, name='show_link'),
]
