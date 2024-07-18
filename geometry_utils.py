def orientation(p, q, r):
    """Функция для определения ориентации тройки точек (p, q, r)"""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # коллинеарные
    elif val > 0:
        return 1  # по часовой стрелке
    else:
        return 2  # против часовой стрелки


def on_segment(p, q, r):
    """Функция для проверки, лежит ли точка r на отрезке pq"""
    if min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1]):
        return True
    return False


def segments_intersect(seg1, seg2):
    """Функция для проверки пересечения двух отрезков"""
    p1, q1 = seg1
    p2, q2 = seg2

    # Вычисляем ориентации
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # Общий случай
    if o1 != o2 and o3 != o4:
        return True

    # Специальные случаи (когда точки коллинеарны)
    # p1, q1 и p2 коллинеарны и p2 лежит на отрезке p1q1
    if o1 == 0 and on_segment(p1, q1, p2):
        return True

    # p1, q1 и q2 коллинеарны и q2 лежит на отрезке p1q1
    if o2 == 0 and on_segment(p1, q1, q2):
        return True

    # p2, q2 и p1 коллинеарны и p1 лежит на отрезке p2q2
    if o3 == 0 and on_segment(p2, q2, p1):
        return True

    # p2, q2 и q1 коллинеарны и q1 лежит на отрезке p2q2
    if o4 == 0 and on_segment(p2, q2, q1):
        return True

    # Если ни одно из условий не выполняется, значит отрезки не пересекаются
    return False
