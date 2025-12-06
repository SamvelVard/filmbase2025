from django.db import models
from django.utils import timezone
from django.conf import settings


class MyModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class News(MyModel):
    title = models.CharField("Заголовок", max_length=400)
    image = models.ImageField("Фото", upload_to='IMGnews/for_title/', blank=True, null=True)
    published_at = models.DateTimeField("Дата добавления",
                                        help_text="Когда новость станет видна пользователям",
                                        default=timezone.now)
    is_published = models.BooleanField("Опубликовано",
                                       help_text="Отображать новость на сайте",
                                       default=True)


    @property
    def likes_count(self):
        return self.reactions.filter(reaction_type='like').count()

    @property
    def dislikes_count(self):
        return self.reactions.filter(reaction_type='dislike').count()

    @property
    def comments_count(self):
        return self.comments.filter(is_published=True).count()

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


class NewsBlock(MyModel):
    news = models.ForeignKey(News, on_delete=models.CASCADE,
                             related_name='blocks', verbose_name="Блок новости")
    title = models.CharField("Заголовок блока", max_length=400, blank=True)
    content = models.TextField("Содержание блока")
    image = models.ImageField("Изображение для блока",
                              upload_to='IMGnews/blocks', blank=True, null=True)
    order = models.PositiveIntegerField("Порядок блоков", default=0)
    background_color = models.CharField("Цвет фона", default="#ffffff", max_length=7)

    class Meta:
        verbose_name = "Блок новости"
        verbose_name_plural = "Блоки новостей"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Блок: {self.title or 'Без названия'}"


class Comment(MyModel):
    content = models.TextField("Текс комментария")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name="Автор комментария",
                             related_name='news_comments',
                             on_delete=models.CASCADE)
    news = models.ForeignKey(News, verbose_name="Новость",
                             related_name='comments',
                             on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name="Ответ на комментарий",
                               related_name='replies')
    published_at = models.DateTimeField(default=timezone.now,
                                        verbose_name="Дата добавления")
    is_published = models.BooleanField(default=True,
                                       verbose_name="Опубликовано")

    @property
    def likes_count(self):
        return self.reactions.filter(reaction_type='like').count()

    @property
    def dislikes_count(self):
        return self.reactions.filter(reaction_type='dislike').count()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-published_at']

    def __str__(self):
        return f"Комментарий от {self.user.username}"


class Reaction(MyModel):
    LIKE = 1
    DISLIKE = -1
    REACTION_CHOICES = [(LIKE, "👍"), (DISLIKE, "👎")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name="Пользователь",
                             related_name='reactions')
    reaction_type = models.IntegerField("Тип реакции",
                                        choices=REACTION_CHOICES,
                                        default=REACTION_CHOICES[0])
    news = models.ForeignKey(News, on_delete=models.CASCADE,
                             null=True, blank=True,
                             verbose_name="Новость",
                             related_name='reactions')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                null=True, blank=True,
                                verbose_name="Комментарий",
                                related_name='reactions')
    class Meta:
        verbose_name = "Реакция"
        verbose_name_plural = "Реакции"
        ordering = ['-created_at']
        unique_together = [
            ['user', 'news'],
            ['user', 'comment'],
        ]

    def __str__(self):
        if self.news:
            target = f"Новость '{self.news.title[:20]}...'"
        else:
            target = f"Комментарий #{self.comment.id}"
        return f"{self.get_reaction_type_display()} от {self.user.username} на {target}"