import time
import os
import random
import signal
import multiprocessing

import pyautogui
import keyboard
import cv2
import numpy as np


__VERSION__ = '1.0.0'


def hook(pid: int, keybind: str) -> None:
    """
    Постоянно проверяет, нажата ли конкретная клавиша.
    Если клавиша нажата, то отправляет сигнал SIGTERM указанному процессу
    и завершает процесс.

    Аргументы:
        pid (int): Идентификатор процесса, которому будет отправлен сигнал SIGTERM.
        keybind (str): Клавиша, которую нужно проверить.
    """
    while True:
        if keyboard.is_pressed(keybind):
            os.kill(pid, signal.SIGTERM)
            os._exit(1)


def find(template: str, threshold: float =0.9) -> tuple:
    """
    Находит расположение изображения-шаблона на экране.

    Аргументы:
        template (str): Путь к изображению-шаблону.
        threshold (float, optional): Пороговое значение для сравнения изображения-шаблона. Значение по умолчанию равно 0.9.

    Возвращает:
        tuple: Кортеж, содержащий координаты совпавшего изображения-шаблона.
    """
    # Получаем скриншот экрана.
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Переводим скриншот в оттенки серого.
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Настрой изображение на экране.
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    return loc


def click(template_path: str, tap_count: int, threshold: float =0.8) -> None:
    """
    Функция кликает по изображению на экране на основе заданного шаблона.

    Аргументы:
        template_path (str): Путь к изображению шаблона.
        tap_count (int): Количество кликов по изображению.
        threshold (float, optional): Порог соответствия изображению шаблону. Значение по умолчанию - 0.8.

    Эта функция принимает шаблон изображения, считывает его и преобразует в оттенки серого.
    Затем она делает скриншот и преобразует его в оттенки серого. Используется соответствие
    шаблонов для поиска расположения изображения на экране. Если изображение найдено, 
    то происходит клик по центру изображения с случайными смещениями. 
    Количество кликов определяется параметром tap_count. Функция выводит количество оставшихся 
    кликов для каждого клика.
    """
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Переводим скриншот в оттенки серого.
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Находим изображение на экране.
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    # Кликаем по найденным координатам.
    for pt in zip(*loc[::-1]):
        center_x = pt[0] + w // 2
        center_y = pt[1] + h // 2
        taps_left = tap_count
        for _ in range(tap_count):
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            x = center_x + offset_x
            y = center_y + offset_y
            interval = random.uniform(0.001, 0.3)
            pyautogui.click(x, y, interval=interval)
            taps_left -= 1
            print(f"{taps_left}/{tap_count}")
        break


if __name__ == "__main__":

    ENERGY = 5500
    ONE_TAP_ENERGY = 11
    
    # Ждем, пока пользователь нажмет клавишу запуска бота
    keybind_start = "`"
    print(f"Нажмите '{keybind_start}' для запуска бота")
    keyboard.wait(keybind_start)

    # Мониторим завершение работы бота по нажатию клавиши в отдельном процессе
    pid = os.getpid()
    keybind_exit = "-"
    multiprocessing.Process(target=hook, args=(pid, keybind_exit)).start()

    # Запускаем бота
    print("Бот запущен")

    # Загружаем изображение, которое мы хотим найти на экране. 0- в градациях серого.
    template = cv2.imread(f'..{os.sep}img{os.sep}energy.bmp', 0)

    while True:
        loc = find(template)

        for _ in zip(*loc[::-1]):
            offset_tap_count = random.randint(-100, 0)
            tap_count = ENERGY // ONE_TAP_ENERGY + offset_tap_count
            print(f"Tap count: {tap_count}")
            click(f'..{os.sep}img{os.sep}coin.bmp', tap_count)
            break

        print("Ожидание пополнения энергии")
        time.sleep(1500) # 25min
        print("Пополнение энергии завершено")
