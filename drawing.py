# drawing.py

from PIL import Image, ImageDraw, ImageTk, ImageFont
from tkinter import Label
from constants import LOCALISATION_COORDINATES
import math

class DrawingController:
    def __init__(self, state, image_path):
        self.state = state
        self.image_path = image_path
        self.image = None
        self.font = ImageFont.truetype("resourses/Arial.ttf", size=10)
        self.font_bold = ImageFont.truetype("resourses/Arial-Bold.ttf", size=10)

    def update_image(self):
        # Загрузка изображения
        image = Image.open(self.image_path)
        self.draw_patient_info(image)
        self.draw_arrows(image)
        self.draw_blocks(image)
        # Преобразование изображения для отображения в Tkinter
        self.image = ImageTk.PhotoImage(image)

        # Обновление виджета изображения
        self.state["image_label"].configure(image=self.image)
        self.state["image_label"].image = self.image # Сохраняем ссылку на изображение, чтобы не было сборки мусора

    def draw_patient_info(self, image):
        draw = ImageDraw.Draw(image)

        patient_info = self.state.get_patient_info()
        text = f"Ф.И.О. пациента {patient_info[0]}\nДата рождения {patient_info[1]}\nНомер истории болезни {patient_info[2]}" or ""
        x, y = 10, 10  # Начальные координаты для текста

        # Добавление текста на изображение
        draw.text((x, y), text, font=self.font, fill="black")



    def draw_arrows(self, image):
        """
        Метод для рисования стрелок, соединяющих локализацию и блоки текста.
        Использует координаты из self.state.
        """
        if self.state:
            draw = ImageDraw.Draw(image)
            for localisation, (loc_coords, text_coords, formations) in self.state.state.items():
                text_coords_abs = (
                    text_coords[0],  # перевод относительных координат в абсолютные
                    text_coords[1]
                )
                draw.line([loc_coords, text_coords_abs], fill="black", width=2)
                draw.polygon(self.arrow(loc_coords, text_coords_abs), fill="black")

    def draw_blocks(self, image):
        """
        Метод для рисования текстовых блоков с описанием локализации и образований.
        """
        draw = ImageDraw.Draw(image)
        for localisation, (loc_coords, text_coords, formations) in self.state.state.items():
            text_coords_abs = (
                text_coords[0],  # перевод относительных координат в абсолютные
                text_coords[1]
            )
            block_text = f"{localisation}"
            for formation, (present, comment) in formations.items():
                if present:
                    block_text += f"\n- {formation} ({comment})"
            draw.text(text_coords_abs, block_text, font=self.font_bold, fill="black")

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
