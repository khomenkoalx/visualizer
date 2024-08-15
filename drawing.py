# drawing.py

from PIL import Image, ImageDraw, ImageTk
from tkinter import Label
from constants import LOCALISATION_COORDINATES

class DrawingController:
    def __init__(self, state, image_path):
        self.state = state
        self.image_path = image_path
        self.image = None

    def update_image(self):
        image = Image.open(self.image_path)  # Загрузка изображения
        self.image = ImageTk.PhotoImage(image)

        self.state["image_label"].configure(image=self.image)
        self.state["image_label"].image = self.image  # Сохраняем ссылку на изображение, чтобы не было сборки мусора

    def draw_arrows(self, draw):
        """
        Метод для рисования стрелок, соединяющих локализацию и блоки текста.
        Использует координаты из self.state.
        """
        for localisation, (loc_coords, text_coords, formations) in self.state.state.items():
            text_coords_abs = (
                text_coords[0] * 600,  # перевод относительных координат в абсолютные
                text_coords[1] * 600
            )
            draw.line([loc_coords, text_coords_abs], fill="black", width=2)
            draw.polygon(self.arrow(loc_coords, text_coords_abs), fill="black")

    def draw_blocks(self, draw):
        """
        Метод для рисования текстовых блоков с описанием локализации и образований.
        """
        for localisation, (loc_coords, text_coords, formations) in self.state.state.items():
            text_coords_abs = (
                text_coords[0] * 600,  # перевод относительных координат в абсолютные
                text_coords[1] * 600
            )
            block_text = f"{localisation}:"
            for formation, (present, comment) in formations.items():
                if present:
                    block_text += f"\n- {formation} ({comment})"
            draw.text(text_coords_abs, block_text, fill="black")

    def arrow(self, start, end):
        """
        Вспомогательная функция для создания координат стрелки
        """
        arrowhead_size = 10  # Размер наконечника стрелки
        angle = math.atan2(end[1] - start[1], end[0] - start[0]) + math.pi

        return [
            (end[0] + arrowhead_size * math.cos(angle - math.pi / 6),
             end[1] + arrowhead_size * math.sin(angle - math.pi / 6)),
            end,
            (end[0] + arrowhead_size * math.cos(angle + math.pi / 6),
             end[1] + arrowhead_size * math.sin(angle + math.pi / 6))
        ]

    def add_block(self):
        """
        Метод добавления блока локализации.
        """
        # Здесь будет логика добавления нового блока.

    def export_to_pdf(self):
        """
        Метод экспорта изображения в PDF.
        """
        # Здесь будет логика экспорта изображения в PDF.
