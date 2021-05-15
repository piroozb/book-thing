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
import pickle
from datetime import date


class Pop(FloatLayout):
    pass


class Pop2(FloatLayout):
    pass


class LoginPage(Screen):
    pass


class RegisterPage(Screen):
    # saves the username and password inputted from the .kv file
    user = ObjectProperty(None)
    pass1 = ObjectProperty(None)
    pass2 = ObjectProperty(None)

    def btn_register(self) -> bool:
        if self.pass1.text != self.pass2.text:
            self.fail_popup(True)
            return False
        print(f'{self.user.text} and {self.pass1.text}')
        # converts password to bytes then encrypts it.
        password = self.pass1.text.encode()
        # TODO: maybe add more rounds to make the password take longer to
        #  hash (for more security).
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
        print(hashed)
        # bcrypt.checkpw(password, hashed)
        # used to check if hash corresponds with password
        pickle_file = open('user.pkl', 'rb')
        user_dict = pickle.load(pickle_file)
        if self.user.text in user_dict.keys():
            self.fail_popup(False)
            return False
        else:
            user_dict[self.user.text] = [hashed, date.today()]
            with open('user.pkl', 'wb') as f:
                pickle.dump(user_dict, f)
            self.passw.text = self.user.text = ''
            return True

    def fail_popup(self, retype: bool) -> None:
        show = Pop2() if retype else Pop()

        popup_win = Popup(title='Error', content=show, size_hint=(None, None),
                          size=(100, 100))
        popup_win.open()


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
