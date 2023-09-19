import subprocess
import time

import keyboard
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import ChromiumOptions
from webdriver_manager.chrome import ChromeDriverManager

piece_types = ['wp', 'wb', 'wn', 'wr', 'wq', 'wk', 'bp', 'bb', 'bn', 'br', 'bq', 'bk']


def to_int(array):
    num = 0
    for i in range(len(array)):
        num <<= 8
        num += array[i]
    return num


def main():
    options = ChromiumOptions()
    options.add_argument(r"user-data-dir=%userprofile%\AppData\Local\Google\Chrome\User Data")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://www.chess.com/')

    color = 'b'

    while not keyboard.is_pressed("shift+w") and not keyboard.is_pressed("shift+b"):
        pass
    if keyboard.is_pressed("shift+w"):
        color = 'w'

    print("started")
    board = driver.find_element(By.CLASS_NAME, 'board')
    size = int(float(board.value_of_css_property('width')[:-2]))
    offset = size/8

    def move_piece(start, end):
        start_x = start % 8
        start_y = start // 8
        end_x = end % 8
        end_y = end // 8

        print(((end_x + 0.5) * offset)-size/2, ((end_y + 0.5) * offset)-size/2)
        ActionChains(driver)\
            .move_to_element_with_offset(board, -(((start_x + 0.5) * offset)-size/2), -(((start_y + 0.5) * offset)-size/2))\
            .click_and_hold()\
            .move_to_element_with_offset(board, -(((end_x + 0.5) * offset)-size/2), -(((end_y + 0.5) * offset)-size/2))\
            .click()\
            .perform()

    def parse_position():
        state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for piece in board.find_elements(By.CLASS_NAME, "piece"):
            try:
                data = piece.get_attribute("class").split(" ")
                if data[2][0] == 's':
                    eposition = data[2][-2:]
                    ptype = data[1]
                else:
                    eposition = data[1][-2:]
                    ptype = data[2]
                position = (7 - (int(eposition[0]) - 1)) + 8 * (int(eposition[1]) - 1)
                state[piece_types.index(ptype)] |= 1 << position
            except IndexError:
                pass
        return state

    # make the moves
    engine = subprocess.Popen(
        r'path to engine',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    def write_data():
        position = parse_position()
        for state in position:
            engine.stdin.write((str(state) + "\n").encode())
            engine.stdin.flush()

    def read_data():
        return int(engine.stdout.readline()), int(engine.stdout.readline())

    last_read = None
    engine.stdin.write(color.encode())
    engine.stdin.flush()
    flag = True
    while not keyboard.is_pressed("shift+q"):
        state = parse_position()
        if state != last_read:
            if not flag:
                flag = True
            else:
                write_data()
                pos = read_data()
                print(pos)
                move_piece(*pos)
                flag = False
            last_read = state

    engine.stdin.close()
    engine.stdout.close()
    engine.kill()
    driver.close()


if __name__ == '__main__':
    main()
