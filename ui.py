# ui.py
import tkinter as tk
from tkinter import ttk, Label

class UI:
    def __init__(self, root, state, drawing_controller):
        self.state = state
        self.drawing_controller = drawing_controller
        self.create_ui(root)

    def create_ui(self, root):
        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.state["patient_info"] = {}

        self.state["patient_info"]["name_entry"] = self.create_entry(frame, "Ф.И.О.:", 1)
        self.state["patient_info"]["dob_entry"] = self.create_entry(frame, "Дата рождения:", 2)
        self.state["patient_info"]["history_entry"] = self.create_entry(frame, "Номер истории болезни:", 3)

        self.create_blocks_container(frame)

        export_button = ttk.Button(frame, text="Экспорт в PDF", command=self.drawing_controller.export_to_pdf)
        export_button.grid(row=6, column=0, columnspan=3, pady=10)

        self.state["image_label"] = Label(root)
        self.state["image_label"].grid(row=0, column=1, padx=10, pady=10)
        self.drawing_controller.update_image()

    def create_entry(self, frame, label_text, row):
        label = ttk.Label(frame, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entry.bind("<KeyRelease>", lambda event: self.drawing_controller.update_image())
        return entry

    def create_blocks_container(self, frame):
        self.state["blocks_canvas"] = tk.Canvas(frame)
        self.state["blocks_canvas"].grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.state["blocks_canvas"].yview)
        scrollbar.grid(row=5, column=3, sticky="ns")
        self.state["blocks_canvas"].configure(yscrollcommand=scrollbar.set)

        self.state["blocks_frame"] = ttk.Frame(self.state["blocks_canvas"])
        self.state["blocks_canvas"].create_window((0, 0), window=self.state["blocks_frame"], anchor="nw")

        self.state["blocks_frame"].bind("<Configure>", lambda e: self.state["blocks_canvas"].configure(
            scrollregion=self.state["blocks_canvas"].bbox("all")
        ))
