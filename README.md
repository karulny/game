# RTS Prototype

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Arcade](https://img.shields.io/badge/arcade-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Простая RTS-стратегия на Python с Arcade.

## 🚀 Быстрый старт 

```bash
pip install -r requirements.txt
cd src
python main.py
```

## 🎮 Управление

| Действие | Клавиша |
|----------|---------|
| Выбрать юнита | ЛКМ |
| Приказ/Атака | ПКМ |
| Спавн юнита | ЛКМ по зданию |
| Камера | WASD / края экрана |
| Зум | Колесико мыши |
| Пауза | ESC |
| Сохранить | F5 |
| Загрузить | F9 |

## 📦 Структура

```
RTS_Prototype/
├── assets/          # Графика, карты
├── src/             # Код игры
│   ├── models/      # Логика (unit.py, building.py)
│   ├── views/       # Отображение (game_view.py)
│   └── controllers/ # Ввод (input_controller.py)
└── saves/           # Сохранения (SQLite)
```

## 📄 Лицензия

MIT - [@karulny](https://github.com/karulny)
