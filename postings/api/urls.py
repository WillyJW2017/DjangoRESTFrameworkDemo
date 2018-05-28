from django.urls import path, re_path
from .views import BlogPostRudView, BlogPostAPIView

app_name = 'api'

urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post-rud'),
    re_path(r'^$', BlogPostAPIView.as_view(), name='post-listcreate'),
]
