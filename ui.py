# ui.py
import tkinter as tk
from tkinter import ttk, Label
from constants import *


class UI:
    def __init__(self, root, state, drawing_controller):
        self.state = state
        self.drawing_controller = drawing_controller
        self.create_ui(root)
        self.blocks = {}
        self.block_row_counter = 1

    def create_ui(self, root):
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        #Диагностическая кнопка
        state_button = ttk.Button(self.frame, text="Состояние", command=self.state.print_state)
        state_button.grid(row=0, column=0, columnspan=3, pady=10)

        self.state["patient_info"] = {}

        self.state["patient_info"]["patient_name"] = self.create_entry(self.frame, "Ф.И.О.:", 1, "name")
        self.state["patient_info"]["patient_dob"] = self.create_entry(self.frame, "Дата рождения:", 2, "dob")
        self.state["patient_info"]["patient_id"] = self.create_entry(self.frame, "Номер истории болезни:", 3, "history_id")
        
        # Добавляем блок для выбора протокола
        self.state['protocol_label'] = ttk.Label(self.frame, text="Выберите протокол:")
        self.state['protocol_label'].grid(row=4, column=0, padx=5, pady=5)
        
        self.state["protocol_combobox"] = ttk.Combobox(self.frame, values=["ФЭГДС", "ФКС"])
        self.state["protocol_combobox"].grid(row=4, column=1, padx=5, pady=5)
        self.state["protocol_combobox"].bind("<<ComboboxSelected>>", self.update_localisation_combobox)

        # Создаем холст для блока контейнеров с вертикальным скроллбаром
        self.canvas = tk.Canvas(self.frame, height=450)
        self.canvas.grid(row=7, column=0, columnspan=5, sticky=tk.NSEW)

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=7, column=5, sticky=tk.NS)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Создаем контейнер внутри холста
        self.blocks_container = ttk.Frame(self.canvas)
        self.blocks_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Добавляем контейнер в холст
        self.canvas.create_window((0, 0), window=self.blocks_container, anchor="nw")

        export_button = ttk.Button(root, text="Экспорт в PDF", command=lambda: self.drawing_controller.export_to_pdf())
        export_button.grid(row=5, column=1, columnspan=3, pady=10)

        self.state["image_label"] = Label(root)
        self.state["image_label"].grid(row=0, column=1, padx=10, pady=10)
        self.drawing_controller.update_image()

    def update_localisation_combobox(self, event):
        protocol = self.state["protocol_combobox"].get()

        if protocol == "ФЭГДС":
            localisation_values = list(LOCALISATION_COORDINATES.keys())[0:8]
        elif protocol == "ФКС":
            localisation_values = list(LOCALISATION_COORDINATES.keys())[9:15]
        else:
            return

        # Удаляем старый комбобокс с выбором протокола
        self.state["protocol_combobox"].grid_forget()
        self.state['protocol_label'].grid_forget()

        # Обновляем label и создаем новый комбобокс для локализаций
        self.localisation_label = ttk.Label(self.frame, text="Локализация:")
        self.localisation_label.grid(row=6, column=0, padx=5, pady=5)

        self.state["localisation_combobox"] = ttk.Combobox(self.frame, values=localisation_values, state='readonly')
        self.state["localisation_combobox"].grid(row=6, column=1, padx=5, pady=5)
        self.state["localisation_combobox"].bind("<<ComboboxSelected>>", self.create_new_block)

    def create_new_block(self, event):
        selected_value = self.state["localisation_combobox"].get()

        # Добавление локализации в состояние
        if selected_value in self.state.get_localisations():
            return
        self.state.add_localisation(selected_value)
        
        # Создаем новый блок на основе выбранного значения
        loc_label = ttk.Label(self.blocks_container, text=f"{selected_value}:")
        loc_label.grid(row=self.block_row_counter, column=0, padx=5, pady=5)

        # Создаем кнопку удаления блока
        delete_button = ttk.Button(self.blocks_container, text="Удалить", command=lambda: self.delete_block(selected_value))
        delete_button.grid(row=self.block_row_counter, column=2, padx=5, pady=5)

        self.blocks[selected_value] = {
            'loc_label': loc_label,
            'form_label': [],
            'checkbuttons': [],
            'entries': [],
            'delete_button': delete_button  # Сохраняем ссылку на кнопку удаления
        }

        # Получаем список образований
        actual_formations = list(set(FORMATION_LIST) | set(FORMATION_EXTENSIONS.get(selected_value, [])))

        self.block_row_counter += 1

        for formation in actual_formations:
            # Создаем лейбл
            label = ttk.Label(self.blocks_container, text=f"{formation}:")
            label.grid(row=self.block_row_counter, column=0, sticky=tk.W)
            self.blocks[selected_value]['form_label'].append(label)

            # Создаем чекбокс с переменной типа BooleanVar и начальным значением False
            formation_var = tk.BooleanVar(value=False)
            formation_checkbox = ttk.Checkbutton(self.blocks_container, variable=formation_var)
            formation_checkbox.grid(row=self.block_row_counter, column=1, sticky=tk.W)
            self.blocks[selected_value]['checkbuttons'].append(formation_checkbox)
            self.drawing_controller.update_image()

            # Привязываем событие изменения состояния чекбокса к функции-обработчику
            def on_checkbox_change(*args, localisation=selected_value, formation=formation, formation_var=formation_var):
                if formation_var.get():
                    self.state.add_formation(localisation, formation)
                    self.drawing_controller.update_image()
                else:
                    self.state.delete_formation(localisation, formation)
                    self.drawing_controller.update_image()
            formation_var.trace_add("write", on_checkbox_change)

            # Создаем поле для ввода текста
            text_entry = ttk.Entry(self.blocks_container)
            text_entry.grid(row=self.block_row_counter, column=2)
            self.blocks[selected_value]['entries'].append(text_entry)

            # Привязка события KeyRelease к методу add_comment
            def on_text_change(event, localisation=selected_value, formation=formation):
                comment = event.widget.get()
                self.state.add_comment(localisation, formation, comment)
                self.drawing_controller.update_image()

            text_entry.bind("<KeyRelease>", on_text_change)

            # Переменная для отслеживания текущей строки
            self.block_row_counter += 1

    def delete_block(self, selected_value):
        # Удаление всех виджетов блока
        for widget in self.blocks[selected_value]['form_label']:
            widget.grid_forget()
        for widget in self.blocks[selected_value]['checkbuttons']:
            widget.grid_forget()
        for widget in self.blocks[selected_value]['entries']:
            widget.grid_forget()
        self.blocks[selected_value]['loc_label'].grid_forget()
        self.blocks[selected_value]['delete_button'].grid_forget()
        

        # Удаление блока из состояния
        self.state.delete_localisation(selected_value)
        del self.blocks[selected_value]
        self.drawing_controller.update_image()
        
    def create_entry(self, frame, label_text, row, data_type):
        label = ttk.Label(frame, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5)
        
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        
        # Привязка события KeyRelease к соответствующему методу обновления данных
        def on_key_release(event):
            value = event.widget.get()
            if data_type == "name":
                self.state.add_patient_name(value)
                self.drawing_controller.update_image()
            elif data_type == "dob":
                self.state.add_patient_dob(value)
                self.drawing_controller.update_image()
            elif data_type == "history_id":
                self.state.add_patient_id(value)
                self.drawing_controller.update_image()
    
        entry.bind("<KeyRelease>", on_key_release)
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

