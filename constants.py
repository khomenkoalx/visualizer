# constants.py
from geometry_utils import segments_intersect



# Список с названиями образований
FORMATION_LIST = (
    'Полип', 'Опухоль', 'Язва', 'Пятно',
    'Атрофия', 'Дивертикул', 'Вена',
    'Геморроидальный узел', 'Стеноз',
    'Эрозия', 'Инородное тело', 'Метаплазия'
)

# Словарь с локализациями и их координатами на изображении
LOCALISATION_COORDINATES = {
    'Пищевод верхняя треть': (445, 125),
    'Пищевод средняя треть': (445, 175),
    'Пищевод нижняя треть': (445, 225),
    'Кардиальный отдел желудка': (440, 300),
    'Тело желудка': (500, 300),
    'Антральный отдел желудка': (450, 325),
    'Пилорический канал': (430, 335),
    'Двенадцатиперстная кишка': (390, 360),
    'Терминальный отдел подвздошной кишки': (380, 525),
    'Слепая кишка': (340, 530),
    'Восходящая ободочная кишка': (330, 450),
    'Поперечная ободочная кишка': (430, 410),
    'Нисходящая ободочная кишка': (540, 450),
    'Сигмовидная кишка': (510, 540),
    'Прямая кишка': (435, 565)
}

# Относительные координаты для подписей
# (в процентах от ширины и высоты изображения)
TEXT_BLOCK_COORDINATES = [
    (0.15, 0.2),
    (0.85, 0.05),
    (0.15, 0.5),
    (0.85, 0.3),
    (0.15, 0.85),
    (0.85, 0.55),
    (0.85, 0.80),
]

"""Использовать словарь EXTRA_OPTIONS чтобы при выведении в UI списка
возможных образований для конкретной локализации не использовать весь список
FORMATION_LIST. FORMATION_LIST должен содержать только те образования, которые
встречаются в любой локализации. Таким образом список образований для
локализации будет составляться из FORMATION_LIST и расширяться списком из
v.
"""
FORMATION_EXTENSIONS = {
    'Пищевод нижняя треть': ['Вена'],
    'Прямая кишка': ['Геморроидальный узел']
}


"""
STATE = {
    localisation: [loc_coord, text_block_coord,
                   {
                       formation: [presence, comment]
                   }
                   ]
}
"""


class Application:
    def __init__(self):
        pass

    def render_state(self):
        pass


class State(Application):
    """
    Класс состояния, описывающим имеющиеся локализации, образования
    и комментарии.
    """
    def __init__(self):
        """
        Инициализация экземпляра класса. Экземпляр хранит переменные:
        1. Словарь состояния (self.state), хранящий информацию для дальнейшего
        рендеринга.
        2. Множество использованных координат текстовых блоков для проверки
        пересечений линий, соединяющих координату локализации и текстового
        блока.
        """
        self.state = dict()
        self.available_text_block_coord = TEXT_BLOCK_COORDINATES.copy()

    def __str__(self):
        return f'{self.state}'

    def add_localisation(self, localisation):
        """
        Метод добавления локализации.
        При добавлении новой локализации

        Параметры:
        - localisation (str): Название локализации в строгом соответствии со
        словарем LOCALISATION_COORDINATES

        """
        self.state[localisation] = [LOCALISATION_COORDINATES[localisation],
                                    self.available_text_block_coord.pop(),
                                    dict()
                                    ]
        self._check_and_solve_intersections()

    def add_formation(self, localisation, formation):
        """
        Метод добавления образования для конкретной локализации.

        Параметры:
        - localisation (str): Название локализации в соответствии со словарем
        LOCALISATION_COORDINATES.
        - formation (str): Название образования в соответствии со списком
        FORMATION_LIST.
        """
        self.state[localisation][2].update({formation: [True, '']})

    def _check_and_solve_intersections(self):
        """
        Приватный метод для поиска пересечений между координатами локализации
        и текстового блока. Для выполнения использует импортируемую функцию
        segment_intersect().
        Принцип работы - проходит по словарю self.state, попарно оценивает
        наличие пересечений между парами линий, соединяющих координату
        локализации на рисунке и координату текстового блока. При наличии
        таких пересечений проводит обмен значений координат текстового блока
        между локализациями.
        """
        for i_key, i_item in self.state.items():
            for j_key, j_item in self.state.items():
                if i_item != j_item:
                    seg1 = i_item[0:2]
                    seg2 = j_item[0:2]
                    if segments_intersect(seg1, seg2):
                        print('Найдено пересечение')
                        print(self.state)
                        self.state[i_key][1], self.state[j_key][1] = self.state[j_key][1], self.state[i_key][1]
                        print(self.state)

    def add_comment(self, localisation, formation, comment):
        self.state[localisation][2][formation][1] = comment

    def delete_formation(self, localisation, formation):
        self.state[localisation][2].pop(formation)

    def delete_localisation(self, localisation):
        self.state.pop(localisation)


endo = State()

endo.add_localisation('Тело желудка')
print('!')

endo.add_localisation('Слепая кишка')
print('!')

endo.add_localisation('Восходящая ободочная кишка')
print('!')

endo.add_localisation('Нисходящая ободочная кишка')
print('!')

endo.add_localisation('Поперечная ободочная кишка')
print('!')

endo.add_localisation('Пищевод нижняя треть')
print('!')

endo.add_localisation('Пищевод средняя треть')
print('!')

endo.add_formation('Пищевод средняя треть', 'Вена')
endo.add_comment('Пищевод средняя треть', 'Вена', 'БОЛЬШАЯ ВЕНА')
print("!!!")
print(endo)