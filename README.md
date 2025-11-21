# Currency Converter Microservice

Асинхронный микросервис на FastAPI, который обращается к публичному API currate.ru, кэширует курсы валют и предоставляет HTTP‑интерфейс с простым фронтендом.

## Возможности
- Актуальные курсы валют через эндпоинт `/convert` с кешированием на 10 минут.
- Список доступных валютных пар через `/currencies`.
- Готовый фронт на `/` (Jinja2 + vanilla JS) с формой конвертации и списком валют.
- Асинхронный HTTP‑клиент на `httpx`, чтение настроек через `.env`.
- Готовый Dockerfile для деплоя.

## Требования
- Python 3.11+ с `pip`.
- Аккаунт на [currate.ru](https://currate.ru) и персональный API‑ключ.
- (Опционально) Docker 24+ для контейнерного запуска.

## Быстрый старт (локально)
```bash
git clone <repo-url>
cd currency-converter
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Создайте файл `.env` в корне проекта (или переименуйте имеющийся пример) и добавьте ключ:
```env
CURRATE_API_KEY=ваш_ключ_с_currate
```

Запустите сервис:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу `http://127.0.0.1:8000/`.  
Документация Swagger — `http://127.0.0.1:8000/docs`.

## Запуск в Docker
```bash
docker build -t currency-converter .
docker run \
  -e CURRATE_API_KEY=ваш_ключ_с_currate \
  -p 8000:8000 \
  currency-converter
```

## Переменные окружения
| Название          | Описание                                           |
|-------------------|-----------------------------------------------------|
| `CURRATE_API_KEY` | API‑ключ аккаунта currate.ru (обязателен).          |

## API

### `GET /convert`
Параметры query:
- `from_currency` — тикер исходной валюты (например, `USD`).
- `to_currency` — тикер целевой валюты (например, `RUB`).
- `amount` — сумма для конвертации (float).

Пример запроса:
```
GET /convert?from_currency=USD&to_currency=RUB&amount=10
```

Пример ответа:
```json
{
  "from_currency": "USD",
  "to_currency": "RUB",
  "rate": 91.024,
  "amount": 10.0,
  "converted": 910.24
}
```

### `GET /currencies`
Возвращает список строк вроде `"EURUSD"`, `"USDRUB"` и т.д. Используется фронтендом для datalist и сетки валютных пар.

### `GET /`
HTML‑страница, которая:
- Отображает список всех валютных пар.
- Предоставляет форму конвертации (выбирает валюты из datalist, подтягивает курс через `/convert`).
- Показывает результат конвертации и ошибки, если пара недоступна.

## Технические детали
- `app/services.py` использует `httpx.AsyncClient` и `python-dotenv`, поэтому ключ из `.env` подхватывается автоматически.
- `app/cache.py` даёт простейший in-memory кеш (10 минут) для курсов, чтобы не спамить API currate.ru.
- Шаблоны находятся в `app/templates/`. В `index.html` минимум CSS/JS для быстрого UI без внешних зависимостей.

## Отладка и типичные проблемы
- **Пустой список валют.** Убедитесь, что переменная `CURRATE_API_KEY` задана и ключ активен. После изменения `.env` перезапустите Uvicorn.
- **`ModuleNotFoundError: httpx` или `jinja2`.** Проверьте, что виртуальное окружение активировано и выполнен `pip install -r requirements.txt`.
- **API возвращает 4xx/5xx.** Библиотека `httpx` поднимает исключение, а `/convert` отдаёт `400 Invalid currency pair`. Проверьте тикеры и доступность пары на currate.
- **Слишком частые запросы.** currate.ru ограничивает частоту обращений для бесплатных ключей; кэш спасает в большинстве случаев, но при необходимости увеличьте `CACHE_LIFETIME` в `app/cache.py`.
