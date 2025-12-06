from django import forms
from dal import autocomplete
from .models import News, NewsBlock, Comment, Reaction


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'image', 'published_at', 'is_published']

class NewsBlockForm(forms.ModelForm):
    class Meta:
        model = NewsBlock
        fields = ['news', 'title', 'content', 'image', 'order', 'background_color']
        widgets = {
            'news': autocomplete.ModelSelect2(
                url='news:news_autocomplete')
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'news': autocomplete.ModelSelect2(
                url='news:news_autocomplete'),
            'user': autocomplete.ModelSelect2(
                url='news:user_autocomplete'),
            'parent': autocomplete.ModelSelect2(
                url='news:comment_autocomplete')
        }


class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['user', 'reaction_type', 'news', 'comment']
        widgets = {
            'user': autocomplete.ModelSelect2(
                url='news:user_autocomplete'),
            'news': autocomplete.ModelSelect2(
                url='news:news_autocomplete'),
            'comment': autocomplete.ModelSelect2(
                url='news:comment_autocomplete'),
        }