from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from functools import partial
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class Blocker(Widget):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return True
        return super(Blocker, self).on_touch_down(touch)

class Menu(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.8, 0.8, 0.8, 1)  # gray
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            for child in reversed(self.children):
                if child.dispatch('on_touch_down', touch):
                    return True
            return True
        return super(Menu, self).on_touch_down(touch)

class SensitivityConverter(BoxLayout):
    orientation = 'vertical'
    left_game = StringProperty('standoff')
    right_game = StringProperty('cod')
    conversion_mode = StringProperty('auto')
    sensor_type = StringProperty('sensitivity')
    pubg_accel = BooleanProperty(False)
    standoff_accel = NumericProperty(0.0)
    cod_accel = NumericProperty(0)
    language = StringProperty('ru')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translations = {
            'from_game': {'ru': 'Из игры', 'en': 'From game', 'es': 'De juego', 'pt': 'Do jogo'},
            'to_game': {'ru': 'В игру', 'en': 'To game', 'es': 'A juego', 'pt': 'Para jogo'},
            'accel_title': {'ru': 'Ускорение', 'en': 'Acceleration', 'es': 'Aceleración', 'pt': 'Aceleração'},
            'mode': {'ru': 'Режим:', 'en': 'Mode:', 'es': 'Modo:', 'pt': 'Modo:'},
            'auto': {'ru': 'Автоматически', 'en': 'Automatically', 'es': 'Automáticamente', 'pt': 'Automaticamente'},
            'manual': {'ru': 'Вручную', 'en': 'Manually', 'es': 'Manualmente', 'pt': 'Manualmente'},
            'type': {'ru': 'Тип:', 'en': 'Type:', 'es': 'Tipo:', 'pt': 'Tipo:'},
            'sens': {'ru': 'Сенса', 'en': 'Sens', 'es': 'Sens', 'pt': 'Sens'},
            'gyro': {'ru': 'Гироскоп', 'en': 'Gyroscope', 'es': 'Giroscopio', 'pt': 'Giroscópio'},
            'same_games': {'ru': 'Выберите разные игры для конвертации', 'en': 'Select different games for conversion',
                           'es': 'Seleccione juegos diferentes para la conversión', 'pt': 'Selecione jogos diferentes para conversão'},
            'general_sens': {'ru': 'Чувствит', 'en': 'Sensitivity', 'es': 'Sensibilidad', 'pt': 'Sensibilidade'},
            '3person': {'ru': '3-е лицо', 'en': 'TPP No Scope', 'es': 'PTP sin visor', 'pt': '3ª Pessoa'},
            '1person': {'ru': '1-е лицо', 'en': 'FPP No Scope', 'es': 'PPP sin visor', 'pt': '1ª Pessoa'},
            'col_holo_iron_side': {'ru': 'Кол., голо.,\nмушка, боковой', 'en': 'Red Dot,Holo,...',
                                   'es': 'Punto Rojo,Holo,…', 'pt': 'Ponto Verm., Holo,…'},
            'in_scope': {'ru': 'С прицелом', 'en': 'Scope sensitivity', 'es': 'Sens.de la mirilla', 'pt': 'Telescópica'},
            '3person_dot': {'ru': '3-е лицо', 'en': 'Third person', 'es': 'Tercera persona', 'pt': 'Terceira pessoa'},
            'standard': {'ru': 'Стандарт (руль)', 'en': 'Steering', 'es': 'Dirección', 'pt': 'Condução'},
            'col_holo_aim': {'ru': 'Кол., голо.,\nв реж. прицел.', 'en': 'Red dot,holo,ADS',
                             'es': 'Punto rojo/ holo.,apuntado', 'pt': 'Ponto verm./ holo.,mira'},
            'tactical': {'ru': 'Тактический', 'en': 'Tactical', 'es': 'Mira táctica', 'pt': 'Escopo táctico'},
            'sniper': {'ru': 'Снайперский', 'en': 'Sniper', 'es': 'Mira de precisión', 'pt': 'Escopo do fuzil'},
            'settings': {'ru': 'Настройки', 'en': 'Settings', 'es': 'Ajustes', 'pt': 'Configurações'},
            'language': {'ru': 'Язык', 'en': 'Language', 'es': 'Idioma', 'pt': 'Idioma'},
            'menu': {'ru': 'Меню', 'en': 'Menu', 'es': 'Menú', 'pt': 'Menu'}
        }
        self.langs = {
            'ru': 'Русский',
            'en': 'English',
            'es': 'Español',
            'pt': 'Português (BR)'
        }
        self.setup_conversion_data()
        self.entry_widgets = []
        self.left_widgets = []
        self.create_widgets()

    def get_text(self, key):
        return self.translations.get(key, {}).get(self.language, key)

    def setup_conversion_data(self):
        # (всё остаётся без изменений, таблицы те же)
        self.standoff_pubg_sens = {
            "general_3p": {0: 0, 0.5: 12, 1.0: 12, 2.0: 50, 3.0: 75, 4.0: 100, 5.0: 125, 10.0: 250, 96.0: 2343},
            "general_1p": {0: 0, 0.5: 12, 1.0: 12, 2.0: 50, 3.0: 75, 4.0: 100, 5.0: 125, 10.0: 250, 96: 2343},
            "col": {0: 0, 0.5: 8, 1.0: 6, 2.0: 32, 3.0: 48, 4.0: 64, 5.0: 82, 10.0: 153, 96: 1537},
            "2x": {0: 0, 0.5: 6, 1.0: 13, 2.0: 26, 3.0: 39, 4.0: 52, 5.0: 65, 10.0: 123, 96: 1218},
            "3x": {0: 0, 0.5: 4, 1.0: 8, 2.0: 15, 3.0: 23, 4.0: 31, 5.0: 39, 10.0: 74, 96: 731},
            "4x": {0: 0, 0.5: 3, 1.0: 6, 2.0: 12, 3.0: 18, 4.0: 24, 5.0: 29, 10.0: 55, 96: 543},
            "6x": {0: 0, 0.5: 2, 1.0: 4, 2.0: 7, 3.0: 11, 4.0: 15, 5.0: 19, 10.0: 37, 96: 356},
            "8x": {0: 0, 0.5: 1, 1.0: 3, 2.0: 6, 3.0: 10, 4.0: 13, 5.0: 16, 10.0: 31, 96: 300}
        }
        self.standoff_pubg_gyro = {
            "general_3p": {0: 0, 0.5: 83, 1.0: 167, 1.5: 248, 2.0: 330, 7.77: 1287, 32.7: 5456},
            "general_1p": {0: 0, 0.5: 83, 1.0: 167, 1.5: 248, 2.0: 330, 7.77: 1287, 32.7: 5456},
            "col": {0: 0, 0.5: 128, 1.0: 250, 1.5: 380, 2.0: 400, 7.77: 1973, 32.7: 8347},
            "2x": {0: 0, 0.5: 103, 1.0: 205, 1.5: 305, 2.0: 400, 7.77: 1579, 32.7: 6683},
            "3x": {0: 0, 0.5: 60, 1.0: 125, 1.5: 185, 2.0: 247, 7.77: 963, 32.7: 4446},
            "4x": {0: 0, 0.5: 45, 1.0: 94, 1.5: 140, 2.0: 185, 7.77: 721, 32.7: 3342},
            "6x": {0: 0, 0.5: 30, 1.0: 63, 1.5: 93, 2.0: 124, 7.77: 481, 32.7: 2224},
            "8x": {0: 0, 0.5: 25, 1.0: 51, 1.5: 77, 2.0: 103, 7.77: 400, 32.7: 2550}
        }
        self.standoff_cod_sens = {
            "general_3p": {0: 0, 0.5: 9, 1.0: 18, 2.0: 36, 3.0: 53, 4.0: 71, 5.0: 106, 10.0: 278, 21: 594},
            "general_1p": {0: 0, 0.5: 9, 1.0: 18, 2.0: 36, 3.0: 53, 4.0: 71, 5.0: 106, 10.0: 278, 21: 594},
            "col": {0: 0, 0.5: 28, 1.0: 56, 2.0: 110, 3.0: 165, 4.0: 220, 5.0: 330, 10.0: 880, 21: 1883},
            "2x": {0: 0, 0.5: 36, 1.0: 73, 2.0: 143, 3.0: 215, 4.0: 287, 5.0: 431, 10.0: 1151, 21: 2463},
            "3x": {0: 0, 0.5: 20, 1.0: 39, 2.0: 78, 3.0: 117, 4.0: 156, 5.0: 195, 10.0: 390, 21: 834},
            "4x": {0: 0, 0.5: 14, 1.0: 30, 2.0: 59, 3.0: 89, 4.0: 119, 5.0: 149, 10.0: 297, 21: 635},
            "6x": {0: 0, 0.5: 10, 1.0: 20, 2.0: 40, 3.0: 60, 4.0: 80, 5.0: 100, 10.0: 200, 21: 428},
            "6x_sniper": {0: 0, 0.5: 11, 1.0: 23, 2.0: 43, 3.0: 65, 4.0: 86, 5.0: 108, 10.0: 216, 21: 463},
            "8x": {0: 0, 0.5: 7, 1.0: 14, 2.0: 28, 3.0: 42, 4.0: 56, 5.0: 70, 10.0: 140, 21: 300}
        }
        self.standoff_cod_gyro = {
            "general_3p": {0: 0, 0.6: 31, 2.4: 126, 32.7: 1917},
            "general_1p": {0: 0, 0.6: 31, 2.4: 126, 32.7: 1917},
            "col": {0: 0, 0.6: 31, 2.4: 126, 32.7: 1917},
            "2x": {0: 0, 0.6: 25, 2.4: 108, 32.7: 1473},
            "3x": {0: 0, 0.6: 13, 2.4: 58, 32.7: 791},
            "4x": {0: 0, 0.6: 10, 2.4: 45, 32.7: 614},
            "6x": {0: 0, 0.6: 7, 2.4: 31, 32.7: 423},
            "6x_sniper": {0: 0, 0.6: 8, 2.4: 34, 32.7: 464},
            "8x": {0: 0, 0.6: 5, 2.4: 22, 32.7: 300}
        }
        self.pubg_cod_sens = {
            "general_3p": {0: 0, 12: 9, 25: 18, 50: 36, 75: 53, 100: 71, 125: 106, 150: 142, 200: 213, 250: 278, 300: 320, 2250: 2400},
            "general_1p": {0: 0, 12: 9, 25: 18, 50: 36, 75: 53, 100: 71, 125: 106, 150: 142, 200: 213, 250: 278, 300: 320, 2250: 2400},
            "col": {0: 0, 8: 28, 17: 56, 34: 110, 51: 165, 68: 220, 85: 330, 102: 440, 136: 660, 170: 880, 204: 1056, 1530: 7920},
            "2x": {0: 0, 7: 36, 14: 73, 28: 143, 42: 215, 56: 287, 70: 431, 84: 575, 112: 863, 140: 1151, 168: 1381, 1260: 10357},
            "3x": {0: 0, 4: 20, 8: 39, 16: 78, 24: 117, 32: 156, 40: 234, 48: 312, 64: 468, 80: 585, 96: 702, 720: 5265},
            "4x": {0: 0, 3: 14, 6: 30, 13: 59, 19: 89, 26: 119, 32: 149, 38: 178, 51: 238, 64: 297, 77: 357, 577: 2677},
            "6x": {0: 0, 2: 10, 4: 20, 8: 40, 11: 60, 15: 80, 19: 100, 23: 120, 30: 160, 38: 200, 46: 240, 345: 1942},
            "8x": {0: 0, 2: 7, 3: 14, 7: 28, 10: 42, 13: 56, 17: 70, 20: 84, 26: 112, 33: 140, 40: 168, 300: 1260},
            "6x_sniper": {0: 0, 2: 11, 4: 23, 8: 43, 11: 65, 15: 86, 19: 108, 23: 129, 30: 172, 38: 216, 46: 259, 345: 1942}
        }
        self.pubg_cod_gyro = {
            "general_3p": {0: 0, 400: 126, 5456: 1719},
            "general_1p": {0: 0, 400: 126, 5456: 1719},
            "col": {0: 0, 612: 126, 8347: 1719},
            "2x": {0: 0, 490: 108, 6683: 1473},
            "3x": {0: 0, 326: 58, 4446: 791},
            "4x": {0: 0, 245: 45, 3342: 614},
            "6x": {0: 0, 163: 31, 2224: 423},
            "8x": {0: 0, 122: 22, 1664: 300},
            "6x_sniper": {0: 0, 163: 34, 2224: 464}
        }
        self.standoff_cod_accel = {
            0: 0,
            0.25: 300
        }

    def create_widgets(self):
        # (всё без изменений до setup_acceleration_ui)
        top_frame = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(120))
        self.add_widget(top_frame)
        left_game_frame = BoxLayout(orientation='vertical')
        top_frame.add_widget(left_game_frame)
        self.left_title = Label(text=self.get_text("from_game"), size_hint_y=None, height=dp(30), halign='center', valign='middle')
        self.left_title.bind(size=self.left_title.setter('text_size'))
        left_game_frame.add_widget(self.left_title)
        games = {'Standoff 2': 'standoff', 'PUBG Mobile': 'pubg', 'CoD Mobile': 'cod'}
        self.left_spinner = Spinner(
            text='Standoff 2',
            values=list(games.keys()),
            size_hint_y=None,
            height=dp(44)
        )
        self.left_spinner.bind(text=lambda instance, value: self.on_left_game_change(value))
        left_game_frame.add_widget(self.left_spinner)
        right_game_frame = BoxLayout(orientation='vertical')
        top_frame.add_widget(right_game_frame)
        self.right_title = Label(text=self.get_text("to_game"), size_hint_y=None, height=dp(30), halign='center', valign='middle')
        self.right_title.bind(size=self.right_title.setter('text_size'))
        right_game_frame.add_widget(self.right_title)
        self.right_spinner = Spinner(
            text='CoD Mobile',
            values=list(games.keys()),
            size_hint_y=None,
            height=dp(44)
        )
        self.right_spinner.bind(text=lambda instance, value: self.on_right_game_change(value))
        right_game_frame.add_widget(self.right_spinner)
        accel_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(60))
        self.add_widget(accel_frame)
        self.accel_title = Label(text=self.get_text("accel_title"), size_hint_y=None, height=dp(30))
        accel_frame.add_widget(self.accel_title)
        self.accel_inner_frame = BoxLayout(orientation='horizontal')
        accel_frame.add_widget(self.accel_inner_frame)
        settings_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120))
        self.add_widget(settings_frame)
        mode_frame = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        settings_frame.add_widget(mode_frame)
        self.mode_label = Label(text=self.get_text("mode"), size_hint_x=None, width=dp(60))
        mode_frame.add_widget(self.mode_label)
        self.mode_buttons = {}
        for mode, text_key in [('auto', 'auto'), ('manual', 'manual')]:
            btn = ToggleButton(text=self.get_text(text_key), group='mode', state='down' if mode == 'auto' else 'normal')
            btn.mode_id = mode
            btn.bind(state=self.on_mode_change)
            mode_frame.add_widget(btn)
            self.mode_buttons[mode] = btn
        sensor_frame = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60))
        settings_frame.add_widget(sensor_frame)
        self.type_label = Label(text=self.get_text("type"), size_hint_x=None, width=dp(60))
        sensor_frame.add_widget(self.type_label)
        self.sensor_buttons = {}
        for sensor, text_key in [('sensitivity', 'sens'), ('gyroscope', 'gyro')]:
            btn = ToggleButton(text=self.get_text(text_key), group='sensor', state='down' if sensor == 'sensitivity' else 'normal')
            btn.sensor_id = sensor
            btn.bind(state=self.on_sensor_change)
            sensor_frame.add_widget(btn)
            self.sensor_buttons[sensor] = btn
        self.table_scroll = ScrollView()
        self.add_widget(self.table_scroll)
        self.table_frame = GridLayout(cols=4, spacing=dp(5), size_hint_y=None, row_force_default=True, row_default_height=dp(40))
        self.table_frame.bind(minimum_height=self.table_frame.setter('height'))
        self.table_scroll.add_widget(self.table_frame)
        self.update_ui()

    def setup_acceleration_ui(self):
        left_game = self.left_game
        right_game = self.right_game
        self.accel_inner_frame.clear_widgets()

        if 'pubg' in [left_game, right_game]:
            # Всегда показываем чекбокс PUBG первым, а второе поле — всегда readonly + серое
            self.accel_inner_frame.add_widget(Label(text="PUBG", size_hint_x=None, width=dp(100)))
            cb = CheckBox(active=self.pubg_accel)
            self.accel_inner_frame.add_widget(cb)
            cb.bind(active=self.update_acceleration)
            self.pubg_checkbox = cb

            other_game = 'standoff' if 'standoff' in [left_game, right_game] else 'cod'

            self.accel_inner_frame.add_widget(Label(text=other_game.capitalize() if other_game == 'standoff' else "CoD",
                                                    size_hint_x=None, width=dp(100)))

            common_kwargs = dict(
                multiline=False,
                height=dp(40),
                size_hint_y=None,
                padding=[dp(5), dp(5), dp(5), dp(5)],
                font_size=dp(14),
                readonly=True,
                background_color=[0.8, 0.8, 0.8, 1],
                foreground_color=[0, 0, 0, 1]
            )

            if other_game == 'standoff':
                text = f"{self.standoff_accel:.2f}" if self.standoff_accel != 0.0 else ''
                self.standoff_accel_input = TextInput(text=text, input_filter='float', **common_kwargs)
                self.accel_inner_frame.add_widget(self.standoff_accel_input)
            else:  # cod
                text = str(self.cod_accel) if self.cod_accel != 0 else ''
                self.cod_accel_input = TextInput(text=text, input_filter='int', **common_kwargs)
                self.accel_inner_frame.add_widget(self.cod_accel_input)

        elif left_game == 'standoff' and right_game == 'cod':
            self.accel_inner_frame.add_widget(Label(text="Standoff", size_hint_x=None, width=dp(100)))
            self.standoff_accel_input = TextInput(text='', multiline=False, input_filter='float', height=dp(40), size_hint_y=None,
                                                  padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14))
            self.accel_inner_frame.add_widget(self.standoff_accel_input)
            self.standoff_accel_input.bind(text=self.on_standoff_accel_text)
            self.accel_inner_frame.add_widget(Label(text="CoD", size_hint_x=None, width=dp(100)))
            self.cod_accel_input = TextInput(text='', multiline=False, readonly=True, input_filter='int', height=dp(40),
                                             size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14),
                                             background_color=[0.8, 0.8, 0.8, 1], foreground_color=[0, 0, 0, 1])
            self.accel_inner_frame.add_widget(self.cod_accel_input)

        elif left_game == 'cod' and right_game == 'standoff':
            self.accel_inner_frame.add_widget(Label(text="CoD", size_hint_x=None, width=dp(100)))
            self.cod_accel_input = TextInput(text='', multiline=False, input_filter='int', height=dp(40), size_hint_y=None,
                                             padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14))
            self.accel_inner_frame.add_widget(self.cod_accel_input)
            self.cod_accel_input.bind(text=self.on_cod_accel_text)
            self.accel_inner_frame.add_widget(Label(text="Standoff", size_hint_x=None, width=dp(100)))
            self.standoff_accel_input = TextInput(text='', multiline=False, readonly=True, input_filter='float', height=dp(40),
                                                  size_hint_y=None, padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14),
                                                  background_color=[0.8, 0.8, 0.8, 1], foreground_color=[0, 0, 0, 1])
            self.accel_inner_frame.add_widget(self.standoff_accel_input)

        self.update_accel_inputs()

    def on_standoff_accel_text(self, instance, value):
        if value == '':
            self.standoff_accel = 0.0
        else:
            try:
                self.standoff_accel = float(value)
            except ValueError:
                self.standoff_accel = 0.0
                instance.text = ''
        self.update_standoff_cod_accel()
        self.update_accel_inputs()

    def on_cod_accel_text(self, instance, value):
        if value == '':
            self.cod_accel = 0
        else:
            try:
                self.cod_accel = int(value)
            except ValueError:
                self.cod_accel = 0
                instance.text = ''
        self.update_standoff_cod_accel()
        self.update_accel_inputs()

    def update_accel_inputs(self):
        if hasattr(self, 'standoff_accel_input') and getattr(self.standoff_accel_input, 'readonly', False):
            self.standoff_accel_input.text = f"{self.standoff_accel:.2f}" if self.standoff_accel != 0.0 else ''
        if hasattr(self, 'cod_accel_input') and getattr(self.cod_accel_input, 'readonly', False):
            self.cod_accel_input.text = str(self.cod_accel) if self.cod_accel != 0 else ''

    def update_acceleration(self, instance, active):
        self.pubg_accel = active
        if active:
            if self.left_game == 'pubg' and self.right_game == 'standoff':
                self.standoff_accel = 0.42
            elif self.left_game == 'standoff' and self.right_game == 'pubg':
                self.standoff_accel = 0.42
            elif self.left_game == 'pubg' and self.right_game == 'cod':
                self.cod_accel = 300
            elif self.left_game == 'cod' and self.right_game == 'pubg':
                self.cod_accel = 300
        else:
            self.standoff_accel = 0.0
            self.cod_accel = 0
        self.update_accel_inputs()

    def update_standoff_cod_accel(self):
        if self.left_game == 'standoff' and self.right_game == 'cod':
            standoff_val = self.standoff_accel
            keys = sorted(self.standoff_cod_accel.keys())
            if standoff_val <= keys[0]:
                self.cod_accel = self.standoff_cod_accel[keys[0]]
            elif standoff_val >= keys[-1]:
                self.cod_accel = self.standoff_cod_accel[keys[-1]]
            else:
                for i in range(len(keys)-1):
                    if keys[i] <= standoff_val <= keys[i+1]:
                        ratio = (standoff_val - keys[i]) / (keys[i+1] - keys[i])
                        cod_value = self.standoff_cod_accel[keys[i]] + ratio * (self.standoff_cod_accel[keys[i+1]] - self.standoff_cod_accel[keys[i]])
                        self.cod_accel = int(round(cod_value))
                        break
        elif self.left_game == 'cod' and self.right_game == 'standoff':
            cod_val = self.cod_accel
            values = sorted(self.standoff_cod_accel.items(), key=lambda x: x[1])
            if cod_val <= values[0][1]:
                self.standoff_accel = values[0][0]
            elif cod_val >= values[-1][1]:
                self.standoff_accel = values[-1][0]
            else:
                for i in range(len(values)-1):
                    if values[i][1] <= cod_val <= values[i+1][1]:
                        ratio = (cod_val - values[i][1]) / (values[i+1][1] - values[i][1])
                        standoff_value = values[i][0] + ratio * (values[i+1][0] - values[i][0])
                        self.standoff_accel = round(standoff_value, 2)
                        break
        self.update_accel_inputs()

    # Остальные методы (setup_conversion_table, interpolate_value и т.д.) остаются без изменений
    # (всё, что ниже в оригинальном коде — без изменений)

    def setup_conversion_table(self):
        # (полностью как в оригинале)
        left_game = self.left_game
        right_game = self.right_game
        mode = self.conversion_mode
        sensor = self.sensor_type
        if left_game == right_game:
            self.table_frame.add_widget(Label(text=self.get_text("same_games")))
            return
        rows = [
            (self.get_text("general_sens"), self.get_text("3person"), self.get_text("3person_dot"), "general_3p"),
            ("", self.get_text("1person"), self.get_text("standard"), "general_1p"),
            ("", self.get_text("col_holo_iron_side"), self.get_text("col_holo_aim"), "col"),
            ("", "2x", self.get_text("tactical"), "2x"),
            (self.get_text("in_scope"), "3x", "3x", "3x"),
            ("", "4x", "4x", "4x"),
            ("", "6x", "6x", "6x"),
            ("", "8x", "8x", "8x"),
            ("", "", self.get_text("sniper"), "6x_sniper")
        ]
        for standoff_label, pubg_label, cod_label, key in rows:
            left_label_text = standoff_label if left_game == "standoff" else pubg_label if left_game == "pubg" else cod_label
            right_label_text = standoff_label if right_game == "standoff" else pubg_label if right_game == "pubg" else cod_label
            font_size = dp(10) if 'кол' in left_label_text.lower() else dp(12)
            add_left = left_label_text or left_game == "standoff" or (left_game == "pubg" and key == "6x_sniper")
            if add_left:
                left_label = Label(text=left_label_text, font_size=font_size, size_hint_y=None, height=dp(40), halign='right', valign='middle')
                left_label.bind(size=left_label.setter('text_size'))
                self.table_frame.add_widget(left_label)
                state = True
                if left_game == "standoff":
                    if mode == "auto" and key == "general_3p" and left_label_text:
                        state = False
                    elif mode == "manual" and key in ["general_3p", "3x"] and left_label_text:
                        state = False
                elif left_game == "pubg" and right_game == "standoff":
                    if mode == "auto" and key == "general_3p" and left_label_text == self.get_text("3person"):
                        state = False
                    elif mode == "manual" and key in ["general_3p", "3x"] and left_label_text in [self.get_text("3person"), "3x"]:
                        state = False
                elif left_game == "pubg" and right_game == "cod":
                    if mode == "auto" and key == "general_3p" and left_label_text == self.get_text("3person"):
                        state = False
                    elif mode == "manual" and key in ["general_3p", "general_1p", "col", "2x", "3x", "4x", "6x", "8x"] and left_label_text:
                        state = False
                elif left_game == "cod" and right_game == "standoff":
                    if mode == "auto" and key == "general_3p" and left_label_text == self.get_text("3person_dot"):
                        state = False
                    elif mode == "manual" and key in ["general_3p", "3x"] and left_label_text in [self.get_text("3person_dot"), "3x"]:
                        state = False
                elif left_game == "cod" and right_game == "pubg":
                    if mode == "auto" and key == "general_3p" and left_label_text == self.get_text("3person_dot"):
                        state = False
                    elif mode == "manual" and key in ["general_3p", "general_1p", "col", "2x", "3x", "4x", "6x", "8x"] and left_label_text:
                        state = False
                if left_game == "pubg" and key == "6x_sniper":
                    state = True
                left_input = TextInput(text='', multiline=False, readonly=state, input_filter='float', size_hint_y=None, height=dp(40),
                                       padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14))
                if state:
                    left_input.background_color = [0.8, 0.8, 0.8, 1]
                    left_input.foreground_color = [0, 0, 0, 1]
                self.table_frame.add_widget(left_input)
                self.left_widgets.append((left_input, key, left_label_text))
            else:
                self.table_frame.add_widget(Label(text='', size_hint_y=None, height=dp(40)))
                left_input = TextInput(text='', multiline=False, readonly=True, size_hint_y=None, height=dp(40),
                                       padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14),
                                       background_color=[0.8, 0.8, 0.8, 1], foreground_color=[0, 0, 0, 1])
                self.table_frame.add_widget(left_input)
            right_label = Label(text=right_label_text, font_size=font_size, size_hint_y=None, height=dp(40), halign='right', valign='middle')
            right_label.bind(size=right_label.setter('text_size'))
            self.table_frame.add_widget(right_label)
            right_input = TextInput(text='', multiline=False, readonly=True, input_filter='float', size_hint_y=None, height=dp(40),
                                    padding=[dp(5), dp(5), dp(5), dp(5)], font_size=dp(14),
                                    background_color=[0.8, 0.8, 0.8, 1], foreground_color=[0, 0, 0, 1])
            self.table_frame.add_widget(right_input)
            self.entry_widgets.append((left_input, right_input, key, left_label_text, right_label_text))
            if mode == "auto":
                left_input.bind(text=partial(self.on_auto_text_change, key, right_input, left_input))
            else:
                left_input.bind(text=partial(self.on_manual_text_change, key, right_input, left_input, left_label_text))

    # Остальные методы (on_auto_text_change, update_auto_conversion и т.д.) полностью как в оригинале

class ConverterApp(App):
    # (полностью как в оригинале)
    def build(self):
        Window.fullscreen = 'auto'
        root = FloatLayout()
        self.converter = SensitivityConverter(size_hint=(1, 1), pos=(0, 0))
        root.add_widget(self.converter)
        self.menu = Menu(orientation='vertical', size_hint=(None, None), size=(dp(250), Window.height), pos=(-dp(250), 0))
        root.add_widget(self.menu)
        self.menu_btn = Button(text='☰', font_size=dp(24), size_hint=(None, None), size=(dp(40), dp(40)), pos=(dp(10), Window.height - dp(50)))
        self.menu_btn.bind(on_press=self.toggle_menu)
        root.add_widget(self.menu_btn)
        self.build_menu()
        Window.bind(size=self.on_window_resize)
        return root

    # остальные методы без изменений

if __name__ == '__main__':
    ConverterApp().run()
