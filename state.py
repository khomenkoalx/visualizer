# state.py

from typing import Dict, List, Optional, Tuple
from constants import LOCALISATION_COORDINATES, TEXT_BLOCK_COORDINATES
from pprint import pprint
from geometry_utils import *

class State:
    def __init__(self):
        self.state: Dict[str, Tuple[Tuple[int, int], Tuple[int, int], Dict[str, str]]] = {}
        self.available_text_block_coord: List[Tuple[int, int]] = TEXT_BLOCK_COORDINATES.copy()
        self.data: Dict[str, Optional[str]] = {}

    def print_state(self) -> None:
        """Печатает содержимое словаря state в удобочитаемом виде"""
        pprint(self.state)
        pprint(self.get_patient_info())
        pprint(self.available_text_block_coord)
    
    def get_patient_info(self) -> List[Optional[str]]:
        """Возвращает информацию о пациенте"""
        patient_info: List[Optional[str]] = [
            self.data.get('patient_name'),
            self.data.get('patient_dob'),
            self.data.get('patient_id')
        ]
        return patient_info

    def __setitem__(self, key: str, value: str) -> None:
        self.data[key] = value

    def __getitem__(self, key: str) -> Optional[str]:
        return self.data.get(key)

    def add_patient_name(self, patient_name: str) -> None:
        """Добавляет имя пациента"""
        self.data['patient_name'] = patient_name

    def add_patient_dob(self, patient_dob: str) -> None:
        """Добавляет дату рождения пациента"""
        self.data['patient_dob'] = patient_dob

    def add_patient_id(self, patient_id: str) -> None:
        """Добавляет номер истории болезни пациента"""
        self.data['patient_id'] = patient_id

    def get_localisations(self) -> List[str]:
        """Возвращает список локализаций"""
        return list(self.state.keys())

    def add_localisation(self, localisation: str) -> None:
        """Добавляет локализацию в состояние"""
        if localisation not in LOCALISATION_COORDINATES:
            raise ValueError(f"Локализация {localisation} не найдена в LOCALISATION_COORDINATES.")
        self.state[localisation] = [
            LOCALISATION_COORDINATES[localisation],
            self.available_text_block_coord.pop(),
            {}
        ]
        self._check_and_solve_intersections()
        print(f"Добавлена {localisation}")

    def add_formation(self, localisation: str, formation: str) -> None:
        """Добавляет образование в указанную локализацию"""
        if localisation not in self.state:
            raise KeyError(f"Локализация {localisation} не найдена в состоянии.")
        self.state[localisation][2][formation] = ''
        print(f"Добавлена {formation}")

    def add_comment(self, localisation: str, formation: str, comment: str) -> None:
        """Добавляет комментарий к образованию в указанной локализации"""
        if localisation not in self.state:
            raise KeyError(f"Локализация {localisation} не найдена в состоянии.")
        if formation not in self.state[localisation][2]:
            raise KeyError(f"Образование {formation} не найдено в локализации {localisation}.")
        self.state[localisation][2][formation] = comment
        print(f"{localisation} и {formation} получили комментарий {comment}")

    def delete_formation(self, localisation: str, formation: str) -> None:
        """Удаляет образование из указанной локализации"""
        if localisation not in self.state:
            raise KeyError(f"Локализация {localisation} не найдена в состоянии.")
        if formation not in self.state[localisation][2]:
            raise KeyError(f"Образование {formation} не найдено в локализации {localisation}.")
        self.state[localisation][2].pop(formation)
        print(f"Удалена {formation}")

    def delete_localisation(self, localisation: str) -> None:
        """Удаляет локализацию из состояния"""
        if localisation not in self.state:
            raise KeyError(f"Локализация {localisation} не найдена в состоянии.")
        coords_for_return = self.state.pop(localisation)
        self.available_text_block_coord.append(coords_for_return[1])
        print(f"Удалена {localisation}")

    def _check_and_solve_intersections(self) -> None:
        """Проверяет пересечения между локализациями и решает их"""
        for i_key, i_item in self.state.items():
            for j_key, j_item in self.state.items():
                if i_key != j_key:
                    seg1 = i_item[0:2]
                    seg2 = j_item[0:2]
                    if segments_intersect(seg1, seg2):
                        print('Найдено пересечение')
                        self.state[i_key][1], self.state[j_key][1] = self.state[j_key][1], self.state[i_key][1]
