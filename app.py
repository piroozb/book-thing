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


class LoginPage(Screen):
    pass


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


class BookApp(MDApp):
    """Class that builds and runs the app"""
    def build(self):
        return Builder.load_file('ui.kv')


if __name__ == "__main__":
    BookApp().run()
