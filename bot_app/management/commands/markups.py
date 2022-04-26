from telebot import types
from .services import get_game_titles

to_main_btn = types.InlineKeyboardButton(
    text='На главную',
    callback_data='main'
)


def get_start_markup() -> types.InlineKeyboardMarkup:
    start_btn = types.InlineKeyboardButton(
        text='Начнем',
        callback_data='edit_profile'
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(start_btn)
    return markup


def get_profile_markup() -> types.InlineKeyboardMarkup:
    steam_nickname_btn = types.InlineKeyboardButton(
        text='Ник в Steam',
        callback_data='steam_nickname'
    )
    about_btn = types.InlineKeyboardButton(
        text='О себе',
        callback_data='about'
    )
    fav_game_btn = types.InlineKeyboardButton(
        text='Любимая игра',
        callback_data='fav_game'
    )
    searchable_btn = types.InlineKeyboardButton(
        text='Видимость профиля для других пользователей',
        callback_data='searchable'
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        steam_nickname_btn,
        about_btn,
        fav_game_btn,
        searchable_btn
    )
    return markup


def get_main_markup() -> types.InlineKeyboardMarkup:
    find_teammate_btn = types.InlineKeyboardButton(
        text='Найти тиммейтов',
        callback_data='find_teammate'
    )
    edit_profile_btn = types.InlineKeyboardButton(
        text='Редактировать профиль',
        callback_data='edit_profile'
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(find_teammate_btn, edit_profile_btn)
    return markup


def get_game_markup(prefix: str) -> types.InlineKeyboardMarkup:
    game_titles = get_game_titles()
    markup = types.InlineKeyboardMarkup()
    for title in game_titles:
        markup.add(
            types.InlineKeyboardButton(
                text=title,
                callback_data=prefix+title
            )
        )
    return markup


def get_teammate_markup(game_title, teammate_tg_id) -> types.InlineKeyboardMarkup:
    next_btn = types.InlineKeyboardButton(
        text='Следующий',
        callback_data='teammate'+game_title
    )
    like_btn = types.InlineKeyboardButton(
        text='Like',
        callback_data='notify'+str(teammate_tg_id)
    )
    back_btn = types.InlineKeyboardButton(
        text='Назад',
        callback_data='find_teammate'
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    if teammate_tg_id:
        markup.add(like_btn, next_btn, back_btn)
    else:
        markup.add(back_btn)
    return markup


def get_searchable_markup(prefix) -> types.InlineKeyboardMarkup:
    yes_btn = types.InlineKeyboardButton(
        text='Да',
        callback_data=prefix+'1'
    )
    no_btn = types.InlineKeyboardButton(
        text='Нет',
        callback_data=prefix+'0'
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(yes_btn, no_btn)
    return markup
