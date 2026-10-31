# Movie Catalog API

Учебный REST API на FastAPI для ведения каталога фильмов. Сервис позволяет добавлять фильмы, получать список и отдельные записи, фильтровать каталог, сортировать результаты и удалять записи.

## Основные возможности

- создание фильма с проверкой входных данных;
- просмотр каталога и фильма по ID;
- фильтрация по жанру и году выпуска;
- сортировка по названию, году или рейтингу;
- удаление фильма;
- проверка доступности сервиса через health endpoint.

## Технологический стек

- Python 3.11+;
- FastAPI и Uvicorn;
- SQLAlchemy 2;
- Pydantic 2;
- SQLite;
- Alembic для миграций.

## Структура проекта

```text
movie-catalog/
├── alembic/
│   ├── versions/
│   │   └── 0001_create_movies.py
│   └── env.py
├── app/
│   ├── __init__.py
│   └── main.py
├── .gitignore
├── alembic.ini
├── README.md
└── requirements.txt
```

## Быстрый старт

```bash
git clone https://github.com/leoeoeo20/movie-catalog.git
cd movie-catalog
python -m venv .venv
```

Активируйте виртуальное окружение:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

Установите зависимости, примените миграции и запустите сервер:

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API будет доступен по адресу `http://127.0.0.1:8000`. Интерактивная документация Swagger: `http://127.0.0.1:8000/docs`.

## Основные эндпоинты

| Метод | Путь | Назначение |
|---|---|---|
| `GET` | `/health` | Проверка состояния сервиса |
| `GET` | `/movies` | Получить список фильмов |
| `GET` | `/movies/{movie_id}` | Получить фильм по ID |
| `POST` | `/movies` | Добавить фильм |
| `DELETE` | `/movies/{movie_id}` | Удалить фильм |

Пример тела для `POST /movies`:

```json
{
  "title": "The Matrix",
  "year": 1999,
  "genre": "Science fiction",
  "rating": 8.7
}
```

При отсутствии записи эндпоинты по ID возвращают `404 Not Found`; при успешном создании возвращается `201 Created`.

## Фильтрация и сортировка

Для `GET /movies` доступны query-параметры:

- `genre` — точное совпадение жанра;
- `year` — год выпуска;
- `sort` — поле сортировки: `title`, `year` или `rating` (по умолчанию `title`);
- `order` — направление `asc` или `desc` (по умолчанию `asc`).

Примеры:

```text
GET /movies?genre=Drama&year=2020
GET /movies?sort=rating&order=desc
```

## Модель данных

| Поле | Тип | Описание |
|---|---|---|
| `id` | integer | Первичный ключ, генерируется базой |
| `title` | string | Название фильма, 1–200 символов |
| `year` | integer | Год выпуска, от 1888 до 2100 |
| `genre` | string | Жанр, 1–100 символов |
| `rating` | float | Рейтинг от 0 до 10, по умолчанию 0 |

## Ограничения базы данных

- `id` — первичный ключ;
- `title`, `year`, `genre` и `rating` не могут быть `NULL`;
- год ограничен диапазоном 1888–2100;
- рейтинг ограничен диапазоном 0–10;
- индексы созданы для `title`, `year` и `genre`;
- используется SQLite, файл базы данных `movies.db` создаётся при применении миграции Alembic.

