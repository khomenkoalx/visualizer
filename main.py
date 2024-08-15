import tkinter as tk
from state import State
from drawing import DrawingController
from ui import UI

def main():
    root = tk.Tk()
    root.title("Image Editor")

    # Создание объекта состояния
    state = State()

    # Создание контроллера для работы с изображением
    drawing_controller = DrawingController(state, 'resourses/digest.png')

    # Создание пользовательского интерфейса
    ui = UI(root, state, drawing_controller)

    # Запуск главного цикла приложения
    root.mainloop()

if __name__ == "__main__":
    main()
