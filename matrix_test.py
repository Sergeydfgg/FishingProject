import calculations
from calculations import MatrixBorders as Mb
from collections import defaultdict


expected_range_to_text = {
    (Mb.low_danger_bottom.value, Mb.low_danger_up.value): 'Организация устойчива к угрозе',
    (Mb.mid_danger_bottom.value, Mb.mid_danger_up.value): 'Необходимы доп меры',
    (Mb.high_danger_bottom.value, Mb.high_danger_up.value): 'Ситуация критическая'
}

workers_results = defaultdict(int)


def check_result(probs_for_test: tuple[float, float, float],
                 expected_org_range: tuple[int or float, float or int]) -> None:
    result = calculations.calculate_result(probs_for_test)
    print(f'Тест для распределения {probs_for_test}\n')
    if Mb.low_danger_bottom.value <= result[0] < Mb.low_danger_up.value:
        print(f'Итог теста - {expected_range_to_text[(Mb.low_danger_bottom.value, Mb.low_danger_up.value)]}')
        print(f'Ожидаемый результат - {expected_range_to_text[expected_org_range]}\n')
    elif Mb.mid_danger_bottom.value <= result[0] < Mb.mid_danger_up.value:
        print(f'Итог теста - {expected_range_to_text[(Mb.mid_danger_bottom.value, Mb.mid_danger_up.value)]}')
        print(f'Ожидаемый результат - {expected_range_to_text[expected_org_range]}\n')
    elif Mb.high_danger_bottom.value <= result[0] <= Mb.high_danger_up.value:
        print(f'Итог теста - {expected_range_to_text[(Mb.high_danger_bottom.value, Mb.high_danger_up.value)]}')
        print(f'Ожидаемый результат - {expected_range_to_text[expected_org_range]}\n')
    else:
        print(f'Итог теста - вне критериев')
        print(f'Ожидаемый результат - {expected_range_to_text[expected_org_range]}\n')

    workers_len = result[1].__len__()
    for val in result[1]:
        if Mb.worker_low_danger_bottom.value <= val < Mb.worker_low_danger_up.value:
            workers_results['Сотрудник не опасен'] += 1
        elif Mb.worker_mid_danger_bottom.value <= val < Mb.worker_mid_danger_up.value:
            workers_results['Нужны доп меры'] += 1
        elif Mb.worker_high_danger_bottom.value <= val <= Mb.worker_high_danger_up.value:
            workers_results['Сотрудник опасен'] += 1
        else:
            workers_results['Выход за диапозон'] += 1

    print(f"Не опасных сотрудников - {workers_results['Сотрудник не опасен'] / workers_len * 100:.2f}%\n"
          f"Нужны меры - {workers_results['Нужны доп меры'] / workers_len * 100:.2f}%\n"
          f"Опасных сотрудников - {workers_results['Сотрудник опасен'] / workers_len * 100:.2f}%\n"
          f"Выходов за пределы оценки - {workers_results['Выход за диапозон'] / workers_len * 100:.2f}%")
