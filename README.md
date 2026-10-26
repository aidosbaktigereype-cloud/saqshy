# Saqshy — сайт и CRM для установки охранных систем

Лендинги услуг (AJAX, видеонаблюдение, СКУД, охранная сигнализация, слаботочные системы) на трёх языках
(русский, казахский, английский), приём заявок, собственная CRM для сотрудников и Telegram-бот.

**Стек:** Python 3.13, Django 5.2 LTS, django-modeltranslation (контент на 3 языках), django-unfold (интерфейс CRM),
SQLite локально / PostgreSQL в продакшене, Docker + Caddy (HTTPS).

> «Saqshy» — рабочее название. Бренд, телефоны, WhatsApp и Telegram задаются в `.env`, код менять не нужно.

---

## Быстрый старт (Windows, локально)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env          # для локального запуска хватит DJANGO_DEBUG=1
python manage.py migrate
python manage.py compile_translations
python manage.py seed_demo       # демо-услуги, пакеты, кейсы и страницы на 3 языках
python manage.py setup_roles     # роли «Менеджер» и «Контент-менеджер»
python manage.py createsuperuser # повторите для второго админа
python manage.py runserver
```

- Сайт: http://127.0.0.1:8000 (казахский — `/kk/`, английский — `/en/`)
- CRM: http://127.0.0.1:8000/crm/

macOS / Linux — то же самое, только `source .venv/bin/activate` и `cp`.

Тесты: `python manage.py test`

## Структура

| Папка | Что внутри |
| --- | --- |
| `config/` | настройки (`settings.py` читает всё из `.env`), URL-ы |
| `core/` | главная, текстовые страницы, SEO (sitemap, robots, JSON-LD), иконки, демо-данные |
| `services/` | услуги, пакеты с ценами, вопросы и ответы |
| `cases/` | кейсы (портфолио) |
| `crm/` | заявки, история, сотрудники, приём заявок `/api/leads/`, Telegram-бот |
| `templates/` | HTML-шаблоны, `partials/` — общие блоки (шапка, форма, CTA) |
| `static/` | `css/site.css` — дизайн-система (цвета в `:root`), `js/site.js` |
| `locale/` | переводы интерфейса (`.po`) для kk и en |
| `deploy/` | Caddyfile, entrypoint, скрипт бэкапа |

### Как это работает

- **Языки.** Русский — без префикса, `/kk/` и `/en/` — с префиксом, у каждой страницы hreflang и canonical.
  Тексты услуг, кейсов и страниц переводятся в CRM (у каждого поля вкладки RU / KK / EN).
  Надписи интерфейса — в `locale/*/LC_MESSAGES/django.po`; после правки: `python manage.py compile_translations`.
- **Заявки.** Формы отправляют данные на `/api/leads/`: проверка телефона, согласие на обработку ПДн,
  скрытое поле-ловушка для ботов, лимит 5 заявок с IP за 10 минут. В заявке сохраняются страница, язык,
  UTM-метки, gclid/yclid и ClientID Метрики — для оценки рекламы и будущих офлайн-конверсий.
- **CRM** (`/crm/`). Этапы: Новая → В работе → Замер → КП → Монтаж → Завершена / Отказ.
  Каждая смена этапа, ответственного и комментарий пишутся в историю. Фильтры по этапу, каналу, услуге, дате.
- **Роли.** Суперпользователь — полный доступ. «Менеджер» — заявки. «Контент-менеджер» — услуги, кейсы, страницы.
  Сотруднику нужно включить «Статус персонала» и выбрать группу.

## Telegram-бот

1. Создайте бота у [@BotFather](https://t.me/BotFather), токен — в `TELEGRAM_BOT_TOKEN`.
2. Создайте рабочую группу, добавьте туда бота и напишите в группе `/start` — бот ответит ID чата.
   Впишите его в `TELEGRAM_CHAT_ID`.
3. Каждый сотрудник берёт свой код в CRM (Сотрудники → профиль → блок Telegram) и пишет боту `/link КОД`.
4. Запуск:
   - локально: `python manage.py telegram_poll` (держите открытым в отдельном терминале);
   - на сервере: заполните `TELEGRAM_WEBHOOK_SECRET` и выполните `python manage.py telegram_setwebhook`.

Новая заявка приходит в группу карточкой с кнопками «✋ Беру», этапы, WhatsApp. Команды: `/new` — новые без
ответственного, `/today` — мои открытые. Бот отвечает только привязанным сотрудникам.

### Напоминания

У заявки есть поле «Следующий шаг». Когда время наступает, бот пишет ответственному в личку
(или в рабочую группу, если Telegram не привязан). Локально напоминания отправляет `telegram_poll`,
на сервере — cron раз в минуту:
`* * * * * cd /opt/saqshy && docker compose exec -T web python manage.py send_reminders`

## CRM

- **Сводка** (`/crm/`) — заявки за день/неделю/месяц, источники, воронка, конверсия, выручка, просроченные шаги.
- **Доска** (`/crm/crm/lead/board/`) — канбан по этапам, карточки перетаскиваются мышью; фильтр «Мои».
- **Заявки** — список с фильтрами, карточка с историей, комментариями и перепиской WhatsApp.
- **2FA.** Суперпользователь при первом входе настраивает код из приложения (Google Authenticator,
  Яндекс Ключ). Потеряли телефон — `python manage.py reset_2fa ЛОГИН`. Отключить требование — `ADMIN_2FA_REQUIRED=0`.

## WhatsApp Cloud API

Входящие сообщения клиентов в WhatsApp становятся заявками (или добавляются в переписку открытой заявки),
приходят в Telegram-группу, а менеджер отвечает **реплаем на сообщение бота** — ответ уходит клиенту в WhatsApp.
Ответить можно и из карточки заявки в CRM. По правилам WhatsApp свободный ответ возможен в течение 24 часов
после последнего сообщения клиента.

Настройка (делается в кабинете Meta владельцем бизнеса):
1. [developers.facebook.com](https://developers.facebook.com/) → Create App → тип **Business** → добавить продукт **WhatsApp**.
2. WhatsApp → API Setup: скопируйте **Phone number ID** → `WHATSAPP_PHONE_NUMBER_ID` и временный **Access token** →
   `WHATSAPP_TOKEN` (живёт 24 часа; для постоянной работы создайте System User в Business Settings и выпустите
   постоянный токен с правами `whatsapp_business_messaging`).
3. В «To» добавьте свой номер — тестовый номер Meta может писать только в подтверждённые номера (до 5).
4. App Settings → Basic → **App Secret** → `WHATSAPP_APP_SECRET`. Придумайте `WHATSAPP_VERIFY_TOKEN`.
5. WhatsApp → Configuration → Webhook: URL `https://<ваш-домен>/wa/webhook/`, Verify token — из шага 4,
   подпишитесь на поле **messages**.
6. Для боевого номера компании пройдите верификацию бизнеса и добавьте номер в WhatsApp Manager.

## Публичный адрес для тестов (Cloudflare Tunnel)

Нужен, чтобы открыть сайт с телефона по HTTPS и подключить вебхук WhatsApp без сервера.

```powershell
winget install --id Cloudflare.cloudflared
.\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
cloudflared tunnel --url http://localhost:8000
```

`cloudflared` выдаст адрес `https://….trycloudflare.com` с сертификатом. Он меняется при каждом запуске —
обновите `SITE_URL` в `.env` и URL вебхука в кабинете Meta. В `.env` разрешите эти адреса:
`DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,.trycloudflare.com` и `DJANGO_CSRF_TRUSTED_ORIGINS=https://*.trycloudflare.com`.
Это только для тестов: реальных клиентов принимайте на сервере в Казахстане.

## Деплой на VPS (PS Cloud, Hoster.kz и т.п.)

Персональные данные клиентов из Казахстана нужно хранить на серверах в РК, поэтому берите VPS в Казахстане.

1. Сервер Ubuntu 22.04+ (1–2 vCPU, 2 ГБ RAM), установите Docker: `curl -fsSL https://get.docker.com | sh`.
2. A-записи домена (`saqshy.kz` и `www`) → IP сервера.
3. На сервере:
   ```bash
   git clone <адрес репозитория> /opt/saqshy && cd /opt/saqshy
   cp .env.example .env && nano .env
   ```
   Обязательно: `DJANGO_DEBUG=0`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS=saqshy.kz,www.saqshy.kz`,
   `DJANGO_CSRF_TRUSTED_ORIGINS=https://saqshy.kz,https://www.saqshy.kz`, `SITE_URL=https://saqshy.kz`,
   `DOMAIN=saqshy.kz`, `POSTGRES_PASSWORD`, контакты.
4. Запуск (Caddy сам получит HTTPS-сертификат):
   ```bash
   docker compose up -d --build
   docker compose exec web python manage.py seed_demo
   docker compose exec web python manage.py createsuperuser
   docker compose exec web python manage.py telegram_setwebhook
   ```
5. Бэкап базы раз в сутки: `crontab -e` → `0 3 * * * cd /opt/saqshy && sh deploy/backup.sh >> backups/backup.log 2>&1`.

Обновление: `git pull && docker compose up -d --build` (миграции применяются автоматически при старте).

## Перед запуском рекламы

- [ ] Заменить демо-цены пакетов на реальные (CRM → Пакеты).
- [ ] Заменить или скрыть демо-кейсы (флаг «Демо-кейс»), загрузить реальные фото.
- [ ] Проверить маркетинговые обещания: «перезвоним за 15 минут», «монтаж за 1 день», гарантия.
- [ ] Вычитать казахские тексты носителем языка.
- [ ] Показать политику конфиденциальности юристу и указать реквизиты в `LEGAL_INFO`.
- [ ] Подключить GA4, Яндекс Метрику, Google Ads (`.env`), настроить цели `lead`, `phone_click`, `whatsapp_click`, `telegram_click`.
- [ ] Добавить сайт в Google Search Console и Яндекс Вебмастер, отправить `/sitemap.xml`.
- [ ] Карточки компании в 2ГИС, Google Business Profile и Яндекс Бизнесе.

## Дальнейшее развитие (заложено в архитектуре)

Флаги в `.env`: `FEATURE_QUIZ`, `FEATURE_CATALOG`, `FEATURE_CART`, `FEATURE_ACCOUNTS`.
Адреса `/catalog/`, `/cart/`, `/checkout/`, `/account/` зарезервированы. Новые модули добавляются как
отдельные Django-приложения (`catalog`, `orders`, `accounts`) рядом с `crm`; в модели `Lead` предусмотрено место для
связей с клиентом и заказом. Если понадобится отдельный API (например, для мобильного приложения) —
Django REST Framework или FastAPI поверх той же базы.
