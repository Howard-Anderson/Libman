"""
                    Library Management System:
    
    Author: Howard Anderson.

    Date: 17/06/2024.

    Description: Library Management System.

    Filename: main.py.

"""

# Curses Imports:
import curses
from curses import wrapper
from curses.textpad import Textbox
import time

# PyMySQL Imports:
from pymysql.connections import Connection
from pymysql.cursors import Cursor

# Libman Imports:
from Libman import Library 

# JSON Imports:
import json

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

        # Library:
        with open("config.txt", "r") as config_file:
            params = json.load(config_file)
        
        connection = Connection(user=params["username"], password=params["password"], database=params["database"])
        connection.begin()
        self.library = Library(connection)

        self.main_menu()

        connection.close()


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
            button_names = ("USERS", "BOOKS", "TRANSACTIONS", "EXIT")
            buttons = self.initialize_containers("BUTTON", button_names, main_win, 20, 20)

            # Labeling Buttons:
            self.normalize_containers("BUTTON", buttons)

            # User - Highlight the Button:
            buttons["USERS"].addstr(2, self.center_words(21, "USERS"), "USERS", curses.A_STANDOUT | self.GREEN_BLACK)
            buttons["USERS"].refresh()

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
                    if button_names[selection] in button_names[:-1]:
                        self.second_win(main_win, main_win_width, button_names[selection])
                        break
                    else:
                        return

                # Reset the Selection Variable:
                if selection < 0:
                    selection = 3

                elif selection > 3:
                    selection = 0

                # Perform the Scrolling action by Changing the Highlighted Button.
                self.highlight(buttons = buttons, selection = selection)

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

            button_names = ("TRANSACT", "UPDATE", "SEARCH", "VIEW", "REMOVE", "BACK")
            buttons = self.initialize_containers("BUTTON", button_names, main_win, 20, 20)
            actions = {
                "TRANSACT": self.transact,
                "UPDATE": self.update,
                "SEARCH": self.search,
                "VIEW": self.view,
                "REMOVE": self.remove
            }

        else:

            button_names = ("ADD", "UPDATE", "SEARCH", "VIEW", "REMOVE", "BACK")
            buttons = self.initialize_containers("BUTTON", button_names, main_win, 20, 20)
            actions = {
                "ADD": self.add,
                "UPDATE": self.update,
                "SEARCH": self.search,
                "VIEW": self.view,
                "REMOVE": self.remove
            }

        # Name the Buttons and Apply Border:
        self.normalize_containers("BUTTON", buttons)

        # Highlight the First Button:
        if main_choice == "TRANSACTIONS":
            buttons["TRANSACT"].addstr(2, self.center_words(21, "TRANSACT"), "TRANSACT", curses.A_STANDOUT | self.GREEN_BLACK)
            buttons["TRANSACT"].refresh()

        else:
            buttons["ADD"].addstr(2, self.center_words(21, "ADD"), "ADD", curses.A_STANDOUT | self.GREEN_BLACK)
            buttons["ADD"].refresh()

        # Perform Area Window variables:
        perform_area_width = self.screen_width - 75
        perform_area_height = self.screen_height - 4
        pos_x = 2
        pos_y = (self.screen_width - perform_area_width) - 3 # Leave Space for Buttons.

        # Perform Area Window:
        perform_area = main_win.subwin(perform_area_height, perform_area_width, pos_x, pos_y)
        self.update_pa_title(perform_area, perform_area_width, "PERFORM AREA")

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

                if button_names[selection] in button_names[:-1]:
                    actions[button_names[selection]](perform_area, perform_area_height, perform_area_width, main_choice)

                # Back Button -> Go to previous Window and follow the Main Window Loop:
                else:
                    return

            # Back Key -> Go to previous Window and follow the Main Window Loop:
            elif key == "b" or key == "B":
                main_win.clear()
                return

            # Reset to keep in bounds:
            if selection < 0:
                selection = 5

            elif selection > 5:
                selection = 0

            # Highlight the Selected Button:
            self.highlight(buttons=buttons, selection=selection)

            key = self.stdscr.getkey()

        return


    def add(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str) -> None:
        """
            Add Records to the Users and Books.
        """
        # Update the Title of the Perform Area:
        self.update_pa_title(perform_area, perform_area_width, f"ADD {main_choice}")

        # Text Box Containers:
        if main_choice == "USERS":

            text_win_names = ("NAME", "AGE", "PHONE NUMBER", "JOIN DATE")
            text_wins = self.initialize_containers("TEXT BOX CONTAINER", text_win_names, perform_area, 10, self.screen_width - perform_area_width)

        else:

            text_win_names = ("NAME", "AUTHOR", "PURCHASE DATE", "PRICE")
            text_wins = self.initialize_containers("TEXT BOX CONTAINER", text_win_names, perform_area, 10, self.screen_width - perform_area_width)

        # Buttons:
        button_names = ("SAVE", "BACK")
        buttons = self.initialize_containers("BUTTON", button_names, perform_area, 35, (self.screen_width - perform_area_width) + 40)

        # Labeling Text Box Containers:
        self.normalize_containers("TEXT BOX CONTAINER", text_wins)

        # Labeling Buttons:
        self.normalize_containers("BUTTON", buttons)

        perform_area.refresh()

        # Text Boxes:
        text_boxes = self.initialize_textboxes(len(text_wins), 11, self.screen_width - perform_area_width + 1)

        # Highlight the Name TextBox:
        text_wins["NAME"].border()
        text_wins["NAME"].addstr(0, 1, "NAME", curses.A_STANDOUT | self.BLUE_BLACK)
        text_wins["NAME"].refresh()

        # Action to be performed when Selected:
        def actions(selection: int, texts: list[str]) -> list[str]:
            if selection <= 3:
                texts[selection] = Textbox(text_boxes[selection]).edit().strip().replace("\n", "")

            elif selection == 4:
                message = self.library.add(texts, main_choice)
                perform_area.addstr(30, (self.screen_width - perform_area_width), message, curses.A_BOLD | self.BLUE_BLACK)
                perform_area.refresh()


            else:
                self.update_pa_title(perform_area, perform_area_width, f"ADD {main_choice}")
                return texts

            return texts

        # Scroll through the Containers and perform action:
        self.scroll(buttons=buttons, yes_actions=actions, text_wins=text_wins, text_boxes=text_boxes)

        return

    def update(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str) -> None:
        """
            Updates a specific record.
            Basis of Update:
                USERS and BOOKS: "UNIQUE VALUE"
                TRANSACTIONS: "USER UNIQUE" and "BOOK UNIQUE"
        """
        # Update the Title of the Perform Area:
        self.update_pa_title(perform_area, perform_area_width, f"UPDATE {main_choice}")

        # Update Text Box Containers:
        if main_choice == "USERS":

            update_text_win_names = ("UNIQUE VALUE", "NAME", "AGE", "PHONE NUMBER", "JOIN DATE")
            

        elif main_choice == "BOOKS":

            update_text_win_names = ("UNIQUE VALUE", "NAME", "AUTHOR", "PRICE", "PURCHASE DATE")
        
        elif main_choice == "TRANSACTIONS":

            update_text_win_names = ("USER UNIQUE", "BOOK UNIQUE", "TRANSACTION DATE", "TRANSACTION TYPE")
        
        update_text_wins = self.initialize_containers("TEXT BOX CONTAINER", update_text_win_names, perform_area, 10, self.screen_width - perform_area_width)

        # Buttons:
        update_button_names = ("UPDATE", "BACK")
        update_buttons = self.initialize_containers("BUTTON", update_button_names, perform_area, 35, (self.screen_width - perform_area_width) + 40)

        # Labeling Update Textbox Containers:
        self.normalize_containers("TEXT BOX CONTAINER", update_text_wins)

        # Labeling Buttons:
        self.normalize_containers("BUTTON", update_buttons)

        # Update Text Boxes:
        update_text_boxes = self.initialize_textboxes(len(update_text_wins), 11, self.screen_width - perform_area_width + 1)
        
        if main_choice == "USERS" or main_choice == "BOOKS":
            update_text_wins["UNIQUE VALUE"].addstr(0, 1, "UNIQUE VALUE", curses.A_STANDOUT | self.BLUE_BLACK)
            update_text_wins["UNIQUE VALUE"].refresh()
        
        else:
            update_text_wins["USER UNIQUE"].addstr(0, 1, "USER UNIQUE", curses.A_STANDOUT | self.BLUE_BLACK)
            update_text_wins["USER UNIQUE"].refresh()

        # Action to be performed:
        def update_actions(selection: int, texts: list[str]) -> list[str]:
            update_texts = texts
            if selection < len(update_text_wins):
                update_texts[selection] = Textbox(update_text_boxes[selection]).edit().strip().replace("\n", "")

            elif selection == len(update_text_wins):
                message = self.library.update(update_texts, main_choice)
                perform_area.addstr(30, 20, message, self.BLUE_BLACK)
                perform_area.refresh()
            
            else:
                return update_texts

            return update_texts

        self.scroll(buttons=update_buttons, yes_actions=update_actions, text_wins=update_text_wins, text_boxes=update_text_boxes, texts=["" for _ in update_text_wins])

        return

    def search(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str) -> None:
        """
            Searches for Entries in the DB.
        """
        # Update the Title of the Perform Area:
        self.update_pa_title(perform_area, perform_area_width, f"SEARCH {main_choice}")
        
        # Search Text Box Containers:
        if main_choice == "USERS" or main_choice == "BOOKS":
            
            search_text_win_names = ("UNIQUE VALUE", "NAME")
        else:
            search_text_win_names = ("USER UNIQUE", "BOOK UNIQUE")

        search_text_wins = self.initialize_containers("TEXT BOX CONTAINER", search_text_win_names, perform_area, 10, self.screen_width - perform_area_width)

        # Buttons:
        button_names = ("SEARCH", "BACK")
        search_buttons = self.initialize_containers("BUTTON", button_names, perform_area, 35, (self.screen_width - perform_area_width) + 40)

        # Labeling Search Textbox Containers:
        self.normalize_containers("TEXT BOX CONTAINER", search_text_wins)

        # Labeling Buttons:
        self.normalize_containers("BUTTON",search_buttons)

        # Search Text Boxes:
        search_text_boxes = self.initialize_textboxes(len(search_text_wins), 11, self.screen_width - perform_area_width + 1)

        if main_choice == "USERS" or main_choice == "BOOKS":
            search_text_wins["UNIQUE VALUE"].addstr(0, 1, "UNIQUE VALUE", curses.A_STANDOUT | self.BLUE_BLACK)
            search_text_wins["UNIQUE VALUE"].refresh()
        else:
            search_text_wins["USER UNIQUE"].addstr(0, 1, "UNIQUE VALUE", curses.A_STANDOUT | self.BLUE_BLACK)
            search_text_wins["USER UNIQUE"].refresh()

        search_texts = ""

        def search_actions(selection: int, texts: list[str]) -> list[str]:
            if selection <= 1:
                texts[selection] = Textbox(search_text_boxes[selection]).edit().strip().replace("\n", "")

            elif selection == 2:
                nonlocal search_texts
                search_texts = self.library.search(texts, main_choice)
                
                # Table Area:
                table_area = perform_area.subwin(perform_area_height - 4, perform_area_width - 4, 4, self.screen_width - perform_area_width)
                #table_area.border()
                table_area.refresh()

                start = 0
                limit = 20
                record_count = self.library.get_record_count(main_choice)

                if record_count < limit:
                    limit = record_count

                key = ""
                
                # Scrolling Loop to View Search Results:
                while True:
                    end = start + limit
                    

                    if key == "KEY_UP":
                        start -= 1
                        end -= 1
            
                    elif key == "KEY_DOWN":
                        start += 1
                        end += 1
            
                    elif key.upper() == "B":
                        break

                    if start > (record_count - limit):
                        start = 0
                        end = limit
            
                    elif start < 0:
                        start = (record_count - limit)
                        end = record_count

                    
                    table_area.clear()
                    table_area.addstr(1, 0, search_texts)
                    table_area.refresh()
                    key = self.stdscr.getkey()
                
                self.update_pa_title(perform_area=perform_area, perform_area_width=perform_area_width, title=f"SEARCH {main_choice}")
            
            elif selection == 3:
                return

            return texts
        
        self.scroll(buttons=search_buttons, yes_actions=search_actions, text_wins=search_text_wins, text_boxes=search_text_boxes)

        return

    def view(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str) -> None:
        """
            Shows all the Entries from the DB.
        """
        # Table Area to view the Table:
        table_area = perform_area.subwin(perform_area_height - 4, perform_area_width - 4, 4, self.screen_width - perform_area_width)
        #table_area.border()
        table_area.refresh()

        start = 0
        limit = 20
        record_count = self.library.get_record_count(main_choice)

        if record_count < limit:
            limit = record_count
        
        while True:
            end = start + limit
            key = self.stdscr.getkey()

            if key == "KEY_UP":
                start -= 1
                end -= 1
            
            elif key == "KEY_DOWN":
                start += 1
                end += 1
            
            elif key.upper() == "B":
                break

            if start > (record_count - limit):
                start = 0
                end = limit
            

            elif start < 0:
                start = (record_count - limit)
                end = record_count


            text = self.library.view(start, end, main_choice)
            table_area.clear()
            table_area.addstr(1, 0, text)
            table_area.refresh()

        return

    def remove(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str) -> None:
        """
            Remove Item / Entry.
        """
        # Update the Title of the Perform Area:
        self.update_pa_title(perform_area, perform_area_width, f"REMOVE {main_choice}")

        if main_choice != "TRANSACTIONS":
            
            text_win_names = ("UNIQUE VALUE")
            text_wins = {"UNIQUE VALUE": perform_area.subwin(3, 100, 10, self.screen_width - perform_area_width)}
        
        else:

            text_win_names = ("USER UNIQUE", "BOOK UNIQUE")
            text_wins = self.initialize_containers("TEXT BOX CONTAINER", text_win_names, perform_area, 10, self.screen_width - perform_area_width)

        # # Text Box Containers:
        # text_wins = self.initialize_containers("TEXT BOX CONTAINER", text_win_names, perform_area, 10, self.screen_width - perform_area_width)

        # Buttons:
        button_names = ("REMOVE", "BACK")
        buttons = self.initialize_containers("BUTTON", button_names, perform_area, 35, (self.screen_width - perform_area_width) + 40)

        # Text Boxes:
        text_boxes = self.initialize_textboxes(len(text_wins), 11, self.screen_width - perform_area_width + 1)

        # Labeling Text Box Containers:
        self.normalize_containers("TEXT BOX CONTAINER", text_wins)

        # Labeling Butttons:
        self.normalize_containers("BUTTON", buttons)

        # Highlight First Container:
        if main_choice == "USERS" or main_choice == "BOOKS":
            text_wins["UNIQUE VALUE"].addstr(0, 1, "UNIQUE VALUE", curses.A_STANDOUT | self.BLUE_BLACK)
            text_wins["UNIQUE VALUE"].refresh()
        else:
            text_wins["USER UNIQUE"].addstr(0, 1, "USER UNIQUE", curses.A_STANDOUT | self.BLUE_BLACK)
            text_wins["USER UNIQUE"].refresh()


        # Actions to be Performed on Selection:
        def actions(selection: int, texts: list[str]) -> list[str]:
            if selection < len(text_wins):
                texts[selection] = Textbox(text_boxes[selection]).edit().strip().replace("\n", "")

            # Remove:
            elif selection == len(text_wins): # Remove Button Index.
                    message = self.library.remove(texts, main_choice)
                    perform_area.addstr(30, (self.screen_width - perform_area_width), message, self.BLUE_BLACK)
                    perform_area.refresh()
            # Back:
            else:
                return

            return texts

        # Scroll through the Containers and perform action:
        self.scroll(buttons, actions, text_wins, text_boxes)

        return


    def transact(self, perform_area: curses.window, perform_area_height: int, perform_area_width: int, main_choice: str) -> None:
        """
            Only use: TRANSACTIONS: To enter a transaction.
        """
        # Update the Title of the Perform Area:
        self.update_pa_title(perform_area, perform_area_width, f"MAKE {main_choice}")

        # Text Box Containers:
        text_wins_names = ("USER UNIQUE", "BOOK UNIQUE", "TRANSACTION DATE", "TRANSACTION TYPE")
        text_wins = self.initialize_containers("TEXT BOX CONTAINER", text_wins_names, perform_area, 10, self.screen_width - perform_area_width)

        # Buttons
        button_names = ("SAVE", "BACK")
        buttons = self.initialize_containers("BUTTON", button_names, perform_area, 35, (self.screen_width - perform_area_width) + 40)

        # Labeling Text Box Containers:
        self.normalize_containers("TEXT BOX CONTAINER", text_wins)

        # Labeling Buttons:
        self.normalize_containers("BUTTON", buttons)

        # Text Boxes:
        text_boxes = self.initialize_textboxes(len(text_wins), 11, self.screen_width - perform_area_width + 1)

        # Highlight First Text Box Containers:
        text_wins["USER UNIQUE"].addstr(0, 1, "USER UNIQUE", curses.A_STANDOUT | self.BLUE_BLACK)
        text_wins["USER UNIQUE"].refresh()

        # Actions to be Performed on Selection:
        def actions(selection: int, texts: list[str]) -> list[str]:
            if selection < 4:
                texts[selection] = Textbox(text_boxes[selection]).edit().strip().replace("\n", "")

            # Save
            elif selection == 4:
                message = self.library.transact(texts)
                perform_area.addstr(30, (self.screen_width - perform_area_width), message, self.BLUE_BLACK)
                perform_area.refresh()
            # Back
            else:
                return


            return texts

        # Scroll through the Containers and perform action:
        self.scroll(buttons, actions, text_wins, text_boxes)

        return

    def update_pa_title(self, perform_area: curses.window, perform_area_width: int, title: str) -> None:
        """
            Updates Perform Area Title.
        """
        perform_area.clear()
        perform_area.attron(self.GREEN_BLACK)
        perform_area.border()
        perform_area.attroff(self.GREEN_BLACK)
        perform_area.addstr(0, self.center_words(perform_area_width, title), title, curses.A_BOLD)
        perform_area.refresh()


    def scroll(self, buttons: dict[str: curses.window], yes_actions: callable, text_wins: dict[str: curses.window] = None, text_boxes: list[curses.window] = None, texts: list[str] = None) -> str:
        """
            Scroll through the Containers in a Loop and perform the action.
        """
        # Get the total number of Containers.
        containers_len = len(text_wins) + len(buttons) - 1 if text_boxes else len(buttons) - 1
        #print(f"{containers_len = }")

        # Initialize Texts to keep track of Inputs passed through Text Box, if Text Box is passed
        if text_wins:
            if texts is None:
                texts = ["" for _ in text_wins]
        else:
            texts = None

        selection = 0

        key = self.stdscr.getkey()

        while True:

            if key == "KEY_UP":
                selection -= 1

            elif key == "KEY_DOWN":
                selection += 1

            elif key.upper() == "Y":
                if text_wins:
                    texts = yes_actions(selection, texts)

                    if selection == containers_len or selection == containers_len - 1:
                        break

                else:
                    if selection == containers_len:
                        return "EXIT"

                    yes_actions(selection)

            elif key.upper() == "B":
                return

            elif key.upper() == "Q":
                return

            if selection < 0:
                selection = containers_len

            elif selection > containers_len:
                selection = 0

            self.highlight(buttons=buttons, text_wins=text_wins, texts=texts, selection=selection)

            key = self.stdscr.getkey()

        return texts


    def initialize_containers(self, container_type: str, names: tuple[str], window: curses.window, start_row_pos: int, col_pos: int) -> dict[str: curses.window]:
        """
            Initializes Containers.
            Containers: "TEXT BOX CONTAINER", "BUTTON".

            container_size = (rows, cols)
        """
        if container_type.upper() == "TEXT BOX CONTAINER":

            container_size = (3, 102)

        elif container_type.upper() == "BUTTON":

            container_size = (5, 21)

        else:
            raise Exception(f"\n[ ! ]: CONTAINER TYPE PASSED IS NOT SUPPORTED : {container_type}\n")

        # Position One after another below by 5 upto the len(names).
        return dict(zip(names, [window.subwin(*container_size, start_row_pos + increment, col_pos) for increment in range(0, 5 * len(names), 5)]))

    def initialize_textboxes(self, number: int, start_row_pos: int, col_pos: int) -> list[curses.window]:
        """
            Initializes Text Boxes.
        """
        return [curses.newwin(1, 100, start_row_pos + increment, col_pos) for increment in range(0, 5 * number, 5)]


    def normalize_containers(self, container_type: str, containers: curses.window) -> None:
        """
            Styles the Containers to Normal Format.

            Containers: "TEXT BOX CONTAINER", "BUTTON"
        """

        for name, container in containers.items():
            container.border()

            if container_type == "TEXT BOX CONTAINER":
                container.addstr(0, 1, name, curses.A_BOLD)

            elif container_type == "BUTTON":
                container.addstr(2, self.center_words(21, name), name, curses.A_NORMAL | self.BLUE_BLACK)

            else:
                raise Exception(f"\n[ ! ]: Container Not Supported: {name}\n")

            container.refresh()


    def highlight(self, buttons: dict[str: curses.window], text_wins: dict[str: curses.window] = None, texts: list[str] = None, selection: int = 0) -> None:
        """
            If Selection, Highlights the Components,
            else, Normalizes the Components.

            Components: TextBoxes[Optional] and Buttons.

            Note:
                This function absolutely requires, Buttons and Selection to be passed.
                It can be used to Highlight Buttons if they are alone passed,
                but can't be used if text_wins is only passed.
        """
        # If TextBox is also Passed:
        if text_wins is not None:

            # If a Text Box is Selected:
            if selection < len(text_wins):

                # Normalize Buttons:
                for name, button in buttons.items():
                    button.addstr(2, self.center_words(21, name), name, curses.A_NORMAL | self.BLUE_BLACK)
                    button.refresh()

                # Normalize TextBoxes:
                for index, (name, text_win) in enumerate(text_wins.items()):
                    text_win.clear()
                    text_win.border()
                    text_win.addstr(0, 1, name, curses.A_BOLD)
                    text_win.addstr(1, 1, texts[index], curses.A_ITALIC)

                    # Highlight the Selected TextBox:
                    if index == selection:
                        text_win.addstr(0, 1, name, curses.A_STANDOUT | self.BLUE_BLACK)

                    text_win.refresh()

                return

            # If a Button is Selected:
            else:

                # Reset the Selection, so that it can be used to iterate using loop:
                selection = selection - len(text_wins)

        # If Button is Selected:
        # Normalize Buttons:
        for index, (name, button) in enumerate(buttons.items()):
            button.addstr(2, self.center_words(21, name), name, curses.A_NORMAL | self.BLUE_BLACK)

            # Highlight the Selected Button:
            if index == selection:
                button.addstr(2, self.center_words(21, name), name, curses.A_STANDOUT | self.GREEN_BLACK)

            button.refresh()

if __name__ == "__main__":
    wrapper(Application)
