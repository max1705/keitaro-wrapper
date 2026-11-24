# Keitaro Wrapper

Тестовое задание: обёртка над рекламным трекером Keitaro.
1. **Создаватель кампаний** — создаёт кампанию с двумя потоками (гео → Google и офферы).
2. **Редактор кампаний** — добавление/удаление офферов, пины весов, отложенная публикация (Push / Cancel).

---

## Как запустить

### 1. Бэкенд

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Создать файл .env на основе примера:

```bash
copy .env.example .env   # Windows
```
Пример содержимого .env:
```bash
KEITARO_API_URL=https://keitaro-for-tests.etolegko.com/admin_api/v1
KEITARO_API_KEY=твой_ключ_со_стенда
DATABASE_URL=sqlite:///./keitaro.db
```
Применить миграции и запустить:

```bash
alembic upgrade head
python -m uvicorn app.main:app --reload
```
Бэкенд доступен на http://127.0.0.1:8000. Swagger: http://127.0.0.1:8000/docs.

### 2. Фронтенд
В новом терминале:

```bash
cd frontend
npm install
npm run dev
```
Фронтенд доступен на http://localhost:5173.

### Миграции (Alembic)
Если изменил модели в backend/app/models.py:

```bash
cd backend
# venv должен быть активирован
alembic revision --autogenerate -m "описание изменений"
alembic upgrade head
```
###  Откатить последнюю миграцию:

```bash
alembic downgrade -1
```
#### Как это работает
Fetch Streams — тянет потоки кампании из Keitaro и синхронизирует их с локальной БД.

Локальные изменения — добавление/удаление офферов и пины весов меняют только локальную БД. Поток становится «жёлтым» (не опубликован).

Push to KT — отправляет текущий состав офферов в Keitaro (PUT /streams/{id}).

Cancel — откатывает локальные изменения к состоянию из Keitaro.

Removed-офферы — при удалении оффер остаётся в БД серым (share = 0), его можно вернуть кнопкой Bring back.

#### Логика весов
При любом изменении состава офферов веса пересчитываются так, чтобы сумма была равна 100%.

Запиненные офферы сохраняют свой вес, а остальные делят оставшийся процент поровну.

#### Примечания
API-ключ и URL стенда хранятся в .env (файл не коммитится в Git).

База данных — SQLite, файл backend/keitaro.db создаётся автоматически при первом запуске.