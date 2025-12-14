from dal import autocomplete
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import News, NewsBlock, Comment, Reaction
from .forms import NewsForm, NewsBlockForm, CommentForm, ReactionForm
from .helpers import paginate
from django.contrib import messages


def check_admin(user):
    return user.is_superuser

def news_list(request):
    news = News.objects.filter(is_published=True)
    query = request.GET.get('query', '')
    if query:
        news = news.filter(title__icontains=query)
    news = news.order_by('-published_at')
    news = paginate(request, news)
    return render(request, 'news/news/list.html', {'news': news,
                                                    'query': query})


def news_detail(request, id):
    if request.user.is_superuser:
        news = get_object_or_404(News, id=id)
    else:
        news = get_object_or_404(News, id=id, is_published=True)
    news_blocks = NewsBlock.objects.filter(news=news).order_by('order')
    comments = Comment.objects.filter(news=news, is_published=True
    ).order_by('-published_at')
    comments_form = CommentForm()
    return render(request, 'news/news/detail.html', {
        'news': news,
        'news_blocks': news_blocks,
        'comments': comments,
        'comments_form': comments_form
    })

#
@user_passes_test(check_admin)
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save()
            messages.success(request, 'Новость создана')
            return redirect('news:news_detail', id=news.id)
    else:
        form = NewsForm()
    return render(request, 'news/news/create.html', {'form': form})
#
#
# @user_passes_test(check_admin)
# def news_update(request, id):
#     news = get_object_or_404(News, id=id)
#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES, instance=news)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Новость изменена')
#             return redirect('news:news_detail', id=news.id)
#     else:
#         form = NewsForm(instance=news)
#     return render(request, 'news/news/update.html',
#                   {'form': form,
#                    'title': 'Редактирование заголовка',
#                    'news': news})
#
#
# @user_passes_test(check_admin)
# def news_delete(request, id):
#     news = get_object_or_404(News, id=id)
#     if request.method == 'POST':
#         news.delete()
#         messages.success(request, 'Новость удалена')
#         return redirect('news:news_list')
#     return render(request, 'news/news/delete.html',
#                   {'news': news})


@login_required
def comment_create(request, id):
    news = get_object_or_404(News, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect('news:news_detail', id=news.id)
    return redirect('news:news_detail', id=news.id)


@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, 'Вы не можете редактировать этот комментарий')
        return redirect('news:news_detail', id=comment.news.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Комментарий изменен')
            return redirect('news:news_detail', id=comment.news.id)
    else:
        form = CommentForm(instance=comment)
    return redirect('news:news_detail', id=comment.news.id)


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        messages.error(request, 'Вы не можете удалить этот комментарий')
        return redirect('news:news_detail', id=comment.news.id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удален')
        return redirect('news:news_detail', id=comment.news.id)
    return redirect('news:news_detail', id=comment.news.id)


@login_required
def news_reaction_create(request, id):
    news = get_object_or_404(News, id=id)
    reaction_type = int(request.POST.get('reaction_type'))
    existing_reaction = Reaction.objects.filter(
        news=news,
        user=request.user).first()
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            existing_reaction.delete()
            messages.info(request, 'Реакция удалена')
        else:
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            messages.success(request, 'Реакция изменена')
    else:
        Reaction.objects.create(
            news=news,
            user=request.user,
            reaction_type=reaction_type
        )
        messages.success(request, 'Реакция добавлена')

    return redirect('news:news_detail', id=news.id)


@login_required
def comment_reaction_create(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    reaction_type = int(request.POST.get('reaction_type'))
    existing_reaction = Reaction.objects.filter(
        comment=comment,
        user=request.user).first()
    if existing_reaction:
        if existing_reaction.reaction_type == reaction_type:
            existing_reaction.delete()
            messages.info(request, 'Реакция удалена')
        else:
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
            messages.success(request, 'Реакция изменена')
    else:
        Reaction.objects.create(
            comment=comment,
            user=request.user,
            reaction_type=reaction_type
        )
        messages.success(request, 'Реакция добавлена')
    return redirect('news:news_detail', id=comment.news.id)