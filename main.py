import tkinter as tk
from state import State
from drawing import DrawingController
from ui import UI
from constants import IMAGE_PATH


def main() -> None:
    """
    Основная функция для запуска приложения.
    """
    # Создание корневого окна
    root = tk.Tk()
    root.title("Визуализация образований ЖКТ")

    # Создание объекта состояния
    state = State()

    # Создание контроллера для работы с изображением
    drawing_controller = DrawingController(state, IMAGE_PATH)

    # Создание пользовательского интерфейса
    ui = UI(root, state, drawing_controller)

    # Запуск главного цикла приложения
    root.mainloop()


if __name__ == "__main__":
    main()
