"""
                    Library Management System:
    
    Author: Howard Anderson.

    Date: 16/06/2024.

    Description: Library Management System.

    Filename: main.py.

"""

# PyMySQL Imports:
from pymysql.connections import Connection
from pymysql.cursors import Cursor

# Curses Imports:
import curses
from curses import wrapper
from curses.textpad import Textbox

# Termtable Imports:
import termtables as tt

# LibMan Inports:
import libman
from libman import Library
from libman import User
from libman import Book

# Queries Imports:
import Queries
from Queries import table

from getpass import getpass

"""
class Application:

    def __init__(self):
        
        #username = input("\n[ # ]: Username: ")
        #password = getpass(prompt="\n[ # ]: Password: ")
        username, password = "anderson", "Anderson#7"
        self.connection = Connection(user=username, password=password, database="LIBMAN")
        self.connection.begin()
        self.cursor = self.connection.cursor(cursor=Cursor)
        library = Library(self.connection)


    def run(self):
        
        print(menu_logo)
        options = "\
        \n    1] Add Items \
        \n    2] Update Items \
        \n    3] View Items \
        \n    4] Search Items \
        \n    5] Delete Items \
        \n"
        print(options)



if __name__ == "__main__":
    library_application = Application()
    library_application.run()

"""

logo = (
    r">>========================================<<",
    r"||                                        ||",
    r"||                                        ||",
    r"||  _     ___ ____  __  __    _    _   _  ||",
    r"|| | |   |_ _| __ )|  \/  |  / \  | \ | | ||",
    r"|| | |    | ||  _ \| |\/| | / _ \ |  \| | ||",
    r"|| | |___ | || |_) | |  | |/ ___ \| |\  | ||",
    r"|| |_____|___|____/|_|  |_/_/   \_\_| \_| ||",
    r"||                                        ||",
    r"||                                        ||",
    r">>========================================<<",
)

menu_logo = (
    r"+----------------------------------------------------+",
    r"|                                                    |",
    r"|   __  __       _         __  __                    |",
    r"|  |  \/  | __ _(_)_ __   |  \/  | ___ _ __  _   _   |",
    r"|  | |\/| |/ _` | | '_ \  | |\/| |/ _ \ '_ \| | | |  |",
    r"|  | |  | | (_| | | | | | | |  | |  __/ | | | |_| |  |",
    r"|  |_|  |_|\__,_|_|_| |_| |_|  |_|\___|_| |_|\__,_|  |",
    r"|                                                    |",
    r"+----------------------------------------------------+",
)


class Application:


    def __init__(self, stdscr) -> None:
        """
            Constructor:
                Initialize Colour pairs.
                Set Main Screen.
        """
        # Standard Screen.
        self.stdscr = stdscr
        self.screen_height, self.screen_width = (curses.LINES, curses.COLS)

        # Colours:
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.GREEN_BLACK = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        self.BLUE_BLACK = curses.color_pair(2)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        self.BLACK_GREEN = curses.color_pair(3)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        self.BLACK_YELLOW = curses.color_pair(4)

        # Screen:
        self.stdscr.clear()
        self.stdscr.border()
        self.stdscr.addstr(0, self.center_words(self.screen_width, "LIBMAN"), "LIBMAN", curses.A_BOLD | self.GREEN_BLACK)
        self.stdscr.refresh()

        self.main_menu()

    def center_words(self, win_width, word) -> int:
        """
            Retutns the Start Coordinate that can be passed to addstr() to place the word in Center.
            Word Placement: Mid - (len(word) / 2).
        """
        return int((win_width/ 2) - (len(word) / 2))

    def main_menu(self) -> None:
        """
            Main Menu Window:
                - User
                - Books
                - Transactions
        """
        # Main Window:
        main_win_height, main_win_width = self.screen_height - 2, self.screen_width - 2
        main_win: curses.window = curses.newwin(main_win_height, main_win_width, 1, 1)

        # Main Window Loop:
        while True:

            # Main Window:
            main_win.clear()
            main_win.refresh()

            main_win.border()
            #main_win.bkgd(" ", self.BLACK_GREEN)
            main_win.addstr(0, self.center_words(main_win_width, "MAIN MENU"), "MAIN MENU", curses.A_BOLD | self.BLUE_BLACK)

            # Printing Logo:
            for row in range(len(logo)):
                main_win.addstr(row + 4, self.center_words(main_win_width, logo[row]), logo[row])

            main_win.refresh()

            # Buttons:
            buttons: dict = {
                "USER": main_win.subwin(5, 21, 20, 20),
                "BOOKS": main_win.subwin(5, 21, 25, 20),
                "TRANSACTIONS": main_win.subwin(5, 21, 30, 20),
                "EXIT": main_win.subwin(5, 21, 40, 20)
                }

            menu_items: list = list(buttons.keys())

            # Write the Name of the Buttons:
            for name, win in buttons.items():
                win.addstr(2, int((21 / 2) - len(name) / 2), name, curses.A_NORMAL | self.BLUE_BLACK)
                win.border()
                win.refresh()

            # User - Highlight the Button:
            buttons["USER"].addstr(2, int((21 / 2) - len("USER") / 2), "USER", curses.A_STANDOUT | self.GREEN_BLACK)
            buttons["USER"].refresh()

            # Key to track the selected Button.
            selection: int = 0

            key: str = self.stdscr.getkey()
            main_win.refresh()

            # Scrolling Loop:
            while True:
                # Move Up:
                if key == "KEY_UP":
                    selection -= 1

                # Move Below:
                elif key == "KEY_DOWN":
                    selection += 1

                # Exit out of the Loop and Quit.
                if key == "q" or key == "Q":
                    del main_win
                    return

                # Select the current highlighted Button.
                elif key == "y" or key == "Y":
                    if menu_items[selection] in menu_items[:-1]:
                        self.second_win(main_win, main_win_width, menu_items[selection])
                        break
                    else:
                        return

                # Reset the Selection Variable:
                if selection < 0:
                    selection = 3

                elif selection > 3:
                    selection = 0

                # Perform the Scrolling action by Changing the Highlighted Button.
                for name, win in buttons.items():
                    if name == menu_items[selection]:
                        win.addstr(2, int((21 / 2) - (len(name) / 2)), name, curses.A_STANDOUT | self.GREEN_BLACK)

                    else:
                        win.addstr(2, int((21 / 2) - (len(name) / 2)), name, curses.A_NORMAL | self.BLUE_BLACK)

                    win.border()
                    win.refresh()

                key = self.stdscr.getkey()
                main_win.refresh()


    def second_win(self, main_win: curses.window, main_win_width: int, main_choice : str) -> None:
        """
            Second Window:
                - Add / Issue
                - Search
                - Update
                - View
                - Remove / Return
        """

        # Second Window Loop:
        while True:

            # Apply the Transition to the Second Window:
            main_win.clear()
            main_win.border()
            main_win.addstr(0, self.center_words(main_win_width, main_choice), main_choice, curses.A_BOLD | self.BLUE_BLACK)
            main_win.refresh()

            # Printing Logo:
            for row in range(len(logo)):
                main_win.addstr(row + 4, 10, logo[row])

            main_win.refresh()

            # Based on the Choice, Buttons to be view:
            if main_choice == "TRANSACTIONS":

                buttons = {
                    "ISSUE" : main_win.subwin(4, 21, 20, 20),
                    "UPDATE": main_win.subwin(4, 21, 25, 20),
                    "SEARCH": main_win.subwin(4, 21, 30, 20),
                    "VIEW": main_win.subwin(4, 21, 35, 20),
                    "RETURN": main_win.subwin(4, 21, 40, 20),
                    "BACK": main_win.subwin(4, 21, 45, 20)
                }

            else:

                buttons = {
                    "ADD" : main_win.subwin(4, 21, 20, 20),
                    "UPDATE": main_win.subwin(4, 21, 25, 20),
                    "SEARCH": main_win.subwin(4, 21, 30, 20),
                    "VIEW": main_win.subwin(4, 21, 35, 20),
                    "REMOVE": main_win.subwin(4, 21, 40, 20),
                    "BACK": main_win.subwin(4, 21, 45, 20)
                }

            button_names = list(buttons.keys())
            button_width = 21

            # Name the Buttons and Apply Border:
            for name, win in buttons.items():
                win.addstr(1, int((21 / 2) - len(name) / 2), name, curses.A_NORMAL | self.BLUE_BLACK)
                win.border()
                win.refresh()

            # Highlight the First Button:
            if main_choice == "TRANSACTIONS":
                buttons["ISSUE"].addstr(1, self.center_words(button_width, "ISSUE"), "ISSUE", curses.A_STANDOUT | self.GREEN_BLACK)
                buttons["ISSUE"].refresh()

            else:
                buttons["ADD"].addstr(1, self.center_words(button_width, "ADD"), "ADD", curses.A_STANDOUT | self.GREEN_BLACK)
                buttons["ADD"].refresh()

            # Perform Area Window variables:
            perform_area_width = self.screen_width - 75
            perform_area_height = self.screen_height - 4
            pos_x = 2
            pos_y = (self.screen_width - perform_area_width) - 3 # Leave Space for Buttons.

            # Perform Area Window:
            perform_area = main_win.subwin(perform_area_height, perform_area_width, pos_x, pos_y)
            perform_area.attron(self.GREEN_BLACK)
            perform_area.border()
            perform_area.addstr(0, self.center_words(perform_area_width, "PERFORM AREA"), "PERFORM AREA")
            perform_area.attroff(self.GREEN_BLACK)
            perform_area.refresh()

            # Keep track of the selected Button:
            selection = 0

            # Get Key Input to perform action:
            key = self.stdscr.getkey()
            main_win.refresh()

            # Second Window Scrolling Loop:
            while True:

                if key == "KEY_UP":
                    selection -= 1

                elif key == "KEY_DOWN":
                    selection += 1

                elif key == "y" or key == "Y":

                    if main_choice == "TRANSACTIONS":

                        actions = {
                            "ISSUE": self.issue_book,
                            "UPDATE": self.update,
                            "SEARCH": self.search,
                            "VIEW": self.view,
                            "RETURN": self.return_book
                        }

                    else:

                        actions = {
                            "ADD": self.add,
                            "UPDATE": self.update,
                            "SEARCH": self.search,
                            "VIEW": self.view,
                            "REMOVE": self.remove
                        }

                    if button_names[selection] in button_names[:-1]:
                        actions[button_names[selection]](perform_area, perform_area_height, perform_area_width, main_choice)
                        break

                    # Back Button -> Go to previous Window and follow the Main Window Loop:
                    else:
                        return

                # Back Key-> Go to previous Window and follow the Main Window Loop:
                elif key == "b" or key == "B":
                    main_win.clear()
                    return

                # Reset to keep in bounds:
                if selection < 0:
                    selection = 5

                elif selection > 5:
                    selection = 0

                # Implement Scrolling action by changing the Changing the Highlighted Button:
                for name, win in buttons.items():
                    if name == button_names[selection]:
                        win.addstr(1, int((21 / 2) - (len(name) / 2)), name, curses.A_STANDOUT | self.GREEN_BLACK)

                    else:
                        win.addstr(1, int((21 / 2) - (len(name) / 2)), name, curses.A_NORMAL | self.BLUE_BLACK)

                    win.border()
                    win.refresh()

                key = self.stdscr.getkey()
                main_win.refresh()


    def add(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str) -> None:

        # Text Box Containers:
        if main_choice == "USER":

            text_wins = {
                "NAME": perform_area.subwin(3, 102, 10, self.screen_width - perform_area_width),
                "PHONE NUMBER": perform_area.subwin(3, 102, 15, self.screen_width - perform_area_width),
                "AGE": perform_area.subwin(3, 102, 20, self.screen_width - perform_area_width),
                "JOIN DATE": perform_area.subwin(3, 102, 25, self.screen_width - perform_area_width)
            }

        else:

            text_wins = {
                "NAME": perform_area.subwin(3, 102, 10, self.screen_width - perform_area_width),
                "AUTHOR": perform_area.subwin(3, 102, 15, self.screen_width - perform_area_width),
                "PRICE": perform_area.subwin(3, 102, 20, self.screen_width - perform_area_width),
                "PURCHASE DATE": perform_area.subwin(3, 102, 25, self.screen_width - perform_area_width)
            }

        text_wins_names = list(text_wins.keys())

        # Print TextBox Windows:
        for name, text_win in text_wins.items():
            text_win.border()
            text_win.addstr(0, 1, name, curses.A_BOLD)
            text_win.refresh()

        buttons = {
            "SAVE": perform_area.subwin(4, 21, 35, self.screen_width - perform_area_width),
            "BACK": perform_area.subwin(4, 21, 40, self.screen_width - perform_area_width)
        }

        for button_name, button in buttons.items():
            button.border()
            button.addstr(1, int((21 / 2) - (len(button_name) / 2)), button_name, curses.A_NORMAL | self.BLUE_BLACK)
            button.refresh()

        perform_area.refresh()

        # Text Boxes:
        pos_x_inc = 0
        text_boxes = []
        for name, text_win in text_wins.items():
            text_boxes.append(curses.newwin(1, 100, 11 + pos_x_inc, self.screen_width - perform_area_width + 1))
            pos_x_inc += 5


        text_wins["NAME"].border()
        text_wins["NAME"].addstr(0, 1, "NAME", curses.A_STANDOUT | self.BLUE_BLACK)
        text_wins["NAME"].refresh()

        selection = 0
        texts = ["" for _ in text_wins]

        key = self.stdscr.getkey()

        while True:

            if key == "KEY_UP":
                selection -= 1

            elif key == "KEY_DOWN":
                selection += 1

            elif key == "y" or key == "Y" :
                if selection <= 3:
                    texts[selection] = Textbox(text_boxes[selection]).edit().strip().replace("\n", "")

                # Save
                if selection == 4:
                    break

                # Back
                else:
                    break

            elif key == "b" or key == "B":
                break

            # Reset Selection to be in Range:
            if selection < 0:
                selection = 5

            elif selection > 5:
                selection = 0

            # Normalize Buttons if they aren't Selected:
            if selection <= 3:
                buttons["SAVE"].addstr(1, int((21 / 2) - (len("SAVE") / 2)), "SAVE", curses.A_NORMAL | self.BLUE_BLACK)
                buttons["SAVE"].refresh()
                buttons["BACK"].addstr(1, int((21 / 2) - (len("BACK") / 2)), "BACK", curses.A_NORMAL | self.BLUE_BLACK)
                buttons["BACK"].refresh()

                text_index = 0
                for name, text_win in text_wins.items():
                    text_win.clear()
                    text_win.border()
                    text_win.addstr(0, 1, name, curses.A_BOLD)
                    text_win.addstr(1, 1, texts[text_index], curses.A_ITALIC)

                    if text_wins_names[selection] == name:
                        text_win.addstr(0, 1, name, curses.A_STANDOUT | self.BLUE_BLACK)

                    text_index += 1
                    text_win.refresh()

            # Actions if Buttons are Selected:
            if selection > 3:
                # Save:
                if selection == 4:
                    buttons["SAVE"].addstr(1, int((21 / 2) - (len("SAVE") / 2)), "SAVE", curses.A_STANDOUT | self.GREEN_BLACK)
                    buttons["SAVE"].refresh()
                    buttons["BACK"].addstr(1, int((21 / 2) - (len("BACK") / 2)), "BACK", curses.A_NORMAL | self.BLUE_BLACK)
                    buttons["BACK"].refresh()

                else:
                    buttons["SAVE"].addstr(1, int((21 / 2) - (len("SAVE") / 2)), "SAVE", curses.A_NORMAL | self.BLUE_BLACK)
                    buttons["SAVE"].refresh()
                    buttons["BACK"].addstr(1, int((21 / 2) - (len("BACK") / 2)), "BACK", curses.A_STANDOUT | self.GREEN_BLACK)
                    buttons["BACK"].refresh()


            key = self.stdscr.getkey()

        #self.stdscr.getch()
        return

    def update(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str):
        # Update the Title of the Perform Area:
        perform_area.clear()
        perform_area.attron(self.GREEN_BLACK)
        perform_area.border()
        perform_area.attroff(self.GREEN_BLACK)
        perform_area.addstr(0, self.center_words(perform_area_width, f"UPDATE {main_choice}"), f"UPDATE {main_choice}", curses.A_BOLD)
        perform_area.refresh()

        # Update Text Box Containers:
        if main_choice == "USER":

            update_text_wins = {
                "NAME": perform_area.subwin(3, 102, 10, self.screen_width - perform_area_width),
                "AGE": perform_area.subwin(3, 102, 15, self.screen_width - perform_area_width),
                "PHONE NUMBER": perform_area.subwin(3, 102, 20, self.screen_width - perform_area_width),
                "JOIN DATE": perform_area.subwin(3, 102, 25, self.screen_width - perform_area_width)
            }

        elif main_choice == "BOOKS":

            update_text_wins = {
                "NAME": perform_area.subwin(3, 102, 10, self.screen_width - perform_area_width),
                "AUTHOR": perform_area.subwin(3, 102, 15, self.screen_width - perform_area_width),
                "PRICE": perform_area.subwin(3, 102, 20, self.screen_width - perform_area_width),
                "PURCHASE DATE": perform_area.subwin(3, 102, 25, self.screen_width - perform_area_width)
            }

        # Search Text Box Containers:
        search_text_wins = {
            "UNIQUE VALUE": perform_area.subwin(3, 102, 10, self.screen_width - perform_area_width),
            "NAME": perform_area.subwin(3, 102, 15, self.screen_width - perform_area_width),
        }

        # Buttons:
        buttons = {
            "SEARCH": perform_area.subwin(4, 21, 35, (self.screen_width - perform_area_width) + 40),
            "UPDATE": perform_area.subwin(4, 21,35, (self.screen_width - perform_area_width) + 40),
            "BACK": perform_area.subwin(4, 21, 40, (self.screen_width - perform_area_width) + 40)
        }

        # Labeling Search Textbox Containers:
        for name, text_win in search_text_wins.items():
            text_win.border()
            text_win.addstr(0, 1, name, curses.A_BOLD)
            text_win.refresh()

        # Labeling Buttons:
        for name, button in buttons.items():
            if name != "UPDATE":
                button.border()
                button.addstr(1, self.center_words(21, name), name, self.BLUE_BLACK)
                button.refresh()

        # Search Text Boxes:
        pos_x_inc = 0
        search_text_boxes = []
        for name, text_win in search_text_wins.items():
            search_text_boxes.append(curses.newwin(1, 100, 11 + pos_x_inc, self.screen_width - perform_area_width + 1))
            pos_x_inc += 5

        search_text_wins["UNIQUE VALUE"].addstr(0, 1, "UNIQUE VALUE", curses.A_STANDOUT | self.BLUE_BLACK)
        search_text_wins["UNIQUE VALUE"].refresh()


        selection = 0
        search_texts = ["" for _ in search_text_wins]
        update_texts = ["" for _ in update_text_wins]

        key = self.stdscr.getkey()

        # Search Loop:
        while True:

            if key == "KEY_UP":
                selection -= 1

            elif key == "KEY_DOWN":
                selection += 1

            elif key == "y" or key == "Y":

                # Textbox is Selected:
                if selection < 2:
                    search_texts[selection] = Textbox(search_text_boxes[selection]).edit().strip().replace("\n", "")

                # Search:
                elif selection == 2:
                    perform_area.clear()
                    perform_area.attron(self.GREEN_BLACK)
                    perform_area.border()
                    perform_area.attroff(self.GREEN_BLACK)
                    perform_area.addstr(0, self.center_words(perform_area_width, f"UPDATE {main_choice}"), f"UPDATE {main_choice}", curses.A_BOLD)
                    perform_area.refresh()
                    break

                # Back
                else:
                    return

            elif key == "b" or key == "B":
                return

            # Reset Selection:
            if selection > 3:
                selection = 0;

            elif selection < 0:
                selection = 3

            # Normalize Buttons if they aren't Selected:
            if selection < 2:
                buttons["SEARCH"].addstr(1, self.center_words(21, "SEARCH"), "SEARCH", curses.A_NORMAL | self.BLUE_BLACK)
                buttons["SEARCH"].refresh()
                buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_NORMAL | self.BLUE_BLACK)
                buttons["BACK"].refresh()

                # Actions if Textbox is Selected:
                text_index = 0
                search_text_wins_names = list(search_text_wins.keys())

                for name, text_win in search_text_wins.items():
                    text_win.clear()
                    text_win.border()
                    text_win.addstr(0, 1, name, curses.A_BOLD)
                    text_win.addstr(1, 1, search_texts[text_index], curses.A_ITALIC)

                    if search_text_wins_names[selection] == name:
                        text_win.addstr(0, 1, name, curses.A_STANDOUT | self.BLUE_BLACK)

                    text_index += 1
                    text_win.refresh()

            # Actions if Buttons are Selected:
            else:

                # Search:
                if selection == 2:
                    buttons["SEARCH"].addstr(1, self.center_words(21, "SEARCH"), "SEARCH", curses.A_STANDOUT | self.GREEN_BLACK)
                    buttons["SEARCH"].refresh()
                    buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_NORMAL | self.BLUE_BLACK)
                    buttons["BACK"].refresh()

                else:
                    buttons["SEARCH"].addstr(1, self.center_words(21, "SEARCH"), "SEARCH", curses.A_NORMAL | self.BLUE_BLACK)
                    buttons["SEARCH"].refresh()
                    buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_STANDOUT| self.GREEN_BLACK)
                    buttons["BACK"].refresh()

            key = self.stdscr.getkey()

        # Labeling Update Textbox Containers:
        for name, text_win in update_text_wins.items():
            text_win.border()
            text_win.addstr(0, 1, name, curses.A_BOLD)
            text_win.refresh()

        # Labeling Buttons:
        for name, button in buttons.items():
            if name != "SEARCH":
                button.border()
                button.addstr(1, self.center_words(21, name), name, curses.A_NORMAL | self.BLUE_BLACK)
                button.refresh()

        # Update Text Boxes:
        pos_x_inc = 0
        update_text_boxes = []
        for name, text_win in update_text_wins.items():
            update_text_boxes.append(curses.newwin(1, 100, 11 + pos_x_inc, self.screen_width - perform_area_width + 1))
            pos_x_inc += 5

        update_text_wins["NAME"].addstr(0, 1, "NAME", curses.A_STANDOUT | self.BLUE_BLACK)
        update_text_wins["NAME"].refresh()

        selection = 0
        key = self.stdscr.getkey()

        # Update Loop:
        while True:

            if key == "KEY_UP":
                selection -= 1

            elif key == "KEY_DOWN":
                selection += 1

            if key == "y" or key == "Y":

                # Textbox is Selected:
                if selection <= 3:
                    update_texts[selection] = Textbox(update_text_boxes[selection]).edit().strip().replace("\n", "")

                # Update:
                elif selection == 4:
                    self.update(perform_area, perform_area_height, perform_area_width, main_choice)
                    return

                # Back:
                else:
                    return

            elif key == "b" or key == "B":
                return

            # Reset Selection:
            if selection < 0:
                selection = 5

            elif selection > 5:
                selection = 0

            # Normalize Buttons when they aren't Selected:
            if selection  <= 3:
                buttons["UPDATE"].addstr(1, self.center_words(21, "UPDATE"), "UPDATE", curses.A_NORMAL | self.BLUE_BLACK)
                buttons["UPDATE"].refresh()
                buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_NORMAL | self.BLUE_BLACK)
                buttons["BACK"].refresh()

                # Actions if Textboxes are Selected:
                text_index = 0
                update_text_wins_names = list(update_text_wins.keys())

                for name, text_win in update_text_wins.items():
                    text_win.clear()
                    text_win.border()
                    text_win.addstr(0, 1, name, curses.A_BOLD)
                    text_win.addstr(1, 1, update_texts[text_index], curses.A_ITALIC)

                    if update_text_wins_names[selection] == name:
                        text_win.addstr(0, 1, name, curses.A_STANDOUT | self.BLUE_BLACK)

                    text_index += 1
                    text_win.refresh()

            # Actions if Buttons are Selected:
            else:

                if selection == 4:
                    buttons["UPDATE"].addstr(1, self.center_words(21, "UPDATE"), "UPDATE", curses.A_STANDOUT | self.GREEN_BLACK)
                    buttons["UPDATE"].refresh()
                    buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_NORMAL | self.BLUE_BLACK)
                    buttons["BACK"].refresh()

                else:
                    buttons["UPDATE"].addstr(1, self.center_words(21, "UPDATE"), "UPDATE", curses.A_NORMAL | self.BLUE_BLACK)
                    buttons["UPDATE"].refresh()
                    buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_STANDOUT| self.GREEN_BLACK)
                    buttons["BACK"].refresh()

            key = self.stdscr.getkey()

        return

    def search(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str):
        # Update the Title of the Perform Area:
        perform_area.clear()
        perform_area.attron(self.GREEN_BLACK)
        perform_area.border()
        perform_area.attroff(self.GREEN_BLACK)
        perform_area.addstr(0, self.center_words(perform_area_width, f"SEARCH {main_choice}"), f"SEARCH {main_choice}", curses.A_BOLD)
        perform_area.refresh()

        # Search Text Box Containers:
        search_text_wins = {
            "UNIQUE VALUE": perform_area.subwin(3, 102, 10, self.screen_width - perform_area_width),
            "NAME": perform_area.subwin(3, 102, 15, self.screen_width - perform_area_width),
        }

        # Buttons:
        buttons = {
            "SEARCH": perform_area.subwin(4, 21, 35, (self.screen_width - perform_area_width) + 40),
            "BACK": perform_area.subwin(4, 21, 40, (self.screen_width - perform_area_width) + 40)
        }

        # Labeling Search Textbox Containers:
        for name, text_win in search_text_wins.items():
            text_win.border()
            text_win.addstr(0, 1, name, curses.A_BOLD)
            text_win.refresh()

        # Labeling Buttons:
        for name, button in buttons.items():
            button.border()
            button.addstr(1, self.center_words(21, name), name, self.BLUE_BLACK)
            button.refresh()

         # Search Text Boxes:
        pos_x_inc = 0
        search_text_boxes = []
        for name, text_win in search_text_wins.items():
            search_text_boxes.append(curses.newwin(1, 100, 11 + pos_x_inc, self.screen_width - perform_area_width + 1))
            pos_x_inc += 5

        search_text_wins["UNIQUE VALUE"].addstr(0, 1, "UNIQUE VALUE", curses.A_STANDOUT | self.BLUE_BLACK)
        search_text_wins["UNIQUE VALUE"].refresh()

        selection = 0
        search_texts = ["" for _ in search_text_wins]

        key = self.stdscr.getkey()

        # Search Loop:
        while True:

            if key == "KEY_UP":
                selection -= 1

            elif key == "KEY_DOWN":
                selection += 1

            elif key == "y" or key == "Y":

                # Textbox is Selected:
                if selection < 2:
                    search_texts[selection] = Textbox(search_text_boxes[selection]).edit().strip().replace("\n", "")

                # Search:
                elif selection == 2:
                    perform_area.clear()
                    perform_area.attron(self.GREEN_BLACK)
                    perform_area.border()
                    perform_area.attroff(self.GREEN_BLACK)
                    perform_area.addstr(0, self.center_words(perform_area_width, f"SEARCH {main_choice}"), f"SEARCH {main_choice}", curses.A_BOLD)
                    perform_area.refresh()
                    break

                # Back:
                else:
                    break

            elif key == "b" or key == "B":
                return

            # Reset Selection:
            if selection > 3:
                selection = 0;

            elif selection < 0:
                selection = 3

            # Normalize Buttons if they aren't Selected:
            if selection < 2:
                buttons["SEARCH"].addstr(1, self.center_words(21, "SEARCH"), "SEARCH", curses.A_NORMAL | self.BLUE_BLACK)
                buttons["SEARCH"].refresh()
                buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_NORMAL | self.BLUE_BLACK)
                buttons["BACK"].refresh()

                # Actions if Textbox is Selected:
                text_index = 0
                text_wins_names = list(search_text_wins.keys())

                for name, text_win in search_text_wins.items():
                    text_win.clear()
                    text_win.border()
                    text_win.addstr(0, 1, name, curses.A_BOLD)
                    text_win.addstr(1, 1, search_texts[text_index], curses.A_ITALIC)

                    if text_wins_names[selection] == name:
                        text_win.addstr(0, 1, name, curses.A_STANDOUT | self.BLUE_BLACK)

                    text_index += 1
                    text_win.refresh()

            # Actions if Buttons are Selected:
            else:

                # Search:
                if selection == 2:
                    buttons["SEARCH"].addstr(1, self.center_words(21, "SEARCH"), "SEARCH", curses.A_STANDOUT | self.GREEN_BLACK)
                    buttons["SEARCH"].refresh()
                    buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_NORMAL | self.BLUE_BLACK)
                    buttons["BACK"].refresh()

                else:
                    buttons["SEARCH"].addstr(1, self.center_words(21, "SEARCH"), "SEARCH", curses.A_NORMAL | self.BLUE_BLACK)
                    buttons["SEARCH"].refresh()
                    buttons["BACK"].addstr(1, self.center_words(21, "BACK"), "BACK", curses.A_STANDOUT| self.GREEN_BLACK)
                    buttons["BACK"].refresh()

            key = self.stdscr.getkey()

        return

    def view(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str):
        table_area = perform_area.subwin(perform_area_height - 4, perform_area_width - 4, 4, self.screen_width - perform_area_width)
        #table_area.border()
        table_area.refresh()

        username, password = "anderson", "Anderson#7"
        connection = Connection(user=username, password=password, database="Anderson")
        connection.begin()
        cursor = connection.cursor(cursor=Cursor)

        text = table(cursor, 2)

        table_area.addstr(1, 0, text)
        table_area.refresh()

        self.stdscr.getch()
        return

    def remove(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str):
        pass

    def issue_book(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str):
        pass

    def return_book(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str):
        pass

if __name__ == "__main__":
    wrapper(Application)