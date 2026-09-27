# Space Photos

Учебный проект по работе с HTTP API, изображениями и Telegram Bot API.

Скрипты скачивают фотографии космоса из NASA и Wikimedia Commons, сохраняют их в локальную директорию и публикуют фотографии в Telegram-канал.

## Что умеет проект

- скачивать фотографии запусков SpaceX из Wikimedia Commons;
- скачивать фотографии NASA APOD;
- скачивать фотографии Земли NASA EPIC;
- публиковать указанную фотографию в Telegram-канал;
- если фотография не указана — публиковать случайную фотографию из выбранной директории;
- автоматически публиковать все фотографии из директории по кругу;
- позволять пользователю выбрать директорию для фотографий;
- позволять пользователю указать другой файл с переменными окружения;
- перемешивать фотографии перед каждым новым циклом публикации;
- автоматически уменьшать слишком большие по разрешению изображения перед отправкой в Telegram;
- при необходимости работать через пользовательский HTTP/SOCKS-прокси.

## Требования

Рекомендуемая версия Python:

```text
Python 3.10
```

Проект использует:

```text
python-telegram-bot==13.15
```

## Установка

Склонируйте репозиторий:

```bash
git clone https://github.com/Suba79/space_photos.git
cd space_photos
```

Создайте виртуальное окружение.

Windows:

```powershell
py -3.10 -m venv .venv
```

Linux/macOS:

```bash
python3.10 -m venv .venv
```

Активируйте виртуальное окружение.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## Переменные окружения

По умолчанию скрипты загружают настройки из файла `.env` в корне проекта.

Создайте `.env`:

```env
NASA_API_KEY=your_nasa_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@your_channel_username
```

Для автоматической публикации можно дополнительно задать:

```env
PUBLISH_DELAY=14400
```

### `NASA_API_KEY`

API-ключ NASA.

Получить ключ можно на сайте:

https://api.nasa.gov/

### `TELEGRAM_BOT_TOKEN`

Токен Telegram-бота, полученный через `@BotFather`.

Не публикуйте токен в GitHub.

### `TELEGRAM_CHANNEL_ID`

Username Telegram-канала, куда бот будет публиковать фотографии.

Пример:

```env
TELEGRAM_CHANNEL_ID=@my_space_photos_channel
```

Бот должен быть добавлен в канал как администратор и иметь право публиковать сообщения.

### `PUBLISH_DELAY`

Интервал между автоматическими публикациями в секундах.

Если переменная не задана, используется 4 часа:

```text
14400
```

Для быстрой проверки можно временно указать:

```env
PUBLISH_DELAY=10
```

После проверки удалите эту переменную или верните `14400`.

### `PROXY_URL` — необязательно

Прокси не нужен, если NASA, Wikimedia Commons и Telegram доступны напрямую.

Если в вашей сети нужен уже настроенный HTTP/SOCKS-прокси, укажите его адрес:

```env
PROXY_URL=socks5h://127.0.0.1:10808
```

Проект сам не запускает прокси-сервер.

## Другой файл настроек

По умолчанию используется:

```text
.env
```

Можно указать другой файл через `--env-file`:

```bash
python fetch_nasa_epic.py --env-file path/to/settings.env
```

Такая же опция доступна во всех запускаемых скриптах:

```bash
python fetch_spacex_images.py --env-file path/to/settings.env
python fetch_nasa_apod.py --env-file path/to/settings.env
python fetch_nasa_epic.py --env-file path/to/settings.env
python telegram_bot.py --env-file path/to/settings.env
python publish_photos.py --env-file path/to/settings.env
```

Если нужные переменные уже заданы в операционной системе, отдельный `.env` можно не использовать.

## Директория с фотографиями

По умолчанию используется директория:

```text
images
```

Путь можно изменить без редактирования исходного кода при помощи `--directory`.

Например:

```bash
python fetch_nasa_epic.py --directory test_images
```

Скрипт создаст `test_images`, если директории ещё нет, и сохранит фотографии туда.

Эта опция доступна для всех скриптов, работающих с директорией изображений:

```bash
python fetch_spacex_images.py --directory my_photos
python fetch_nasa_apod.py --directory my_photos
python fetch_nasa_epic.py --directory my_photos
python telegram_bot.py --directory my_photos
python publish_photos.py --directory my_photos
```

У `telegram_bot.py` параметр `--directory` используется для выбора случайной фотографии, если конкретный путь к файлу не передан.

## Запуск и проверка

Все команды ниже выполняются из корневой директории проекта при активированном виртуальном окружении.

### Скачать фотографии SpaceX

С настройками по умолчанию:

```bash
python fetch_spacex_images.py
```

Можно передать свой поисковый запрос:

```bash
python fetch_spacex_images.py "Falcon 9 Starlink 6-38"
```

Можно указать другую директорию:

```bash
python fetch_spacex_images.py --directory my_photos
```

Как проверить результат:

- в выбранной директории появились файлы `spacex1.jpg`, `spacex2.jpg` и другие;
- изображения открываются обычным просмотрщиком.

### Скачать фотографии NASA APOD

```bash
python fetch_nasa_apod.py
```

В другую директорию:

```bash
python fetch_nasa_apod.py --directory my_photos
```

Как проверить результат:

- в выбранной директории появились файлы вида `nasa_apod_1.jpg`, `nasa_apod_2.png` и т. п.;
- часть APOD может быть видео, поэтому количество скачанных изображений может быть меньше количества запрошенных записей.

### Скачать фотографии NASA EPIC

```bash
python fetch_nasa_epic.py
```

В другую директорию:

```bash
python fetch_nasa_epic.py --directory test_images
```

Как проверить результат:

- в выбранной директории появились PNG-файлы вида `nasa_epic_1.png`;
- скрипт скачивает до 10 фотографий Земли.

### Опубликовать конкретную фотографию в Telegram

Передайте путь к фотографии размером меньше 10 МБ:

```bash
python telegram_bot.py images/spacex2.jpg
```

Можно использовать любой другой путь:

```bash
python telegram_bot.py my_photos/photo.jpg
```

Как проверить результат:

- именно указанный файл появился в Telegram-канале.

Файлы размером больше 10 МБ не отправляются.

Если изображение слишком большое по разрешению для Telegram, скрипт уменьшает копию изображения в памяти. Оригинальный файл не изменяется.

### Опубликовать случайную фотографию

Из стандартной директории `images`:

```bash
python telegram_bot.py
```

Из другой директории:

```bash
python telegram_bot.py --directory test_images
```

Как проверить результат:

- в Telegram-канале появилась одна из фотографий из выбранной директории.

### Запустить автоматическую публикацию

Из стандартной директории:

```bash
python publish_photos.py
```

Из другой директории:

```bash
python publish_photos.py --directory test_images
```

Скрипт:

1. находит файлы `.jpg`, `.jpeg` и `.png`;
2. пропускает файлы тяжелее 10 МБ;
3. перемешивает список фотографий;
4. публикует их по одной;
5. ждёт время, указанное в `PUBLISH_DELAY`;
6. после публикации всех фотографий снова перемешивает список;
7. повторяет цикл бесконечно.

Для быстрой проверки установите в `.env`:

```env
PUBLISH_DELAY=10
```

Запустите:

```bash
python publish_photos.py --directory test_images
```

Как проверить результат:

- первая фотография появилась в канале;
- примерно через 10 секунд появилась следующая;
- затем публикация продолжается с тем же интервалом.

Остановить скрипт:

```text
Ctrl + C
```

После проверки удалите `PUBLISH_DELAY=10` из `.env` или верните значение `14400`.

## Проверка параметров

У каждого скрипта с аргументами можно посмотреть доступные параметры:

```bash
python fetch_spacex_images.py --help
python fetch_nasa_apod.py --help
python fetch_nasa_epic.py --help
python telegram_bot.py --help
python publish_photos.py --help
```

## Проверка инструкции с нуля

Чтобы убедиться, что README не зависит от старого окружения:

1. откройте новую консоль;
2. склонируйте репозиторий в новую директорию;
3. создайте новое виртуальное окружение;
4. установите зависимости через `requirements.txt`;
5. создайте `.env` или подготовьте другой файл настроек;
6. последовательно запустите скрипты по инструкциям выше;
7. дополнительно проверьте работу `--directory` и `--env-file`;
8. сверяйте результат с пунктами «Как проверить результат».

## Структура проекта

```text
space_photos/
├── fetch_spacex_images.py   # скачивание фотографий SpaceX
├── fetch_nasa_apod.py       # скачивание NASA APOD
├── fetch_nasa_epic.py       # скачивание NASA EPIC
├── telegram_bot.py          # публикация одной фотографии
├── publish_photos.py        # автоматическая публикация фотографий
├── utils.py                 # общие вспомогательные функции
├── requirements.txt         # зависимости проекта
├── README.md
├── .gitignore
├── .env                     # локальные секретные настройки, не добавляется в Git
└── images/                  # директория по умолчанию, не добавляется в Git
```

## Безопасность

Файл `.env` содержит секретные данные и добавлен в `.gitignore`.

Директория `images` также добавлена в `.gitignore`.

Перед коммитом проверьте:

```bash
git status
```

В списке файлов для коммита не должны появляться `.env` и содержимое `images/`.

## Зависимости

Основные библиотеки:

- `requests` — HTTP-запросы;
- `PySocks` — поддержка SOCKS-прокси;
- `python-dotenv` — загрузка переменных окружения;
- `python-telegram-bot==13.15` — работа с Telegram Bot API;
- `Pillow` — подготовка и уменьшение изображений перед отправкой в Telegram.

Полный список зависимостей находится в `requirements.txt`.

## Цель проекта

Код написан в учебных целях в рамках курса Devman по работе с API веб-сервисов.
