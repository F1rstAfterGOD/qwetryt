# YouTube Shorts Bot

Telegram бот для создания коротких видео из YouTube роликов через API opus.pro

## Быстрый старт

### 1. Настройка окружения

```bash
# Скопируйте файл конфигурации
copy .env.example .env

# Отредактируйте .env файл и заполните:
# BOT_TOKEN - получите от @BotFather
# OPUS_API_KEY - получите на https://opus.pro
# MONGO_URI - подключение к MongoDB
```

### 2. Запуск через Docker (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

### 3. Локальный запуск

```bash
# Установите зависимости
pip install -r requirements.txt

# Запустите MongoDB
docker run -d -p 27017:27017 mongo:latest

# Запустите приложение
python run.py
```

## Структура проекта

```
youtube-shorts-bot/
├── bot/                 # Telegram бот
│   ├── handlers.py      # Обработчики команд
│   ├── keyboards.py     # Клавиатуры
│   ├── main.py         # Основной модуль бота
│   └── states.py       # FSM состояния
├── api/                # Webhook API
│   ├── main.py         # HTTP сервер
│   └── webhooks.py     # Обработка webhook
├── core/               # Основные модули
│   ├── api.py          # API клиент
│   ├── bot.py          # Бот инициализация
│   ├── logger.py       # Логирование
│   └── mongo.py        # MongoDB подключение
├── db/                 # База данных
│   └── models.py       # Модели данных
├── services/           # Внешние сервисы
│   └── opus_api.py     # Opus.pro API
├── utils/              # Утилиты
│   ├── logger.py       # Логирование
│   ├── validators.py   # Валидация
│   └── watermark.py    # Обработка водяных знаков
├── config/             # Конфигурация
│   └── settings.py     # Настройки
├── .env.example        # Пример конфигурации
├── requirements.txt    # Python зависимости
├── run.py             # Запуск для разработки
└── compose.yml        # Docker конфигурация
```

## Конфигурация

Основные переменные в `.env`:

```env
# Telegram Bot
BOT_TOKEN=your_bot_token_here
WEBHOOK_BASE_URL=https://yourdomain.com
WEBHOOK_SECRET=your_webhook_secret

# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=youtube_shorts_bot

# Opus.pro API
OPUS_API_KEY=your_opus_api_key
OPUS_WEBHOOK_SECRET=your_opus_webhook_secret
```

##  Функционал

-  Обработка YouTube ссылок (youtube.com, youtu.be, shorts)
-  Интеграция с Opus.pro для нарезки видео
-  Webhook уведомления о готовности
-  Водяные знаки (настройка позиции, размера, прозрачности)
-  База данных для отслеживания задач
-  Docker поддержка

##  API Endpoints

- `POST /webhooks/opus` - Webhook от Opus.pro
- `GET /health` - Проверка состояния API

##  Использование

1. Отправьте `/start` боту
2. Отправьте ссылку на YouTube видео
3. Дождитесь уведомления о готовности
4. Получите ссылки на нарезанные клипы

##  Получение API ключей

### Telegram Bot Token
1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в `.env`

### Opus.pro API
1. Зарегистрируйтесь на https://opus.pro
2. Перейдите в API раздел
3. Создайте API ключ
4. Настройте webhook URL: `https://yourdomain.com/webhooks/opus`

##  Решение проблем

### MongoDB не подключается
```bash
docker run -d -p 27017:27017 mongo:latest
```

### Бот не отвечает
- Проверьте BOT_TOKEN в .env
- Убедитесь что токен получен от @BotFather

### Webhook не работает
- WEBHOOK_BASE_URL должен быть HTTPS
- Сервер должен быть доступен извне
- Проверьте OPUS_WEBHOOK_SECRET