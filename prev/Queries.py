
# PyMySQL Imports:
from pymysql.connections import Connection
from pymysql.cursors import Cursor

# Curses Imports:
import curses
from curses import wrapper
from curses.textpad import Textbox

# Termtable Imports:
import termtables as tt

TEXT = ""
CURSOR = None

def view(cursor: Cursor) -> tuple:
    # View all Records:
    cursor.execute(f"SELECT * FROM test0")
    rows = cursor.fetchall()
    #print(f"\nRecords: {rows}")
    return rows

def schema(cursor: Cursor) -> tuple:
    # Schema:
    cursor.execute(f"DESCRIBE Anderson.test0")
    rows = cursor.fetchall()
    #print(f"\nSchema: {rows}")
    return rows

def row_count(cursor: Cursor) -> int:
    # Get Row Count:
    cursor.execute(f"SELECT COUNT(unique_value) FROM test0")
    record_count = cursor.fetchall()
    #print(f"\nRecord Count: {record_count}")
    return record_count[0][0]

def insert(cursor: Cursor) -> None:
    # Insert Into Table:
    value = int(input("\nEnter the Number of Records to Insert: "))
    record_count = row_count(cursor)
    phone_number = "8637653901"
    for record in range(record_count + 1, 1 + record_count + value) :
        cursor.execute(f"INSERT INTO test0(unique_value, name, phone_number) VALUES({record}, \"{username}\", \"{phone_number}\")")

def get_col_names(cursor) -> list:
    # Get Column Names:
    cols = schema(cursor)
    col_names = [col[0] for col in cols]
    #print(f"\nColumn Names: {col_names}")
    return col_names

def fetch(cursor, num, limit) -> tuple:
    # Fetch Particular Number of Rows:
    cursor.execute(f"SELECT * FROM test0 WHERE unique_value >= {num} LIMIT {limit}")
    rows = cursor.fetchall()
    #print(f"\nRecords: {rows}")
    return rows


def table(cursor, num, limit) -> str:
    # Table:
    records = fetch(cursor, num, limit)
    col_names = get_col_names(cursor)
    text = tt.to_string(
        records,
        header = col_names,
        style = tt.styles.ascii_thin_double)
    return text

def curses_screen(stdscr):
    (rows, cols) = (curses.LINES, curses.COLS)
    stdscr.clear()
    stdscr.border()
    stdscr.refresh()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_BLACK = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    BLACK_GREEN = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    BLACK_YELLOW = curses.color_pair(3)

    main_win = curses.newwin(rows - 2, cols - 2, 1, 1)
    #main_win.bkgd(" ", BLACK_GREEN)
    main_win.border()
    main_win.refresh()

    win1 = main_win.subwin(rows - 4, cols - 4, 2, 2)
    win1.bkgd(" ", BLACK_GREEN)
    win1.border()
    win1.addstr(0, int(cols / 2), "WINDOW - 1", curses.A_STANDOUT)
    win1.refresh()

    # win1.addstr(TEXT)
    # win1.refresh()
    #
    # stdscr.getch()

    win1.clear()

    width = cols - 75
    height = rows - 12
    pos_y = cols - width
    print(f"{ width = }  {pos_y = }")
    win2 = win1.subwin(height, width, 5, pos_y - 3)
    win2.border()
    win2.refresh()
    stdscr.getch()

    win2.clear()
    # text = table(CURSOR, 2)
    # win1.addstr(text)
    # win1.refresh()
    #
    # stdscr.getch()

if __name__ == "__main__":
    # Open Connection:
    username, password = "anderson", "Anderson#7"
    connection = Connection(user=username, password=password, database="Anderson")
    connection.begin()
    cursor = connection.cursor(cursor=Cursor)

    #records = view(cursor)
    #schema(cursor)
    #insert(cursor)
    #view(cursor)
    #col_names = get_col_names(cursor)

    TEXT = table(cursor, 0)
    CURSOR = cursor

    wrapper(curses_screen)

    # Close Connection:
    connection.commit()
    cursor.close()
    connection.close()
