from django.conf import settings
from django.core.management.base import BaseCommand
from telebot import TeleBot, types
from .services import (
    check_username,
    get_random_user_card,
    update_user_profile,
    get_game_by_title,
    get_or_create_user,
    is_profile_filled
)
from .markups import (
    get_main_markup,
    get_profile_markup,
    get_start_markup,
    get_game_markup,
    get_teammate_markup,
    get_searchable_markup,
    to_main_btn
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        bot = TeleBot(token=settings.TOKEN)

        @bot.message_handler(commands=['start'])
        @check_username(bot=bot)
        def start_command(message: types.Message):
            chat_id = message.chat.id
            _, created = get_or_create_user(tg_id=message.from_user.id)
            update_user_profile(
                tg_id=message.from_user.id,
                tg_username=message.from_user.username
            )
            filled = is_profile_filled(message.from_user.id)
            if created:
                bot.send_message(
                    chat_id=chat_id,
                    text='Рад знакомству, профиль успешно создан.\nДавайте заполним его.',
                    reply_markup=get_start_markup()
                )
            elif not filled:
                bot.send_message(
                    chat_id=chat_id,
                    text='Мы уже знакомы, но профиль еще не заполнен.\nДавайте заполним его.',
                    reply_markup=get_start_markup()
                )
            elif filled:
                bot.send_message(
                    chat_id=chat_id,
                    text='Похоже, мы уже знакомы и ваш профиль заполнен.\nДавайте найдем вам тиммейтов',
                    reply_markup=get_main_markup()
                )

        @bot.callback_query_handler(func=lambda call: call.data == 'main')
        def main(call: types.CallbackQuery):
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Похоже, мы уже знакомы и ваш профиль заполнен.\nДавайте найдем вам тиммейтов.',
                reply_markup=get_main_markup()
            )

        @bot.callback_query_handler(func=lambda call: call.data == 'edit_profile')
        def edit_profile(call: types.CallbackQuery):
            markup = get_profile_markup()
            if is_profile_filled(tg_id=call.from_user.id):
                markup.add(to_main_btn)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Редактирование профиля',
                reply_markup=markup
            )

        @bot.callback_query_handler(func=lambda call: call.data == 'find_teammate')
        def find_teammate(call: types.CallbackQuery):
            markup = get_game_markup(prefix='teammate')
            markup.add(to_main_btn)
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Выберите игру из списка ниже',
                reply_markup=markup
            )

        @bot.callback_query_handler(func=lambda call: call.data.startswith('teammate'))
        def show_teammate(call: types.CallbackQuery):
            game_title = call.data.removeprefix('teammate')
            user_card, teammate_tg_id = get_random_user_card(
                game_title=game_title,
                tg_id=call.from_user.id
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text=user_card,
                reply_markup=get_teammate_markup(
                    game_title=game_title,
                    teammate_tg_id=teammate_tg_id
                )
            )

        @bot.callback_query_handler(func=lambda call: call.data.startswith('notify'))
        def notify_teammate(call: types.CallbackQuery):
            teammate_tg_id = call.data.removeprefix('notify')
            tg_username = call.from_user.username
            bot.send_message(
                chat_id=teammate_tg_id,
                text=f'Пользователю @{tg_username} понравилась ваша карточка. Напишите ему!'
            )

        @ bot.callback_query_handler(func=lambda call: call.data == 'steam_nickname')
        def set_steam_nickname(call: types.CallbackQuery):
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Введите свой ник в Steam'
            )
            bot.register_next_step_handler(
                message=call.message,
                callback=step_steam_nickname,
                call=call
            )

        def step_steam_nickname(message: types.Message, **kwargs):
            update_user_profile(
                tg_id=message.from_user.id,
                steam_nickname=message.text
            )
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.id
            )
            edit_profile(call=kwargs['call'])

        @ bot.callback_query_handler(func=lambda call: call.data == 'about')
        def set_about(call: types.CallbackQuery):
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Расскажите немного о себе:'
            )
            bot.register_next_step_handler(
                message=call.message,
                callback=step_about,
                call=call
            )

        def step_about(message: types.Message, **kwargs):
            update_user_profile(
                tg_id=message.from_user.id,
                about=message.text
            )
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.id
            )
            edit_profile(call=kwargs['call'])

        @ bot.callback_query_handler(func=lambda call: call.data == 'fav_game')
        def set_fav_game(call: types.CallbackQuery):
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Выберите игру из списка ниже',
                reply_markup=get_game_markup(prefix='fav_game')
            )

        @ bot.callback_query_handler(func=lambda call: call.data.startswith('fav_game'))
        def step_fav_game(call: types.CallbackQuery):
            game_title = call.data.removeprefix('fav_game')
            fav_game = get_game_by_title(game_title)
            update_user_profile(
                tg_id=call.from_user.id,
                fav_game=fav_game
            )
            edit_profile(call=call)

        @ bot.callback_query_handler(func=lambda call: call.data == 'searchable')
        def set_searchable(call: types.CallbackQuery):
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text='Хотите, чтобы ваш профиль появлялся в поиске?',
                reply_markup=get_searchable_markup(prefix='searchable')
            )

        @ bot.callback_query_handler(func=lambda call: call.data.startswith('searchable'))
        def step_searchable(call: types.CallbackQuery):
            searchable = call.data.removeprefix('searchable')
            update_user_profile(
                tg_id=call.from_user.id,
                searchable=bool(int(searchable))
            )
            edit_profile(call=call)

        bot.polling(non_stop=True)
