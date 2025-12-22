from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('create/', views.news_create, name='news_create'),

    path('<int:id>/update/', views.news_update, name='news_update'),
    path('<int:id>/delete/', views.news_delete, name='news_delete'),

    path('block/<int:block_id>/update/', views.news_block_update, name='news_block_update'),
    path('block/<int:block_id>/delete/', views.news_block_delete, name='news_block_delete'),
    path('block/<int:block_id>/create/', views.news_block_create, name='news_block_create'),

    # ВАЖНО: пути для комментариев ДОЛЬШЕ и должны идти ПЕРЕД более короткими
    path('comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('comment/<int:comment_id>/reaction/', views.comment_reaction_create, name='comment_reaction_create'),

    path('<int:news_id>/block/create/', views.news_block_create, name='news_block_create'),
    # ТОЛЬКО ПОСЛЕ этого пути для новостей
    path('<int:id>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:id>/reaction/', views.news_reaction_create, name='news_reaction_create'),

    # САМЫЙ ПОСЛЕДНИЙ - общий путь
    path('<int:id>/', views.news_detail, name='news_detail'),
]