from django.urls import path
from .views import PostList, SearchList, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, del_subscribe, \
    add_subscribe

urlpatterns = [
    path('', PostList.as_view()),
    path('search/', SearchList.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/add_subscribe/', add_subscribe, name='add_subscribe'),
    path('<int:pk>/del_subscribe/', del_subscribe, name='del_subscribe'),
]
