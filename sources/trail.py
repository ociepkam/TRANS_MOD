from psychopy import visual
import random
import numpy as np
from copy import deepcopy
from os.path import join
from numpy.random import choice
from sources.parameters import SIGN, FIGURES


class Trial:
    def __init__(self, k, n, ans_type):
        self.k = k
        self.n = n
        self.ans_type = ans_type
        self.pairs = None
        self.answers = None
        self.figures = list(choice(deepcopy(FIGURES), self.n, replace=False))
        self.prepare_pairs()
        self.check_sign()
        self.prepare_answers()

    @staticmethod
    def reverse_pair(pair, to_reverse=("sign", "symbols")):
        if "sign" in to_reverse:
            pair["sign"] = SIGN[1] if pair["sign"] == SIGN[0] else SIGN[0]
        if "symbols" in to_reverse:
            pair["left"], pair["right"] = pair["right"], pair["left"]
        return pair

    def prepare_one_pair(self, left, right, sign=0):
        pair = {"left": left, "sign": SIGN[sign], "right": right}
        if random.randint(0, 1):
            pair = self.reverse_pair(pair)
        return pair

    def check_sign(self):
        if all([pair["sign"] == SIGN[0] for pair in self.pairs]) or \
                all([pair["sign"] == SIGN[1] for pair in self.pairs]):
            to_change = random.randint(0, len(self.pairs) - 1)
            self.pairs[to_change] = self.reverse_pair(self.pairs[to_change])

    def prepare_pairs(self):
        if self.n == 4:
            self.pairs = [self.prepare_one_pair(0, 1),
                          self.prepare_one_pair(2, 3)]
        elif self.n == 5:
            self.pairs = [self.prepare_one_pair(0, 1),
                          self.prepare_one_pair(2, 3),
                          self.prepare_one_pair(random.choice([0, 1, 2, 3]), 4)]
        elif self.n == 6:
            self.pairs = [self.prepare_one_pair(0, 1),
                          self.prepare_one_pair(2, 3),
                          self.prepare_one_pair(4, 5)]

        for i in range(self.k - len(self.pairs)):
            while True:
                fig1, fig2 = np.sort(choice(range(self.n), 2, replace=False))
                pair = self.prepare_one_pair(fig1, fig2)
                if pair not in self.pairs and self.reverse_pair(pair) not in self.pairs:
                    self.pairs.append(pair)
                    break

        print(self.pairs)
        random.shuffle(self.pairs)

    def prepare_answers(self):
        rest_pairs = deepcopy(self.pairs)
        good_answers = choice(rest_pairs, 2, False)
        rest_pairs.remove(good_answers[0])
        rest_pairs.remove(good_answers[1])
        self.answers = [self.reverse_pair(ans) for ans in good_answers]
        self.answers[0]["corr"] = 1
        self.answers[1]["corr"] = 1
        if self.ans_type == 2:
            bad_answers = [self.reverse_pair(answer, choice(["sign", "symbols"])) for answer in deepcopy(self.answers)]
        elif self.ans_type == 3:
            bad_answers = [self.reverse_pair(choice(deepcopy(self.answers)), choice(["sign", "symbols"])),
                           self.reverse_pair(choice(rest_pairs), choice(["sign", "symbols"]))]
        elif self.ans_type == 4:
            bad_answers = [self.reverse_pair(pair, choice(["sign", "symbols"])) for pair in choice(rest_pairs, 2, False)]
        else:
            raise Exception("ans_typ has to be 2, 3 or 4")
        print(bad_answers)
        bad_answers[0]["corr"] = 0
        bad_answers[1]["corr"] = 0
        self.answers += bad_answers
        print(self.answers)
        random.shuffle(self.answers)

    def prepare_to_draw(self, win, config):
        for i, pair in enumerate(self.pairs):
            x_column_offset = (-(config["n_columns"]-1) * 0.5 + (i % config["n_columns"])) * config["columns_offset"]

            x = config["task_pos"][0] + (i - (self.k - 1) * 0.5) * config["task_offset"][0] + x_column_offset
            y = config["task_pos"][1] + (int(i/config["n_columns"]) - (self.k - 1) * 0.5) * config["task_offset"][1]
            left = visual.ImageStim(win=win, image=join('images', self.figures[pair["left"]]),
                                    interpolate=True, size=config["fig_size"], pos=(x - config["pair_offset"], y))
            sign = visual.TextStim(win=win, text=pair["sign"], color='black', height=config["sign_size"], pos=(x, y))
            right = visual.ImageStim(win=win, image=join('images', self.figures[pair["right"]]),
                                     interpolate=True, size=config["fig_size"], pos=(x + config["pair_offset"], y))
            pair["draw"] = [left, sign, right]

        for i, pair in enumerate(self.answers):
            x = config["answers_pos"][0] + (i - (len(self.answers) - 1) * 0.5) * config["answers_offset"][0]
            y = config["answers_pos"][1] + (i - (len(self.answers) - 1) * 0.5) * config["answers_offset"][1]
            print(x, y)
            left = visual.ImageStim(win=win, image=join('images', self.figures[pair["left"]]),
                                    interpolate=True, size=config["fig_size"], pos=(x - config["pair_offset"], y))
            sign = visual.TextStim(win=win, text=pair["sign"], color='black', height=config["sign_size"], pos=(x, y))
            right = visual.ImageStim(win=win, image=join('images', self.figures[pair["right"]]),
                                     interpolate=True, size=config["fig_size"], pos=(x + config["pair_offset"], y))
            pair["draw"] = [left, sign, right]

            pair["frame"] = visual.Rect(win, width=config["frame_width"], height=config["frame_height"],
                                        opacity=0, lineColor=config["frame_click_color"], pos=[x, y],
                                        lineWidth=config["frame_line_width"])

    def draw(self, log):
        for pair in self.pairs:
            for elem in pair["draw"]:
                elem.setAutoDraw(log)
        for pair in self.answers:
            for elem in pair["draw"]:
                elem.setAutoDraw(log)
            pair["frame"].setAutoDraw(log)

    def __str__(self):
        print("k: ", self.k)
        print("n: ", self.n)
        print("ans_type: ", self.ans_type)
        print([str(e["left"]) + e["sign"] + str(e["right"]) for e in self.pairs])
        print([str(e["left"]) + e["sign"] + str(e["right"]) for e in self.answers])
        return ""
