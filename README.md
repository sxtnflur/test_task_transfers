# Transfers API

Сервис на FastAPI для приёма и обработки заявок на переводы. Заявка сохраняется в PostgreSQL, а её обработка выполняется в фоновой задаче. После завершения сервис отправляет результат на настроенный webhook, подписывая тело запроса HMAC-SHA256.

## Возможности

- создание перевода через HTTP API;
- идемпотентность по `external_id`;
- хранение переводов и их статусов в PostgreSQL;
- Bearer-аутентификация API;
- валидация суммы и валюты;
- асинхронная доставка webhook с заголовком `X-signature`;
- миграции Alembic и тесты pytest.

## Требования

- Python 3.13;
- PostgreSQL;
- доступная конечная точка для webhook (для локальной проверки можно использовать `POST /transfer/test_webhook`).

## Настройка

Создайте окружение и установите зависимости:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements/main.txt
pip install -r requirements/test.txt
```

Скопируйте пример конфигурации и заполните значения:

```bash
cp .env.example .env
```

Переменные `.env`:

| Переменная | Назначение |
| --- | --- |
| `API_TOKEN` | Токен для Bearer-аутентификации и ключ подписи webhook. |
| `WEBHOOK_URL` | URL, на который отправляется результат обработки перевода. |
| `TX_FROM_ADDRESS` | Адрес отправителя, включаемый в webhook. |
| `DATABASE_URL` | URL базы данных в формате SQLAlchemy async, например `postgresql+asyncpg://postgres:password@localhost:5432/test_transfers`. |

Создайте указанную в `DATABASE_URL` базу данных и примените миграции:

```bash
alembic upgrade head
```

## Запуск

```bash
uvicorn main:create_app --app-dir src --host 0.0.0.0 --port 8000
```

После запуска интерактивная документация доступна по адресу <http://localhost:8000/docs>.

## API

### Создать перевод

`POST /transfer`

Заголовки:

```http
Authorization: Bearer <API_TOKEN>
Content-Type: application/json
```

Пример запроса:

```bash
curl -X POST http://localhost:8000/transfer \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "order-1001",
    "currency": "usd",
    "amount": "125.50",
    "destination": "0xRecipientAddress",
    "comment": "Payment for order #1001"
  }'
```

Ответ `200 OK`:

```json
{
  "id": "f4f42611-c63a-480d-9db8-6c482968379e",
  "external_id": "order-1001",
  "currency": "USD",
  "amount": 125.5,
  "destination": "0xRecipientAddress",
  "status": "pending"
}
```

Повторный запрос с тем же `external_id` вернёт уже созданный перевод. Сумма должна быть больше нуля; код валюты приводится к верхнему регистру и должен содержать три символа.

## Webhook

По завершении фоновой обработки на `WEBHOOK_URL` отправляется `POST` с JSON:

```json
{
  "id": "f4f42611-c63a-480d-9db8-6c482968379e",
  "external_id": "order-1001",
  "amount": 125.5,
  "status": "completed",
  "details": {
    "from_address": "0xSenderAddress",
    "to_address": "0xRecipientAddress",
    "tx_hash": null
  }
}
```

Заголовок `X-signature` содержит hex-представление HMAC-SHA256 от тела запроса. В качестве HMAC-ключа используется SHA-256 от `API_TOKEN` в UTF-8. Получатель должен проверить подпись перед обработкой уведомления.

## Тесты

Тесты используют базу из `DATABASE_URL`; в её имени обязательно должен быть суффикс `/test_transfers`. Перед каждым набором тестов таблицы в этой базе пересоздаются.

```bash
pytest
```

## Структура проекта

```text
src/
├── auth/                         # Bearer-аутентификация
├── config/                       # настройки приложения
└── transfers/
    ├── domain/                   # сущности, статусы и value objects
    ├── app/                      # сценарии создания перевода и webhook
    ├── infra/                    # PostgreSQL и HTTP-клиент webhook
    └── presentation/http/        # FastAPI-роуты, схемы и обработчики ошибок
migrations/                       # миграции Alembic
tests/                            # domain-, application- и infrastructure-тесты
```
