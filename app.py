import os

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivymd.app import MDApp
import bcrypt
from datetime import date
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv('.env')
cluster = MongoClient(os.getenv('VAL'))
db = cluster["BookData"]
collection = db["books"]


# helper function
def fail_popup(retype: bool) -> None:
    show = Pop2() if retype else Pop()

    popup_win = Popup(title='Error', content=show, size_hint=(None, None),
                      size=(350, 100))
    popup_win.open()


class Pop(FloatLayout):
    pass


class Pop2(FloatLayout):
    pass


class LoginPage(Screen):
    user = ObjectProperty(None)
    pass1 = ObjectProperty(None)

    def btn_login(self) -> bool:
        user = self.user.text
        password = self.pass1.text.encode()
        # gets the information from the database.
        data_user = collection.find_one({"_id": user})
        if data_user is None:
            fail_popup(False)
            return False
        else:
            # currently hashed is a str of the hashed password
            hashed = data_user["password"]
        # clears textbox
        self.pass1.text = self.user.text = ''
        # used to check if hash corresponds with password
        if bcrypt.checkpw(password, hashed.encode()):
            return True
        else:
            fail_popup(True)
            return False


class RegisterPage(Screen):
    # saves the username and password inputted from the .kv file
    user = ObjectProperty(None)
    pass1 = ObjectProperty(None)
    pass2 = ObjectProperty(None)

    def btn_register(self) -> bool:
        if self.pass1.text != self.pass2.text or 40 < len(self.user.text) or\
                len(self.user.text) < 8 or ' ' in self.pass1.text:
            fail_popup(True)
            self.pass1.text = self.user.text = self.pass2.text = ''
            return False
        # converts password to bytes then encrypts it.
        user = self.user.text
        password = self.pass1.text.encode()
        # TODO: maybe add more rounds to make the password take longer to
        #  hash (for more security).
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
        data_user = collection.find_one({"_id": user})

        self.pass1.text = self.user.text = self.pass2.text = ''
        if data_user is not None or 32 < len(user) or \
                len(user) < 6 or ' ' in user:
            fail_popup(False)
            return False
        else:
            collection.insert_one({"_id": user, "password": hashed.decode(),
                                   "date": str(date.today())})
            return True


class UserPage(Screen):
    pass


class HomePage(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class BookApp(MDApp):
    """Class that builds and runs the app"""
    def build(self):
        return Builder.load_file('ui.kv')


if __name__ == "__main__":
    BookApp().run()
