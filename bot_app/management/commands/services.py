import random
from typing import Any, List, Tuple
from telebot import TeleBot, types
from bot_app.models import UserProfile, Game


def check_username(bot: TeleBot):
    def dec(f):
        def inner(msg: types.Message):
            if msg.from_user.username:
                f(msg)
            else:
                bot.send_message(
                    msg.chat.id,
                    text='Пожалуйста, заполните поле username в настройках профиля Telegram.'
                )
        return inner
    return dec


def get_random_user_card(game_title: str, tg_id: int) -> Tuple[str, int]:
    users = UserProfile.objects.filter(
        fav_game__title=game_title,
        searchable=True).exclude(tg_id=tg_id)
    if users:
        user = random.choice(users)
        user_card = '\n'.join((
            f'Telegram: @{user.tg_username}',
            f'Ник в Steam: {user.steam_nickname}',
            user.about
        ))
        user_id = user.tg_id
    else:
        user_card = 'К сожалению, в поиске еще нет игроков'
        user_id = 0
    return user_card, user_id


def get_game_titles() -> List[str]:
    games = Game.objects.all()
    return [game.title for game in games]


def get_game_by_title(game_title: str):
    game = Game.objects.get(title=game_title)
    return game


def get_user_by_tg_id(tg_id: int) -> UserProfile:
    user = UserProfile.objects.get(tg_id=tg_id)
    return user


def update_user_profile(tg_id: int, **kwargs) -> None:
    user = get_user_by_tg_id(tg_id)
    if 'tg_username' in kwargs:
        user.tg_username = kwargs['tg_username']
        user.save()
    elif 'steam_nickname' in kwargs:
        user.steam_nickname = kwargs['steam_nickname']
        user.save()
    elif 'about' in kwargs:
        user.about = kwargs['about']
        user.save()
    elif 'fav_game' in kwargs:
        user.fav_game = kwargs['fav_game']
        user.save()
    elif 'searchable' in kwargs:
        user.searchable = kwargs['searchable']
        user.save()
    else:
        user.save()


def get_or_create_user(tg_id: int) -> Tuple[UserProfile, bool]:
    user, created = UserProfile.objects.get_or_create(tg_id=tg_id)
    return user, created


def is_profile_filled(tg_id: int) -> bool:
    user = get_user_by_tg_id(tg_id)
    is_filled_profile = bool(user.steam_nickname) and \
        bool(user.about) and \
        bool(user.fav_game)
    return is_filled_profile
