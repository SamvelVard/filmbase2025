from django.contrib import admin
from .models import News, NewsBlock, Comment, Reaction
from .forms import NewsBlockForm


admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Reaction)

@admin.register(NewsBlock)
class NewsBlockAdmin(admin.ModelAdmin):
    form = NewsBlockForm
    ordering = ['-created_at']