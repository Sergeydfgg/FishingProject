import pandas as pd
from random import uniform
from statistics import mean
import enum


class MatrixBorders(enum.Enum):
    low_danger_bottom = 0
    low_danger_up = 0.5
    mid_danger_bottom = 0.5
    mid_danger_up = 1
    high_danger_bottom = 1
    high_danger_up = 2
    worker_low_danger_bottom = 0
    worker_low_danger_up = 0.6
    worker_mid_danger_bottom = 0.6
    worker_mid_danger_up = 1.3
    worker_high_danger_bottom = 1.3
    worker_high_danger_up = 2


def prepare_data() -> list[str]:
    with open('available_workers.txt', 'r', encoding='utf-8') as file_to_read:
        data = file_to_read.read()
        abc = [chr(i) for i in range(1072, 1072+33)]
        clr_data = "".join([ltr for ltr in data.lower() if ltr in abc or ltr in [' ', ',', '-']]).split(',')
        return list(map(str.strip, clr_data))[:-1]


def calc_prob(probs: tuple[float, float, float]) -> int:
    cur_prob = uniform(0, 1)
    for ind, prob in enumerate(probs):
        if (cur_prob := cur_prob - prob) < 0:
            return ind


def gen_data(probs: tuple[float, float, float]) -> list[int]:
    return [calc_prob(probs) for _ in range(0, 5)]


def calc_res(clr_data: list[str], probs: tuple[float, float, float]) -> tuple[float, list[float]]:
    dict_to_df = {key.capitalize(): gen_data(probs) for key in clr_data}
    df = pd.DataFrame.from_dict(dict_to_df)
    return df.mean().mean(), [df[worker.capitalize()].mean() for worker in clr_data]


def calculate_result(probs: tuple[float, float, float]) -> tuple[float, list[float]]:
    data_to_send = prepare_data()
    res = [calc_res(data_to_send, probs) for _ in range(100)]
    worker_res = [mean([res[j][1][i] for j in range(100)]) for i in range(len(res[0][1]) - 1)]
    return mean(list(map(lambda val: val[0], res))), worker_res
