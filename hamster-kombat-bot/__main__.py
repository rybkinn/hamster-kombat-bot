import time
import os

import pyautogui
import cv2
import numpy as np


def change() -> None:
    global work
    work = not work


work = False


def find(template_path: str, threshold: float =0.9, interval: float =1) -> None:
    """
    Находит шаблон изображения на экране и при его обнаружении выполняет указанное действие.

    Args:
        template_path (str): путь к файлу шаблона изображения.
        threshold (float, optional): минимальный порог сходства для сопоставления шаблонов. По умолчанию 0,9.
        interval (float, optional): интервал между каждой проверкой шаблона. По умолчанию 1.
    """

    # Загружаем изображение, которое мы хотим найти на экране. 0- в градациях серого.
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    try:
        while True:
            if work:

                # Получаем скриншот экрана.
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

                # Переводим скриншот в оттенки серого.
                gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                # Находим изображение на экране.
                result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
                loc = np.where(result >= threshold)

                for _ in zip(*loc[::-1]):
                    click(f'img{os.sep}coin.bmp', interval=0.3)
                    break
                time.sleep(interval)
    
    except KeyboardInterrupt:
        print('\nВыход из программы')


def click(template_path: str, threshold: float =0.8, interval: float =0.0001) -> None:
    """
    Кликает по изображению на экране на основе шаблонного изображения.

    Args:
        template_path (str): Путь к шаблонному изображению.
        threshold (float, optional): Минимальный порог сходства для сопоставления шаблонов. По умолчанию 0.8.
        interval (float, optional): Интервал между каждым кликом. По умолчанию 0.0001.

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
        for _ in range(260):
            pyautogui.doubleClick(center_x, center_y, interval=interval)
        break


if __name__ == "__main__":
    find(f'img{os.sep}energy.bmp')
