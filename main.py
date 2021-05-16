from typing import Optional, List
from classes import Publication, Book, Comment
import os
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.utils.fitimage import FitImage
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import ThreeLineAvatarListItem, TwoLineAvatarListItem, \
    ImageLeftWidget
import bcrypt
from datetime import date
from pymongo import MongoClient
from dotenv import load_dotenv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.behaviors import ButtonBehavior

# Constant to define demo mode or non-demo mode
DEMO = True

load_dotenv('.env')
cluster = MongoClient(os.getenv('VAL'))
db = cluster["BookData"]
collection = db["books"]
user_cluster = MongoClient(os.getenv('USER_VAL'))
db_user = user_cluster['UserData']
collection_user = db_user['BookThink']

ERROR = ["Registry failed: passwords doesn't match!",
         'Registry failed: invalid password!',
         'Registry failed: username already taken!',
         'Registry failed: username invalid!',
         'Login failed: invalid username or password.']


# helper function
def fail_popup(retype: int) -> None:
    show = ERROR[retype]

    popup_win = MDDialog(title='Error',
                         text=show, size=(.5, .5))
    popup_win.open()


class LoginPage(Screen):
    user = ObjectProperty(None)
    pass1 = ObjectProperty(None)

    def btn_login(self) -> bool:
        """Method for when someone tries to log in"""
        user = self.user.text
        password = self.pass1.text.encode()
        # gets the information from the database.
        data_user = collection_user.find_one({"_id": user})
        if data_user is None:
            fail_popup(4)
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
            fail_popup(4)
            return False


class RegisterPage(Screen):
    # saves the username and password inputted from the .kv file
    user = ObjectProperty(None)
    pass1 = ObjectProperty(None)
    pass2 = ObjectProperty(None)

    def btn_register(self) -> bool:
        """Method for when someone tries to register"""
        # checks if passwords match, has the right characters and is not too
        # long/short
        if self.pass1.text != self.pass2.text:
            fail_popup(0)
            return False
        elif 40 < len(self.pass1.text) or len(self.pass1.text) < 8 \
                or ' ' in self.pass1.text:
            fail_popup(1)
            self.pass1.text = self.user.text = self.pass2.text = ''
            return False
        # converts password to bytes then encrypts it.
        user = self.user.text
        password = self.pass1.text.encode()
        # TODO: maybe add more rounds to make the password take longer to
        #  hash (for more security).
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=12))
        data_user = collection_user.find_one({"_id": user})
        self.pass1.text = self.user.text = self.pass2.text = ''
        # checks if user already exists, has the right characters and is not too
        # long/short
        if data_user is not None:
            fail_popup(2)
            return False
        elif 32 < len(user) or len(user) < 6 or ' ' in user:
            fail_popup(3)
            return False
        else:
            # uploads info to the database
            collection_user.insert_one({"_id": user,
                                        "password": hashed.decode(),
                                        "date": str(date.today())})
            return True


class HomePage(Screen):
    pass


class BookPage(Screen):
    img_path = 'images/Demo/Books/1984.png'
    book = Book('1984', 'George Orwell', 'Dystopian Fiction', 328, 23)
    comments = [Comment("I hated this book!", "user420"),
                Comment("I loved this! Couldn't put it down.", "user001"),
                Comment("What a wonderful book!", "user489")]




class WindowManager(ScreenManager):
    pass


class BookApp(MDApp):
    """Class that builds and runs the app"""

    def build(self):
        return Builder.load_file('ui.kv')

    def update_publication_grid(self, search_keywords: Optional[str] = None) -> None:
        buttons = self.get_publication_buttons(search_keywords)
        self.root.screens[-1].ids.book_grid.clear_widgets()
        for button in buttons:
            self.root.screens[-1].ids.book_grid.add_widget(button)

    def get_publication_buttons(self, search_keywords: Optional[str] = None
                                ) -> List[TwoLineAvatarListItem]:
        buttons = []
        if DEMO:
            img_paths = ['images/Demo/Books/1984.png',
                         'images/Demo/Books/IHaveTheRightToDestroyMyself.png',
                         'images/Demo/Books/NoPlaceLikeHere.png',
                         'images/Demo/Books/OneFlewOverTheCuckoosNest.png',
                         'images/Demo/Books/TheGirlWithTheDragonTattoo.png',
                         'images/Demo/Books/TheHobbit.png',
                         'images/Demo/Books/TheNarrowRoadToTheDeepNorth.png',
                         'images/Demo/Books/ThreeDayRoad.png',
                         'images/Demo/Books/WhyWeSleep.png']
            books = [Book('1984', 'George Orwell', 'Dystopian Fiction', 328,
                          23),
                     Book('I Have The Right To Destroy Myself', 'Young-Ha Kim',
                          'Fiction', 131),
                     Book('No Place Like Here', 'Christina June', 'Fiction', 32,
                          231),
                     Book('One Flew Over The Cuckoos Nest', 'Ken Kesey',
                          'Fiction', 500, 12),
                     Book('The Girl With The Dragon Tattoo', 'Stieg Larsson',
                          'Fiction', 34),
                     Book('The Hobbit', 'J. R. R. Tolkien', 'Fantasy', 300),
                     Book('The Narrow Road To The Deep North',
                          'Richard Flanagan', 'Fantasy', 430),
                     Book('Three Day Road', 'Joseph Boyden', 'Fiction', 223),
                     Book('Why We Sleep', 'Matthew Walker', 'Fiction', 190)
                     ]
            for i in range(9):
                book = books[i]
                if search_keywords is None or search_keywords.lower() in \
                        (book.title + book.author).lower():
                    buttons.append(
                        self.build_publication_button(img_paths[i], books[i]))
            return buttons
        else:
            # access database and based on search, add books from there
            pass

    def build_publication_button(self, img_path: str, publication: Publication
                                 ) -> TwoLineAvatarListItem:
        button = TwoLineAvatarListItem(text=publication.title,
                                       secondary_text=publication.author,
                                       on_release=self.change_screens)
        button.add_widget(ImageLeftWidget(source=img_path))
        return button

    def change_screens(self, *args) -> None:
        self.root.transition.direction = 'left'
        self.root.current = 'book_info'

    def update_recent_comments(self) -> None:
        comments = self.get_recent_comments()
        self.root.screens[-1].ids.recent_posts.clear_widgets()
        for comment in comments:
            self.root.screens[-1].ids.recent_posts.add_widget(comment)

    def get_recent_comments(self) -> List[BoxLayout]:
        recent_comments = []
        if DEMO:
            img_paths = ['images/Demo/Books/1984.png',
                         'images/Demo/Books/IHaveTheRightToDestroyMyself.png',
                         'images/Demo/Books/NoPlaceLikeHere.png'
                         ]
            books = [Book('1984', 'George Orwell', 'Dystopian Fiction', 328,
                          23),
                     Book('I Have The Right To Destroy Myself', 'Young-Ha Kim',
                          'Fiction', 131),
                     Book('No Place Like Here', 'Christina June', 'Fiction', 32,
                          231)
                     ]
            comments = [Comment("I hated this book!", "user420"),
                        Comment("I loved this! Couldn't put it down.", "user001"),
                        Comment("What a wonderful book!", "user489")
                        ]
            for i in range(3):
                recent_comments.append(self.format_comment_preview(
                    img_paths[i], books[i], comments[i]))
            return recent_comments
        else:
            pass

    def format_comment_preview(self, img_path: str, publication: Publication,
                               comment: Comment) -> BoxLayout:
        """
        set up a comment for preview (for profile page)
        """
        comment_preview = ThreeLineAvatarListItem(
            text=publication.title, secondary_text=publication.author,
            tertiary_text=f'"{comment.content[:20]}..."', ripple_scale=0,
            font_style='H6', secondary_font_style='Body2',
            secondary_theme_text_color='Primary')
        comment_preview.add_widget(ImageLeftWidget(source=img_path))
        return comment_preview


# class PreviousMDIcons(Screen):
#
#     def set_list_md_icons(self, text="", search=False):
#         '''Builds a list of icons for the screen MDIcons.'''
#
#         def add_icon_item(name_icon):
#             self.ids.rv.data.append(
#                 {
#                     "viewclass": "CustomOneLineIconListItem",
#                     "icon": name_icon,
#                     "text": name_icon,
#                     "callback": lambda x: x,
#                 }
#             )
#
#         self.ids.rv.data = []
#         for name_icon in md_icons.keys():
#             if search:
#                 if text in name_icon:
#                     add_icon_item(name_icon)
#             else:
#                 add_icon_item(name_icon)


# class MainApp(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = PreviousMDIcons()
#
#     def build(self):
#         return self.screen
#
#     def on_start(self):
#         self.screen.set_list_md_icons()


if __name__ == "__main__":
    BookApp().run()
