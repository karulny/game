![Python](https://img.shields.io/badge/python-3.14-blue.svg)


# О проекте

## *Про структуру*:
```
RTS_Prototype/
├── main.py                   # Главный файл запуска и окно Arcade
├── config.py                 # Константы (размер экрана, пути, размеры тайлов)
├── resources                  # Карта моделки и тд.
├── models/                   # ПАПКА: Все данные и игровое состояние
│   ├── __init__.py
│   ├── game_state.py         # Состояние игры, ресурсы, лимит населения
│   ├── game_map.py           # Наша GameMapModel (загрузка TMX, логическая сетка)
│   └── units_and_buildings.py# Классы UnitModel, BuildingModel (HP, координаты, состояние FSM)
├── views/                    # ПАПКА: Все, что касается отрисовки (UI, карта, спрайты)
│   ├── __init__.py
│   ├── game_view.py          # Основной класс arcade.View (вся отрисовка)
│   ├── ui_panel_view.py      # Классы для отрисовки Верхней и Нижней UI панелей
│   └── minimap_view.py       # Класс для отрисовки мини-карты
└── controllers/              # ПАПКА: Вся логика, ввод игрока, ИИ
    ├── __init__.py
    ├── input_controller.py   # Обработка кликов (выделение, приказы ПКМ) 
    ├── physics_controller.py # Движение, коллизии, физический движок
    └── ai_controller.py      # Реализация агрессивной FSM для ИИ
```
