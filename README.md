## TestBot
* При остутствии username в Телеграме, бот не позволяет совершать никаких действий и сообщает об отсутствии
* При запуске бота пользователь создает личный профиль
* В профиле есть поля "Ник в Steam", "О себе", "Любимая игра", "Разрешение на появление в поиске", который настраивает пользователь
* Имеются автоматически заполняемые поля ID в Телеграм и username в Телеграм
* После создания профиля есть возможность его отредактировать
* В базу данных внесены несколько пользователей, а также игры, из которых пользователь выбирает любимую игру, а также поиск тиммейтов
* При нажатии на кнопку "Like" при поиске тиммейтов, пользователю, которому принадлежит карточка, отправляется сообщение от бота
* Для работы с базой данных используется Django ORM
* Бот работает в режиме polling
## Запуск
### Для локального запуска
* Для запуска бота необходимо внести токен в переменную среды TG_BOT_TOKEN
* Для админ панели
```
python manage.py runserver
```
* Бот
```
python manage.py bot
```
### Для запуска в докере
* Для запуска бота необходимо внести токен в переменную среды TG_BOT_TOKEN в Dockerfile
```
docker-compose up -d --build
```