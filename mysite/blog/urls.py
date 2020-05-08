from django.conf.urls import url
from django.urls import path
from . import views




urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    path('post/create/', views.PostCreate.as_view(), name='post_create_url'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.PostDelete.as_view(), name='post_delete'),
    path('tags/', views.tags_list, name='tags_list_url'),
    path('tag/create', views.TagCreate.as_view(), name='tag_create_url'),
    path('tag/<int:pk>', views.TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<int:pk>/edit/', views.TagEdit.as_view(), name='tag_edit_url'),
    path('tag/<int:pk>/delete/', views.TagDelete.as_view(), name='tag_delete_url'),
]