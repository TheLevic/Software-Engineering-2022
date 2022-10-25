from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
import lib.db as db
from lib.Player import Player

Window.fullscreen = False
Window.size = (800, 800)
sm = ScreenManager()
red_players = []
green_players = []

class splashScreen(Screen):
    pass


class mainScreen(Screen):
    def myFunc(self):
        print("entering")


class mainApp(App):
    def build(self):
        sm.add_widget(Builder.load_file("kv/splashScreen.kv"))
        sm.add_widget(Builder.load_file("kv/mainScreen.kv"))
        return sm

    def submit(self):
        red_kv_dict = {}
        green_kv_dict = {}

        # create red and green team nested dictionary
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
        if red_kv_dict:
            for idx in red_kv_dict:
                values = (red_kv_dict[idx]['player_name'], red_kv_dict[idx]['player_id'])
                db.commitToDatabase(values)
                red_players.append(Player(red_kv_dict[idx]['player_name'], red_kv_dict[idx]['player_id']))
                self.root.get_screen('mainScreen').ids.testBox.text = f"{red_kv_dict[idx]['player_name']} " \
                                                                      f"{red_kv_dict[idx]['player_id']} added"
        if green_kv_dict:
            for idx in green_kv_dict:
                values = (green_kv_dict[idx]['player_name'], green_kv_dict[idx]['player_id'])
                db.commitToDatabase(values)
                green_players.append(Player(green_kv_dict[idx]['player_name'], green_kv_dict[idx]['player_id']))
                self.root.get_screen('mainScreen').ids.testBox.text = f"{green_kv_dict[idx]['player_name']} " \
                                                                      f"{green_kv_dict[idx]['player_id']} added"
        # additional print statements for testing purposes
        print("The red players are: ")
        for i in range(len(red_players)):
            print(red_players[i].name)

        print("The green players are: ")
        for i in range(len(green_players)):
            print(green_players[i].name)


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
