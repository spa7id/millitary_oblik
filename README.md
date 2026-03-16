# Military Oblik v.1

Система обліку військовослужбовців та підрозділів.

## 📋 Опис

Веб-додаток для управління військовими підрозділами та особовим складом. 
Включає систему контролю доступу, ієрархію підрозділів, облік бійців.

## 🚀 Технології

- Python 3.11+
- Django 5.x
- Bootstrap 4.6
- SB Admin 2 Theme
- PostgreSQL

---

## 📦 Встановлення

### 1. Клонувати репозиторій
```bash
git clone https://github.com/spa7id/millitary_oblik.git
cd millitary_oblik
```

### 2. Встановити PostgreSQL

**Windows:**
1. Завантажити з https://www.postgresql.org/download/windows/
2. Запустити інсталятор
3. Запам'ятати пароль для користувача `postgres`

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 3. Створити базу даних

**Увійти в PostgreSQL:**
```bash
# Linux/Mac
sudo -u postgres psql

# Windows (через pgAdmin або psql в командному рядку)
psql -U postgres
```

**Виконати SQL команди:**
```sql
-- Створити користувача
CREATE USER military_user WITH PASSWORD 'your_strong_password';

-- Створити базу даних
CREATE DATABASE military_oblik_db OWNER military_user;

-- Надати права
GRANT ALL PRIVILEGES ON DATABASE military_oblik_db TO military_user;

-- Вийти
\q
```

### 4. Створити віртуальне середовище

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Встановити залежності
```bash
pip install -r requirements.txt
```

### 6. Налаштувати змінні оточення

**Скопіювати файл-приклад:**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**Відредагувати `.env` та встановити:**
```env
SECRET_KEY=your-generated-secret-key
DEBUG=True
DATABASE_URL=postgresql://military_user:your_strong_password@localhost:5432/military_oblik_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

**📋 Детальний опис всіх змінних:** [.env.example](.env.example)

**⚠️ ВАЖЛИВО:** 
- Ніколи не комітьте файл `.env` в Git!
- Для production згенеруйте новий `SECRET_KEY`
- Встановіть `DEBUG=False` для production

**Згенерувати унікальний SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 7. Виконати міграції
```bash
python manage.py migrate
```

### 8. Створити суперкористувача
```bash
python manage.py createsuperuser
```

**Введіть:**
- Username (ім'я користувача)
- Email (опціонально)
- Password (пароль)

### 9. Запустити сервер
```bash
python manage.py runserver
```

### 10. Відкрити в браузері

- **Основний додаток:** http://localhost:8000
- **Адмін-панель:** http://localhost:8000/admin

---

## 🔐 Конфігурація змінних оточення

Проект використовує PostgreSQL базу даних та змінні оточення для налаштування.

### Основні змінні:

| Змінна | Опис | Приклад | Обов'язкова |
|--------|------|---------|-------------|
| `SECRET_KEY` | Секретний ключ Django | `django-insecure-...` | ✅ Так |
| `DEBUG` | Режим налагодження | `True` / `False` | ✅ Так |
| `DATABASE_URL` | URL PostgreSQL БД | `postgresql://user:pass@localhost:5432/dbname` | ✅ Так |
| `ALLOWED_HOSTS` | Дозволені хости | `localhost,127.0.0.1` | ✅ Так |

### Налаштування для різних середовищ:

**🔧 Розробка (Development):**
```env
DEBUG=True
DATABASE_URL=postgresql://military_user:dev_password@localhost:5432/military_oblik_dev
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**🚀 Production:**
```env
DEBUG=False
DATABASE_URL=postgresql://prod_user:strong_password@prod-server:5432/military_oblik_prod
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECRET_KEY=your-very-long-production-secret-key
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**📚 Повний список змінних:** [.env.example](.env.example)

---

## 🔑 Функціонал

- ✅ Облік військовослужбовців
- ✅ Ієрархія підрозділів (батальйон → рота → взвод → відділення)
- ✅ Система контролю доступу (офіцери/солдати)
- ✅ Перевірка прав доступу (403 Forbidden)
- ✅ Детальні сторінки бійців і підрозділів
- ✅ Breadcrumbs навігація
- ✅ Форми створення/редагування з валідацією
- ✅ Пагінація списків
- ✅ Сторінки помилок (404, 403, 500)
- ✅ Bootstrap 4.6 дизайн (SB Admin 2)

---

## 📂 Структура проекту
```
millitary_oblik/          # Корінь репозиторію
├── military_oblik/       # Налаштування Django
│   ├── settings.py       # Конфігурація
│   ├── urls.py           # URL маршрути
│   └── wsgi.py           # WSGI
├── oblik/                # Основний додаток
│   ├── models.py         # Моделі БД
│   ├── views.py          # Views з контролем доступу
│   ├── forms.py          # Форми
│   ├── urls.py           # URL додатку
│   └── templates/        # HTML шаблони
├── templates/            # Глобальні шаблони
│   ├── base.html
│   ├── 404.html
│   └── 403.html
├── static/               # Статичні файли
├── manage.py             # Django CLI
├── requirements.txt      # Залежності
├── .env.example          # Приклад .env
├── .gitignore
└── README.md             # Ця документація
```

---

## 🔐 Безпека

**Перед розгортанням на production:**

1. ✅ Згенерувати унікальний `SECRET_KEY`
2. ✅ Встановити `DEBUG = False`
3. ✅ Налаштувати `ALLOWED_HOSTS`
4. ✅ Використати PostgreSQL
5. ✅ Увімкнути HTTPS
6. ✅ Налаштувати безпечні cookies
7. ✅ Перевірити що `.env` в `.gitignore`

---
