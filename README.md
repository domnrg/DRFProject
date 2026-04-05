# DRF Project

Учебный проект LMS системы на Django REST Framework с поддержкой оплаты, подписок и асинхронных задач

## Возможности
- Регистрация и аутентификация пользователей
- Создание, редактирование и удаление привычек
- Ограничение прав доступа
- Подписка на обновления курсов
- Отображение статуса подписки пользователя
- Пагинация списков курсов и уроков
- Фильтрация платежей:
  - по дате
  - по курсу/уроку
  - по способу оплаты
- Интеграция со Stripe:
  - создание продукта
  - создание цены
  - получение ссылки на оплату
- Валидация ссылок (разрешен только YouTube)
- Swagger и ReDoc документация API 
- Асинхронные задачи:
  - уведомления об обновлении курсов
  - деактивация неактивных пользователей
- Работа через Celery + Redis
- Контейнеризация (Docker Compose):
  - "web" - Django
  - "db" - PostgreSQL
  - "redis" - Redis для очередей
  - "celery" - Celery Worker
  - "celery-beat" - планировщик периодических задач
  - nginx - reverse proxy
- В продакшен-среде приложение запускается с использованием Gunicorn
- Автоматический деплой (CI/CD)

## Технологии
- Python 3.10+
- Django 5.x
- Djangorestframework
- Redis 
- Celery
- Celery-beat
- Docker
- Docker Compose
- Nginx
- GitHub Actions

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/username/DRFProject.git
```
2. Создайте файл окружения на основе шаблона .env.sample.

### Пример файла .env.sample
```
SECRET_KEY=
STRIPE_API_KEI=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
TELEGRAM_TOKEN=
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
```
3. Откройте файл .env и заполните необходимые переменные:
```
SECRET_KEY=your_secret_key
STRIPE_API_KEI=your_srtipe_key
POSTGRES_DB=habittracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgras_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
TELEGRAM_TOKEN=your_token
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
4. Соберите и запустите контейнеры:
```
docker compose up -d --build
```
5. Примените миграции:
```
docker compose exec web python manage.py migrate
```
6. Создайте суперпользователя:
```
docker compose exec web python manage.py createsuperuser
```
## Доступ к сервисам:

Перейти в браузере:

Главная старница: http://localhost:8000/
Админка: http://localhost:8000/admin/
Swagger документация: http://localhost:8000/swagger/
ReDoc документация: http://localhost:8000/redoc/

## Проверка работоспособности:

После запуска проекта
```
docker compose up -d --build
```
убедитесь что все сервисы работают корректно:

1. "web" - Django сервер

Откройте в браузере http://localhost:8000/swagger/
Если страница открывается - сервис работает

Проверка через логи
```
docker compose logs -f web
```
2. "db" - PostgreSQL

Проверка подключения к базе:
```
docker compose exec db psql -U postgres
```
Если удалось войти в консоль PostgreSQL - база работает

Проверка таблиц:
```
\dt
```
3. "redis"

Проверка через CLI:
```
docker compose exec redis redis-cli
```
Внутри выполнить
```
ping
```
Ожидаемый ответ:
```
PONG
```
4. "celery" - Celery Worker

Проверка логов:
```
docker compose logs -f celery
```
Ожидаемо увидеть:
 - подключение к Redis
 - (Task received)

5. "celery-beat"

Проверка логов:
```
docker compose logs -f celery-beat
```
Ожидаемо увидеть:
 - отправку периодических задач
 - сообщение вида
```
Scheduler: Sending due task
```
## Деплой на сервер:

1. Подключитесь к серверу.
```
ssh user@server_ip
```
2. Установите Docker.
```
sudo apt update
sudo apt install docker.io docker-compose -y
```
3. Запуск.
```
git clone <repo_url>
cd project
docker compose up --build
```
## Автоматический деплой (CI/CD)

В проекте настроен GitHub Actions workflow для автоматической проверки и деплоя приложения.

### Как работает workflow

При каждом push выполняются следующие шаги:

1. Запускается линтер (flake8)
2. Запускаются тесты Django
3. Собирается Docker-образ
4. Выполняется деплой на удаленный сервер через SSH

Если тесты выполняются с ошибкой - деплой НЕ выполняется

### Необходимые Secrets в GitHub

В репозитории необходимо добавить следующие переменные:

- SERVER_IP - IP-адрес сервера
- SSH_USER - пользователь сервера
- SSH_KEY - приватный SSH-ключ
- DEPLOY_DIR - директория проекта на сервере
- SECRET_KEY=your_secret_key
- STRIPE_API_KEI=your_srtipe_key
- POSTGRES_DB=habittracker
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=your_postgras_password
- POSTGRES_HOST=db
- POSTGRES_PORT=5432

### Процесс деплоя

GitHub Actions выполняет следующие действия:

1. Копирует проект
2. Подключается по SSH
3. Выполняет команды:
```
docker compose down
docker compose up -d --build

docker compose exec -T web python manage.py migrate
docker compose exec -T web python manage.py collectstatic --noinput
```
### Запуск деплоя

1. Закомитте изменения:
```
git add .
git commit -m "update"
git push origin develop
```
2. Перейдите во вкладку "Actions" в GitHub
3. Убедитесь, что workflow успешно выполнен
После успешного выполнения приложение автоматически обновится на сервере.

### Особенности проекта

- Для тестов используется SQLite
- Для продакшена - PostgreSQL
- Все сервисы изолированы в Docker
- Асинхронные задачи выполняются через Celery
- Nginx используется как reverse proxy

## Лицензия:

Проект распространяется под [лицензией MIT](LICENSE).