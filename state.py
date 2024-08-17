# state.py
from constants import LOCALISATION_COORDINATES, TEXT_BLOCK_COORDINATES

class State:
    def __init__(self):
        self.state = {}
        self.available_text_block_coord = TEXT_BLOCK_COORDINATES.copy()
        self.data = {}  # To store additional data like patient_info

    def print_state(self):
        # Печатает содержимое словаря state в удобочитаемом виде
        from pprint import pprint
        pprint(self.state)
        pprint(self.get_patient_info())
        pprint(self.available_text_block_coord)
    
    def get_patient_info(self):
        patient_info = [self.data.get('patient_name'),
                        self.data.get('patient_dob'), self.data.get('patient_id')]
        return patient_info

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data.get(key)

    def add_patient_name(self, patient_name):
        self.data['patient_name'] = patient_name

    def add_patient_dob(self, patient_dob):
        self.data['patient_dob'] = patient_dob

    def add_patient_id(self, patient_id):
        self.data['patient_id'] = patient_id

    def get_localisations(self):
        return self.state.keys()

    def add_localisation(self, localisation):
        self.state[localisation] = [
            LOCALISATION_COORDINATES[localisation],
            self.available_text_block_coord.pop(),
            {}
        ]
        self._check_and_solve_intersections()
        print(f"Добавлена {localisation}")

    def add_formation(self, localisation, formation):
        self.state[localisation][2].update({formation: ''})
        print(f"Добавлена {formation}")

    def add_comment(self, localisation, formation, comment):
        self.state[localisation][2][formation][1] = comment
        print(f"{localisation} и {formation} получили комментарий {comment}")

    def delete_formation(self, localisation, formation):
        self.state[localisation][2].pop(formation)
        print(f"Удалена {formation}")

    def delete_localisation(self, localisation):
        coords_for_return = self.state.pop(localisation)
        self.available_text_block_coord.append(coords_for_return[1])
        print(f"Удалена {localisation}")


    def _check_and_solve_intersections(self):
        for i_key, i_item in self.state.items():
            for j_key, j_item in self.state.items():
                if i_item != j_item:
                    seg1 = i_item[0:2]
                    seg2 = j_item[0:2]
                    if segments_intersect(seg1, seg2):
                        print('Найдено пересечение')
                        self.state[i_key][1], self.state[j_key][1] = self.state[j_key][1], self.state[i_key][1]

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Коллинеарные
    elif val > 0:
        return 1  # По часовой стрелке
    else:
        return 2  # Против часовой стрелки

def on_segment(p, q, r):
    if min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1]):
        return True
    return False

def segments_intersect(seg1, seg2):
    p1, q1 = seg1
    p2, q2 = seg2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, q1, p2):
        return True
    if o2 == 0 and on_segment(p1, q1, q2):
        return True
    if o3 == 0 and on_segment(p2, q2, p1):
        return True
    if o4 == 0 and on_segment(p2, q2, q1):
        return True

    return False
