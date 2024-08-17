# drawing.py

from PIL import Image, ImageTk, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
import os
import math
import time
from constants import OUTPUT_PATH, FONT_REGULAR, FONT_BOLD

class DrawingController:
    def __init__(self, state, image_path):
        self.state = state
        self.image_path = image_path
        self.image = None
        self.font = ImageFont.truetype(FONT_REGULAR, size=10)
        self.font_bold = ImageFont.truetype(FONT_BOLD, size=10)

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
                text_coords[0] + 10 if text_coords[0] > 300 else text_coords[0] - 150, 
                text_coords[1]
            )
            block_text = f"{localisation}"
            for formation, comment in formations.items():
                block_text += f"\n- {formation} ({comment})"
            draw.text(text_coords_abs, block_text, font=self.font_bold, fill="black")


    def arrow(self, start, end):
        """
        Вспомогательная функция для создания координат стрелки
        """
        arrowhead_size = 0  # Размер наконечника стрелки
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
        # Преобразование ImageTk.PhotoImage в Pillow Image
        pil_image = ImageTk.getimage(self.image)

        # Получаем текущую временную метку
        timestamp = time.strftime("%Y%m%d_%H%M%S")

        # Формируем имя файла с временной меткой
        patient_info = self.state.get_patient_info()[0]
        pdf_filename = f"{OUTPUT_PATH}/{patient_info}_{timestamp}.pdf"

        # Создаем папку для результатов экспорта, если ее нет
        os.makedirs(f"{OUTPUT_PATH}", exist_ok=True)

        # Устанавливаем альбомную ориентацию страницы A4
        page_width, page_height = landscape(A4)

        # Создаем PDF-документ
        c = canvas.Canvas(pdf_filename, pagesize=(page_width, page_height))

        # Получаем размеры изображения
        img_width, img_height = pil_image.size

        # Рассчитываем коэффициент масштабирования для сохранения соотношения сторон
        aspect_ratio = img_width / img_height
        if img_width > page_width or img_height > page_height:
            if img_width / page_width > img_height / page_height:
                img_width = page_width
                img_height = page_width / aspect_ratio
            else:
                img_height = page_height
                img_width = page_height * aspect_ratio

        # Рассчитываем координаты для центрирования изображения на странице
        x = (page_width - img_width) / 2
        y = (page_height - img_height) / 2

        # Сохраняем изображение во временный файл
        temp_filename = "temp_image.png"
        pil_image.save(temp_filename)

        # Вставляем изображение в PDF с сохранением соотношения сторон
        c.drawImage(temp_filename, x, y, width=img_width, height=img_height)

        # Закрываем PDF-документ
        c.save()

        # Удаляем временный файл (опционально)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)