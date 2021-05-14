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
import bcrypt


class LoginPage(Screen):
    # saves the username and password inputted from the .kv file
    user = ObjectProperty(None)
    passw = ObjectProperty(None)

    def btn(self):
        print(f'{self.user.text} and {self.passw.text}')
        # converts password to bytes then encrypts it.
        password = self.passw.text.encode()
        # TODO: maybe add more rounds to make the password take longer to
        #  hash (for more security).
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
        print(hashed)
        # bcrypt.checkpw(password, hashed)
        # used to check if hash corresponds with password
        self.passw.text = self.user.text = ''


class RegisterPage(Screen):
    pass


class UserPage(Screen):
    pass


class HomePage(Screen):
    pass


class FeedPage(Screen):
    pass


class BookPage(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('ui.kv')


class BookApp(App):
    """Class that builds and runs the app"""
    def build(self):
        return kv


if __name__ == "__main__":
    BookApp().run()
