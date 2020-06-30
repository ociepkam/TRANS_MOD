import atexit
from psychopy import visual, event, core, logging
from os.path import join
import csv
import random
import time

from sources.check_exit import check_exit
from sources.experiment_info import experiment_info
from sources.load_data import load_config, replace_polish
from sources.screen import get_screen_res, get_frame_rate
from sources.show_info import show_info
from sources.trail import Trial

part_id, part_sex, part_age, date = experiment_info()
NAME = "{}_{}_{}".format(part_id, part_sex[:1], part_age)
RAND = str(random.randint(100, 999))

RESULTS = list()
RESULTS.append(["NR", "trial_type", "k", "n", "ans_type", "corr1", "corr2", "acc", "rt1", "rt2"])


@atexit.register
def save_beh():
    # logging.flush()
    with open(join('results', 'behavioral', 'beh_{}_{}.csv'.format(NAME, RAND)), 'w') as f:
        beh_writer = csv.writer(f)
        beh_writer.writerows(RESULTS)


def prepare_trials(info, rand):
    trials = []
    for elem in info:
        assert elem["n"] in [4, 5, 6], "n has to be 4, 5 or 6"
        assert elem["k"] in [4, 6], "k has to be 4 or 6"
        assert elem["ans_typ"] in [2, 3, 4], "ans_typ has to be 2, 3 or 4"
        trials += [[elem["k"], elem["n"], elem["ans_typ"]]] * elem["nr"]
        print(trials)
    if rand:
        random.shuffle(trials)
    return trials


def run_trial(win, k, n, ans_type, config, feedback, feedb):
    response_clock = core.Clock()
    trial = Trial(k,  n, ans_type)
    trial.prepare_to_draw(win, config)

    acc = None
    corr = [None, None]
    rt = []
    trial.draw(True)
    win.callOnFlip(response_clock.reset)
    event.clearEvents()
    win.flip()

    clicked = []
    while response_clock.getTime() < config["trial_time"] and len(clicked) < 2:
        for idx, ans in enumerate(trial.answers):
            if mouse.isPressedIn(ans["frame"]) and ans["frame"].opacity == 0:
                rt.append(response_clock.getTime())
                ans["frame"].opacity = 1
                clicked.append(idx)
                win.flip()
                time.sleep(config["click_show_time"])
                ans["frame"].opacity = 0
                win.flip()
        if config["trial_time"] - response_clock.getTime() < config['SHOW_CLOCK']:
            clock_image.setAutoDraw(True)
        check_exit(config["exit_key"])
        win.flip()
    if len(clicked):
        corr[0] = trial.answers[clicked[0]]["corr"]
    if len(set(clicked)) == 2:
        corr[1] = trial.answers[clicked[1]]["corr"]
    acc = 1 if corr[0] and corr[1] else 0

    if feedback:
        for ans in trial.answers:
            if ans["corr"]:
                ans["frame"].lineColor = config["frame_answer_color"]
                ans["frame"].opacity = 1
        if acc and len(set(clicked)) == 2:
            feedb["pos"].setAutoDraw(True)
        elif len(clicked) == 2:
            feedb["neg"].setAutoDraw(True)
        else:
            feedb["no"].setAutoDraw(True)
        win.flip()
        if config["feedback_time"] > 0:
            time.sleep(config["feedback_time"])
        else:
            key = event.waitKeys(["space", config["exit_key"]])
            if key == config["exit_key"]:
                logging.critical('Experiment finished by user! {} pressed.'.format(key))
                exit(1)
    for _, v in feedb.items():
        v.setAutoDraw(False)
    trial.draw(False)
    clock_image.setAutoDraw(False)
    win.flip()
    time.sleep(config["wait_time"])
    rt += [None, None]
    return corr[0], corr[1], acc, rt[0], rt[1]


config = load_config()
SCREEN_RES = get_screen_res()
win = visual.Window(SCREEN_RES, fullscr=True, monitor='testMonitor', units='pix', color='Gainsboro')
FRAMES_PER_SEC = get_frame_rate(win)
mouse = event.Mouse(visible=True)

clock_image = visual.ImageStim(win=win, image=join('images', 'clock.png'), interpolate=True,
                               size=config['CLOCK_SIZE'], pos=config['CLOCK_POS'])

pos_feedb = visual.TextStim(win, text=replace_polish(config["pos_feedb"]), color='black', height=40, pos=(0, -200))
neg_feedb = visual.TextStim(win, text=replace_polish(config["neg_feedb"]), color='black', height=40, pos=(0, -200))
no_feedb = visual.TextStim(win, text=replace_polish(config["no_feedb"]), color='black', height=40, pos=(0, -200))
feedb = {"pos": pos_feedb, "neg": neg_feedb, "no": no_feedb}

# TRAINING
mean_acc = 0
data_train = prepare_trials(config["training"], config["train_trials_randomize"])

while mean_acc < config["min_training_acc"]:
    show_info(win, join('.', 'messages', "instruction1.txt"), text_size=config['TEXT_SIZE'],
              screen_width=SCREEN_RES[0], key=config["exit_key"])
    # show_image(window, 'instruction.png', SCREEN_RES, , key=config["exit_key"])
    mean_acc = 0
    i = 1
    for k, n, ans_type in data_train:
        corr1, corr2, acc, rt1, rt2 = run_trial(win, k, n, ans_type, config, config["feedback_in_training"], feedb)

        RESULTS.append([i, "train", k, n, ans_type, corr1, corr2, acc, rt1, rt2])
        i += 1
        mean_acc += 1 if acc else 0
    if i > 1:
        mean_acc /= (i - 1)
    else:
        break

# EXPERIMENT
show_info(win, join('.', 'messages', "instruction2.txt"), text_size=config['TEXT_SIZE'],
          screen_width=SCREEN_RES[0], key=config["exit_key"])

i = 1
data_exp = prepare_trials(config["experiment"], config["train_trials_randomize"])
for k, n, ans_type in data_exp:
    corr1, corr2, acc, rt1, rt2 = run_trial(win, k, n, ans_type, config, False, feedb)
    RESULTS.append([i, "exp", k, n, ans_type, corr1, corr2, acc, rt1, rt2])
    i += 1

show_info(win, join('.', 'messages', "end.txt"), text_size=config['TEXT_SIZE'],
          screen_width=SCREEN_RES[0], key=config["exit_key"])
