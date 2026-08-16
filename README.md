# Дипломный проект. Задание 3: UI Stellar Burgers

UI-автотесты построены по Page Object и проверяют конструктор, модальные окна,
счётчики ингредиентов и ленту заказов в Google Chrome и Mozilla Firefox.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Chrome и Firefox должны быть установлены. Selenium Manager автоматически
подберёт совместимые драйверы.

## Запуск

Оба браузера в headless-режиме:

```bash
pytest
```

Только один браузер:

```bash
pytest --browser=chrome
pytest --browser=firefox
```

Запуск с видимым окном браузера:

```bash
pytest --browser=chrome --headed
```

Просмотр Allure-отчёта:

```bash
allure serve allure-results
```
