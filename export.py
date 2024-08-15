# export.py

from fpdf import FPDF
from tkinter import filedialog

class ExportController:
    def __init__(self, state):
        self.state = state

    def export_to_pdf(self):
        """
        Метод для экспорта текущего состояния в PDF файл.
        """
        pdf = FPDF()
        pdf.add_page()
        
        # Добавление текста с информацией о пациенте
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Ф.И.О.: {self.state['patient_info']['name_entry'].get()}", ln=True)
        pdf.cell(200, 10, txt=f"Дата рождения: {self.state['patient_info']['dob_entry'].get()}", ln=True)
        pdf.cell(200, 10, txt=f"Номер истории болезни: {self.state['patient_info']['history_entry'].get()}", ln=True)
        pdf.ln(10)  # Переход на новую строку

        # Добавление информации о локализациях и образованиях
        for localisation, (_, _, formations) in self.state.state.items():
            pdf.cell(200, 10, txt=f"Локализация: {localisation}", ln=True)
            for formation, (present, comment) in formations.items():
                if present:
                    pdf.cell(200, 10, txt=f"  - {formation}: {comment}", ln=True)

        # Сохранение PDF
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=[("PDF files", "*.pdf"),
                                                           ("All files", "*.*")])
        if filepath:
            pdf.output(filepath)
