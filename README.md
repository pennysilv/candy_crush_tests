# 🎮 Candy Crush Tests  
### Python + Appium + pytest

Простой набор автотестов для мобильной игры (Unity и другие движки).  
Работаем **по координатам** — в играх XPath почти не помогает.

---

## 🔎 Что внутри

- 4 типа тестов: **стабильность**, **взаимодействие**, **производительность**, **визуальная проверка**
- **Page Object Model (POM)** — экраны вынесены в отдельные файлы
- **Скриншоты и HTML-отчёт** после прогона
- **Реалистичные сценарии**: тап, свайп, пинч, выход в фон и обратно

---

## 🏗️ Структура проекта

```text
candy_crush_tests/
├─ pages/                # экраны (POM)
│  ├─ base_page.py
│  ├─ main_menu_page.py
│  ├─ game_board_page.py
│  └─ level_map_page.py
├─ tests/                # тесты
│  ├─ test_app_stability.py
│  ├─ test_screen_interactions.py
│  ├─ test_performance.py
│  └─ test_visual_validation.py
├─ utils/                # хелперы
│  └─ helpers.py
├─ config/               # настройки
│  └─ settings.py
├─ data/
│  └─ test_data.json     # координаты и данные
├─ reports/              # отчёты и скрины
├─ conftest.py
├─ requirements.txt
└─ run_tests.py
