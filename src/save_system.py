import sqlite3
import json
import os
import sys


class SaveSystem:
    def __init__(self):
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.db_path = os.path.join(app_dir, "saves", "game.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS saves
                       (
                           id             INTEGER PRIMARY KEY AUTOINCREMENT,
                           save_name      TEXT NOT NULL,
                           money          INTEGER,
                           units_data     TEXT,
                           buildings_data TEXT,
                           camera_x       REAL,
                           camera_y       REAL,
                           save_date      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )
                       """)

        conn.commit()
        conn.close()

    def save_game(self, game_state, camera_pos, save_name="autosave"):
        units_data = []
        for unit in game_state.units:
            units_data.append({
                'x': unit.x,
                'y': unit.y,
                'team': unit.team,
                'hp': unit.hp,
                'state': unit.state.value
            })

        buildings_data = []
        for building in game_state.buildings:
            buildings_data.append({
                'grid_x': building.grid_x,
                'grid_y': building.grid_y,
                'type': building.type,
                'owner': building.owner,
                'hp': building.hp,
                'spawn_cooldown': building.spawn_cooldown
            })

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
                       INSERT INTO saves (save_name, money, units_data, buildings_data, camera_x, camera_y)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (
                           save_name,
                           game_state.money,
                           json.dumps(units_data),
                           json.dumps(buildings_data),
                           camera_pos[0],
                           camera_pos[1]
                       ))

        conn.commit()
        conn.close()
        print(f"Игра сохранена: {save_name}")

    def load_game(self, save_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if save_id:
            cursor.execute("SELECT * FROM saves WHERE id = ?", (save_id,))
        else:
            cursor.execute("SELECT * FROM saves ORDER BY save_date DESC LIMIT 1")

        save_data = cursor.fetchone()
        conn.close()

        if not save_data:
            print("Сохранение не найдено")
            return None

        return {
            'id': save_data[0],
            'save_name': save_data[1],
            'money': save_data[2],
            'units_data': json.loads(save_data[3]),
            'buildings_data': json.loads(save_data[4]),
            'camera_x': save_data[5],
            'camera_y': save_data[6],
            'save_date': save_data[7]
        }

    def get_all_saves(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, save_name, save_date FROM saves ORDER BY save_date DESC")
        saves = cursor.fetchall()
        conn.close()

        return saves

    def delete_save(self, save_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM saves WHERE id = ?", (save_id,))
        conn.commit()
        conn.close()
        print(f"Сохранение {save_id} удалено")