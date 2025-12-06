from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:id>/', views.news_detail, name='news_detail'),
    path('create/', views.news_create, name='news_create'),
    path('<int:id>/update/', views.news_update, name='news_update'),
    path('<int:id>/delete/', views.news_delete, name='news_delete'),

    path('<int:id>/comment/create/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    path('<int:id>/reaction/', views.news_reaction_create, name='news_reaction_create'),
    path('comment/<int:comment_id>/reaction/', views.comment_reaction_create, name='comment_reaction_create'),
]