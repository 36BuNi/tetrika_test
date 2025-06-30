from typing import Dict, List, Tuple


def appearance(intervals: Dict[str, List[int]]) -> int:
    """
    Вычисляет общее время одновременного присутствия ученика и учителя на уроке.

    :param intervals: Словарь с интервалами времени.
    :return: Общее время присутствия в секундах.
    """

    def merge_and_clip(intervals: List[int], min_val: int, max_val: int) -> List[Tuple[int, int]]:
        """
        Обрабатывает и объединяет интервалы времени.

        :param intervals: Список временных меток (вход/выход).
        :param min_val: Минимальное допустимое время (начало урока).
        :param max_val: Максимальное допустимое время (конец урока).
        :return: Список объединённых интервалов в виде кортежей (начало, конец).
        """
        paired: List[Tuple[int, int]] = []
        for i in range(0, len(intervals), 2):
            start: int = max(intervals[i], min_val)
            end: int = min(intervals[i + 1], max_val)
            if start < end:
                paired.append((start, end))

        if not paired:
            return []

        paired.sort()
        merged: List[Tuple[int, int]] = [paired[0]]

        for current in paired[1:]:
            last: Tuple[int, int] = merged[-1]
            if current[0] <= last[1]:
                merged[-1] = (last[0], max(last[1], current[1]))
            else:
                merged.append(current)

        return merged

    lesson_start: int
    lesson_end: int
    lesson_start, lesson_end = intervals['lesson']

    pupil_intervals: List[Tuple[int, int]] = merge_and_clip(intervals['pupil'], lesson_start, lesson_end)
    tutor_intervals: List[Tuple[int, int]] = merge_and_clip(intervals['tutor'], lesson_start, lesson_end)

    total: int = 0
    p_idx: int = 0
    t_idx: int = 0
    len_pupil: int = len(pupil_intervals)
    len_tutor: int = len(tutor_intervals)

    while p_idx < len_pupil and t_idx < len_tutor:
        p_start, p_end = pupil_intervals[p_idx]
        t_start, t_end = tutor_intervals[t_idx]

        overlap_start: int = max(p_start, t_start)
        overlap_end: int = min(p_end, t_end)

        if overlap_start < overlap_end:
            total += overlap_end - overlap_start

        if p_end < t_end:
            p_idx += 1
        else:
            t_idx += 1

    return total
