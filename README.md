Telegram бот для учёта личных расходов и ведения бюджета, [видео с пояснениями по коду и описание](https://www.youtube.com/watch?v=Kh16iosOTIQ).


В переменных окружения надо проставить API токен бота, а также адрес proxy и логин-пароль к ней.

`TELEGRAM_API_TOKEN` — API токен бота

`TELEGRAM_PROXY_URL` — URL прокси сервера

`TELEGRAM_ACCESS_ID` — ID Telegram аккаунта, от которого будут приниматься сообщения (сообщения от остальных аккаунтов игнорируются)

Использование с Docker показано ниже. 
Предварительно заполните ENV переменные, указанные выше,
в Dockerfile, а также в команде запуска укажите локальную директорию с проектом 
вместо `local_project_path`. SQLite база данных будет лежать в папке проекта `db/finance.db`.

```
сборка и запуск:
docker build -t tgfinance ./
docker run -dit --restart unless-stopped --name tg -v /local_project_path/db:/home/db tgfinance

заливка на докерхаб:
docker login --username username
docker tag tgfinance username/tgfinance
docker push username/tgfinance
```
