from django.db import models


class Game(models.Model):
    title = models.CharField(max_length=300)
    about = models.TextField(null=True)

    def __str__(self):
        return f'{self.title}'


class UserProfile(models.Model):
    tg_username = models.CharField(
        max_length=200,
        verbose_name='Ник в Telegram'
    )
    tg_id = models.PositiveIntegerField(
        verbose_name='ID в Telegram',
        unique=True
    )
    steam_nickname = models.CharField(
        max_length=200,
        verbose_name='Ник в Steam',
        null=True,
        blank=True
    )
    about = models.TextField(
        verbose_name='Поле "О себе"',
        null=True,
        blank=True
    )
    searchable = models.BooleanField(
        verbose_name='Разрешение на появление в поиске',
        default=False
    )
    fav_game = models.ForeignKey(
        verbose_name='Любимая игра',
        to=Game,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'Профиль пользователя. Ник TG: {self.tg_username}, ' \
        f'ID: {self.tg_id}'
        