# -*- coding: utf-8 -*-
# main.py — ПК-версия комплекса PHONON-CORE v1.0 [ЧАСТЬ 1 - ТОЧНЫЙ ФИКС ГЕОМЕТРИИ]
import math
import random
import threading
import time
import os
from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Point, Line
from kivy.uix.widget import Widget
import phonon_engine

Window.size = (360, 640)
DB_PATH = r"D:\Phonon_Core_App\core_knowledge.txt"

class Phonon3DCanvas(Widget):
    def __init__(self, **kwargs):
        super(Phonon3DCanvas, self).__init__(**kwargs)
        self.angle_y = 45.0
        self.cube_nodes = []
        for x in range(-3, 4):
            for y in range(-3, 4):
                for z in range(-3, 4):
                    try:
                        w = int(abs(math.sin(x)*10) + abs(math.cos(y)*10) + z*5)
                        dig_root = phonon_engine.q_digital_root(w)
                    except: 
                        dig_root = 1
                    self.cube_nodes.append((x * 1.2, y * 1.2, z * 1.2, dig_root))
        Clock.schedule_interval(self.update_screen, 1.0 / 60.0)

    def update_screen(self, dt):
        self.angle_y += 0.008
        self.canvas.clear()
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        scale = 30.0
        with self.canvas:
            # ИСПРАВЛЕНИЕ: Жёсткое извлечение цифр по индексам элементов кортежа
            for node in self.cube_nodes:
                nx = node[0]
                ny = node[1]
                nz = node[2]
                dig_root = node[3]
                
                x_rot = nx * math.cos(self.angle_y) - nz * math.sin(self.angle_y)
                y_rot = ny
                screen_x = cx + x_rot * scale
                screen_y = cy + y_rot * scale
                
                if dig_root == 9:
                    Color(0.0, 1.0, 1.0, 0.9)
                    Point(points=[screen_x, screen_y], pointsize=4.5)
                elif dig_root == 3 or dig_root == 6:
                    Color(0.5, 0.0, 1.0, 0.7)
                    Point(points=[screen_x, screen_y], pointsize=3.0)
                else:
                    Color(0.0, 0.7, 1.0, 0.4)
                    Point(points=[screen_x, screen_y], pointsize=1.8)
            
            with phonon_engine.print_lock:
                if hasattr(phonon_engine, 'live_thoughts_3d') and phonon_engine.live_thoughts_3d:
                    for laser in phonon_engine.live_thoughts_3d:
                        try:
                            xa = laser.get("xa", 0.0)
                            ya = laser.get("ya", 0.0)
                            za = laser.get("za", 0.0)
                            xb = laser.get("xb", 0.0)
                            yb = laser.get("yb", 0.0)
                            zb = laser.get("zb", 0.0)
                            r_c = laser.get("color", (0.0, 0.4, 1.0))
                            
                            xa_r = xa * math.cos(self.angle_y) - za * math.sin(self.angle_y)
                            xb_r = xb * math.cos(self.angle_y) - zb * math.sin(self.angle_y)
                            sa_x, sa_y = cx + xa_r * scale, cy + ya * scale
                            sb_x, sb_y = cx + xb_r * scale, cy + yb * scale
                            
                            Color(r_c, r_c, r_c, 1.0)
                            l_width = 2.5 if r_c != (0.0, 0.4, 1.0) else 1.2
                            Line(points=[sa_x, sa_y, sb_x, sb_y], width=l_width)
                        except Exception:
                            pass
class PhononApp(App):
    def build(self):
        self.title = "PHONON-CORE v1.0"
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.status_label = Label(text="PHONON-CORE v1.0\n[МАТРИЦА КВАНТОВЫХ КУБИТОВ]", size_hint_y=0.1, color=(0, 1, 1, 1), bold=True, halign="center")
        main_layout.add_widget(self.status_label)
        
        self.canvas_3d = Phonon3DCanvas(size_hint_y=0.4)
        main_layout.add_widget(self.canvas_3d)
        
        self.scroll_view = ScrollView(size_hint_y=0.3)
        self.console_text = Label(
            text="[СИСТЕМА]: Инициализация автообучения матрицы...\n[СИСТЕМА]: Память резонатора синхронизирована.\n[АРКП]: Готов к запуску фононного импульса...", 
            color=(0, 1, 0, 1), 
            size_hint_y=None, 
            halign="left", 
            valign="top", 
            font_size="13sp"
        )
        self.console_text.bind(texture_size=self.console_text.setter('size'))
        self.console_text.bind(width=lambda img, val: setattr(self.console_text, 'text_size', (val, None)))
        self.scroll_view.add_widget(self.console_text)
        main_layout.add_widget(self.scroll_view)
        
        # Многострочное текстовое поле для загрузки больших блоков книг
        self.input_field = TextInput(hint_text="Скопируйте текст книги и нажмите 'ВСТАВИТЬ КНИГУ'...", multiline=True, size_hint_y=0.08, background_color=(0.1, 0.1, 0.1, 1), foreground_color=(1, 1, 1, 1), cursor_color=(0, 1, 1, 1))
        main_layout.add_widget(self.input_field)
        
        btn_layout = BoxLayout(orientation='vertical', size_hint_y=0.12, spacing=5)
        self.btn_book = Button(text="ВСТАВИТЬ КНИГУ", background_color=(0, 0.5, 0.2, 1), color=(1, 1, 1, 1), bold=True)
        self.btn_book.bind(on_release=self.load_book_data)
        
        self.btn_pulse = Button(text="ЗАПУСТИТЬ ФОНОННЫЙ ИМПУЛЬС", background_color=(0, 0.3, 0.6, 1), color=(1, 1, 1, 1), bold=True)
        self.btn_pulse.bind(on_release=self.trigger_pulse)
        
        btn_layout.add_widget(self.btn_book); btn_layout.add_widget(self.btn_pulse)
        main_layout.add_widget(btn_layout)
        
        try:
            phonon_engine.init_paths(r"D:\Phonon_Core_App")
            phonon_engine.PHONON_LOG = DB_PATH
            phonon_engine._phonon_learner()
            phonon_engine.load_phonon_brain()
        except Exception as e: 
            self.console_text.text += f"\n[ОШИБКА ДВИЖКА]: {str(e)}"
        return main_layout

    def load_book_data(self, instance):
        """ БЕЗОПАСНЫЙ ИМПОРТ: Вызов буфера Windows строго по клику, защищающий от вылета при старте """
        try:
            from kivy.core.clipboard import Clipboard
            clipboard_data = Clipboard.paste()
            if clipboard_data and clipboard_data.strip():
                self.input_field.text = clipboard_data
                self.console_text.text += f"\n[СИСТЕМА]: Данные из буфера Windows ({len(clipboard_data)} симв.) перенесены в поле ввода."
            else:
                self.console_text.text += "\n[ОШИБКА]: Буфер обмена ОС пуст! Сначала скопируйте текст книги."
        except Exception as e:
            self.console_text.text += f"\n[ОШИБКА ИМПОРТА]: {str(e)}"

    def trigger_pulse(self, instance):
        orig_text = self.input_field.text.strip()
        if orig_text:
            preview_text = orig_text[:100] + "..." if len(orig_text) > 100 else orig_text
            self.console_text.text += f"\n\n[ВВОД]: ОПЕРАТОР: {preview_text}"
            
            full_phrase = phonon_engine.generate_matrix_response(orig_text)
            
            try:
                os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
                with open(DB_PATH, "a", encoding="utf-8") as f: 
                    f.write(f"\n=== ИМПУЛЬС СИНХРОНИЗАЦИИ ===\n[ВВОД]: {orig_text}\n[ОТВЕТ АРКП]: {full_phrase}\n")
                    f.flush()
            except Exception as e: 
                self.console_text.text += f"\n[ПРЕДУПРЕЖДЕНИЕ ПАМЯТИ]: {str(e)}"
            
            with phonon_engine.print_lock:
                phonon_engine.live_thoughts_3d.clear()
            
            self.laser_words = full_phrase.split()
            self.current_laser_idx = 0
            
            Clock.schedule_interval(self.animate_cube_thought, 0.45)
            
            self.update_console_ui(orig_text, full_phrase)
            self.input_field.text = ""
        else: 
            self.console_text.text += "\n[ОШИБКА] Строка импульса пуста!"

    def animate_cube_thought(self, dt):
        if self.current_laser_idx >= len(self.laser_words) - 1:
            return False
            
        w1 = self.laser_words[self.current_laser_idx]
        w2 = self.laser_words[self.current_laser_idx + 1]
        
        ww1 = sum(phonon_engine.W_BUKVICA.get(l, 1) for l in w1) or 9
        ww2 = sum(phonon_engine.W_BUKVICA.get(l, 1) for l in w2) or 9
        
        xa = float(((ww1 % 7) - 3) * 1.2)
        ya = float(((phonon_engine.q_digital_root(ww1) % 7) - 3) * 1.2)
        za = float(((len(w1) % 7) - 3) * 1.2)
        
        xb = float(((ww2 % 7) - 3) * 1.2)
        yb = float(((phonon_engine.q_digital_root(ww2) % 7) - 3) * 1.2)
        zb = float(((len(w2) % 7) - 3) * 1.2)
        
        root_b = phonon_engine.q_digital_root(ww2)
        if root_b == 9:
            color_vector = (0.0, 1.0, 1.0)
        elif root_b == 3 or root_b == 6:
            color_vector = (0.5, 0.0, 1.0)
        else:
            color_vector = (0.0, 0.4, 1.0)
        
        with phonon_engine.print_lock:
            phonon_engine.live_thoughts_3d.append({
                "xa": xa, "ya": ya, "za": za,
                "xb": xb, "yb": yb, "zb": zb,
                "color": color_vector,
                "time": time.time()
            })
            
        self.current_laser_idx += 1
        return True

    def update_console_ui(self, orig_text, full_phrase):
        self.console_text.text += f"\n[MATРИЦА ОТВЕТ]: {full_phrase}"
        self.scroll_view.scroll_y = 0

if __name__ == '__main__':
    PhononApp().run()
ы
