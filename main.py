from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
import lib.db as db
import lib.Player as Player


Window.fullscreen = False
Window.size = (800, 800)
sm = ScreenManager()


class splashScreen(Screen):
    pass

class playActionDisplay(Screen):
    pass

class mainScreen(Screen):
    pass

class keyboardInput(Screen):
    def __init__(self, **kwargs):
        super(keyboardInput, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.switchScreens = False
    
    def _keyboard_closed(self):
        pass

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'f5':
            self.switchScreens = not self.switchScreens
            if self.switchScreens == True:
                sm.current = "playActionDisplay"
            if self.switchScreens == False:
                sm.current = "mainScreen"
            
        # Return True to accept the key.
        return True

class mainApp(App):
    def build(self):
        sm.add_widget(Builder.load_file("kv/splashScreen.kv"))
        sm.add_widget(Builder.load_file("kv/mainScreen.kv"))
        sm.add_widget(Builder.load_file("kv/playActionDisplay.kv"))
        sm.add_widget(Builder.load_file("kv/keyboardInput.kv"))
        return sm

    def submit(self):
        red_kv_dict = {}
        green_kv_dict = {}
        # output that the command successfully executed
        # self.root.get_screen(
        #     'mainScreen').ids.testBox.text = f'{self.root.get_screen("mainScreen").ids.name_entry0.text} {self.root.get_screen("mainScreen").ids.id_entry0.text} added'
        # create red  and green team nested dictionary
        for i in range(15):
            red_name_string = f'self.root.get_screen("mainScreen").ids.red_name_entry{i}.text'
            red_id_string = f'self.root.get_screen("mainScreen").ids.red_id_entry{i}.text'
            green_name_string = f'self.root.get_screen("mainScreen").ids.green_name_entry{i}.text'
            green_id_string = f'self.root.get_screen("mainScreen").ids.green_id_entry{i}.text'
            if eval(red_name_string) == "" and eval(green_name_string) == "":
                break
            if eval(red_name_string) != "":
                red_sub_dict = {f'red_{i}': {'player_name': eval(red_name_string), 'player_id': eval(red_id_string)}}
                red_kv_dict.update(red_sub_dict)
            if eval(green_name_string) != "":
                green_sub_dict = {f'green_{i}': {'player_name': eval(green_name_string), 'player_id': eval(green_id_string)}}
                green_kv_dict.update(green_sub_dict)
        # print statements for debugging purposes
        print(red_kv_dict)
        print(green_kv_dict)
        if red_kv_dict:
            for idx in red_kv_dict:
                values = (red_kv_dict[idx]['player_name'], red_kv_dict[idx]['player_id'])
                db.commitToDatabase(values)
                self.root.get_screen('mainScreen').ids.testBox.text = f"{red_kv_dict[idx]['player_name']} " \
                                                                      f"{red_kv_dict[idx]['player_id']} added"
        if green_kv_dict:
            for idx in green_kv_dict:
                values = (green_kv_dict[idx]['player_name'], green_kv_dict[idx]['player_id'])
                db.commitToDatabase(values)
                self.root.get_screen('mainScreen').ids.testBox.text = f"{green_kv_dict[idx]['player_name']} " \
                                                                      f"{green_kv_dict[idx]['player_id']} added"

    def showRecords(self):
        records = db.getAllDbValues()
        word = ''
        # loop through the returned records from our database
        for record in records:
            word = f'{word}\n{record[0]} {record[1]}'
            self.root.get_screen('mainScreen').ids.testBox.text = f'{word}'

    def removeRecords(self):
        print('Database cleared')
        db.clearDB()

    def on_start(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, dt):
        sm.current = "mainScreen"

    
    


if __name__ == '__main__':
    mainApp().run()
