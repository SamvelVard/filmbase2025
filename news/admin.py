from django.contrib import admin
from .models import News, NewsBlock, Comment, Reaction

admin.site.register(News)
admin.site.register(NewsBlock)
admin.site.register(Comment)
admin.site.register(Reaction)
