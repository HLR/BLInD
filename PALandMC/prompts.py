method_explanation={
"PAL":"""Solve the probabilistic questions by only writing a Python code.
"In Calculations section, the solution process is done, including the code and the mathematical reasoning in the form of python code comments that start with #. "In Answer section, the final answer is assigned to a variable named answer.""",
"MC":"""Solve the probabilistic questions writing a Python code that would solve the question with a monte carlo method. The final probability is assigned to a variable named answer. Follow the format no matter what.""",
}


#2 0.3899999999999999
e1={"context":"If purple event is False, then grey event is True with probability of 39%. If purple event is False, then grey event is False with probability of 61%. If purple event is True, then grey event is True with probability of 3%. If purple event is True, then grey event is False with probability of 97%. purple event is true with probability of 55%. purple event is false with probability of 45%. ",
    "query":"What is the probability that grey event is True given that purple event is False?",
    "graph": "purple event -> grey event",
    "numbers":"""prob_grey_true_given_purple_false = 0.39
prob_grey_false_given_purple_false = 0.61
prob_grey_true_given_purple_true = 0.03
prob_grey_false_given_purple_true = 0.97
prob_purple_true = 0.55
prob_purple_false = 0.45""",

"PAL":"""
# To find: P(Grey=True|Purple=False)
# This is given to us in the context

# Answer
answer=prob_grey_true_given_purple_false
""",
"MC":"""
import random
def simulate():
    purple = random.random() < prob_purple_true
    if purple:
        grey = random.random() < prob_grey_true_given_purple_true
    else:
        grey = random.random() < prob_grey_true_given_purple_false
    return purple, grey

grey_true_given_purple_false_count = 0
purple_false_count = 0
for _ in range(1000000):
    purple, grey = simulate()
    if not purple:
        purple_false_count += 1
        if grey:
            grey_true_given_purple_false_count += 1

answer = grey_true_given_purple_false_count / purple_false_count if purple_false_count > 0 else 0
""",}

#121 0.3996569250317662
e2={"context":"pink event is true with probability of 87%. pink event is false with probability of 13%. If pink event is False, then black event is True with probability of 45%. If pink event is False, then black event is False with probability of 55%. If pink event is True, then black event is True with probability of 62%. If pink event is True, then black event is False with probability of 38%. If pink event is False, then red event is True with probability of 42%. If pink event is False, then red event is False with probability of 58%. If pink event is True, then red event is True with probability of 48%. If pink event is True, then red event is False with probability of 52%. ",
    "query":"What is the probability that black event is False given that red event is True?",
    "graph": "pink event -> black event, pink event -> red event",
    "numbers":"""prob_pink_true = 0.87
prob_pink_false = 0.13
prob_black_true_given_pink_false = 0.45
prob_black_false_given_pink_false = 0.55
prob_black_true_given_pink_true = 0.62
prob_black_false_given_pink_true = 0.38
prob_red_true_given_pink_false = 0.42
prob_red_false_given_pink_false = 0.58
prob_red_true_given_pink_true = 0.48
prob_red_false_given_pink_true = 0.52""",
"PAL":"""
# To find: P(Black=False|Red=True)
# According to Bayes' Theorem:
# P(Black=False|Red=True) = P(Black=False and Red=True) / P(Red=True)

# First, we find P(Black=False and Red=True)
# P(Black=False and Red=True) = P(Black=False|Pink=True)*P(Red=True|Pink=True)*P(Pink=True) + P(Black=False|Pink=False)*P(Red=True|Pink=False)*P(Pink=False)

prob_black_false_and_red_true = (prob_black_false_given_pink_true * prob_red_true_given_pink_true * prob_pink_true) + (prob_black_false_given_pink_false * prob_red_true_given_pink_false * prob_pink_false)

# Next, we find P(Red=True)
# P(Red=True) = P(Red=True|Pink=True)*P(Pink=True) + P(Red=True|Pink=False)*P(Pink=False)

prob_red_true = (prob_red_true_given_pink_true * prob_pink_true) + (prob_red_true_given_pink_false * prob_pink_false)

# Now, we can calculate P(Black=False|Red=True):
prob_black_false_given_red_true = prob_black_false_and_red_true / prob_red_true

# Answer
answer=prob_black_false_given_red_true
""",
"MC":"""
import random

def simulate():
    pink = random.random() < prob_pink_true
    if pink:
        black = random.random() < prob_black_true_given_pink_true
        red = random.random() < prob_red_true_given_pink_true
    else:
        black = random.random() < prob_black_true_given_pink_false
        red = random.random() < prob_red_true_given_pink_false
    return pink, black, red

black_false_given_red_true_count = 0
red_true_count = 0
for _ in range(1000000):
    pink, black, red = simulate()
    if red:
        red_true_count += 1
        if not black:
            black_false_given_red_true_count += 1

answer = black_false_given_red_true_count / red_true_count if red_true_count > 0 else 0
""",}


#228 0.2319835959421541
e3={"context":"If black event is False, then pink event is True with probability of 22%. If black event is False, then pink event is False with probability of 78%. If black event is True, then pink event is True with probability of 10%. If black event is True, then pink event is False with probability of 90%. black event is true with probability of 61%. black event is false with probability of 39%. If pink event is False, then yellow event is True with probability of 19%. If pink event is False, then yellow event is False with probability of 81%. If pink event is True, then yellow event is True with probability of 72%. If pink event is True, then yellow event is False with probability of 28%. If pink event is False, then blue event is True with probability of 20%. If pink event is False, then blue event is False with probability of 80%. If pink event is True, then blue event is True with probability of 60%. If pink event is True, then blue event is False with probability of 40%. ",
    "query":"What is the probability that yellow event is True given that blue event is False?",
    "graph": "black event -> pink event, pink event -> yellow event, pink event -> blue event",
    "numbers":"""prob_pink_true_given_black_false = 0.22
prob_pink_false_given_black_false = 0.78
prob_pink_true_given_black_true = 0.10
prob_pink_false_given_black_true = 0.90
prob_black_true = 0.61
prob_black_false = 0.39
prob_yellow_true_given_pink_false = 0.19
prob_yellow_false_given_pink_false = 0.81
prob_yellow_true_given_pink_true = 0.72
prob_yellow_false_given_pink_true = 0.28
prob_blue_true_given_pink_false = 0.20
prob_blue_false_given_pink_false = 0.80
prob_blue_true_given_pink_true = 0.60
prob_blue_false_given_pink_true = 0.40""",

"PAL":"""
# We need to calculate the probability of Yellow event being True given that Blue event is False.
# P(Yellow=True | Blue=False) = P(Yellow=True and Blue=False) / P(Blue=False)

# First, calculate P(Blue=False)
# P(Blue=False) = P(Blue=False | Pink=True)*P(Pink=True) + P(Blue=False | Pink=False)*P(Pink=False)

prob_pink_True = (prob_pink_true_given_black_true * prob_black_true) + (prob_pink_true_given_black_false * prob_black_false)
prob_pink_false = 1 - prob_pink_true

prob_blue_false = (prob_blue_false_given_pink_true * prob_pink_true) + (prob_blue_false_given_pink_false * prob_pink_false)

# Next, calculate P(Yellow=True and Blue=False)
# P(Yellow=True and Blue=False) = P(Yellow=True | Pink=True)*P(Blue=False | Pink=True)*P(Pink=True) +
#                                  P(Yellow=True | Pink=False)*P(Blue=False | Pink=False)*P(Pink=False)
prob_yellow_true_and_blue_false = (prob_yellow_true_given_pink_true * prob_blue_false_given_pink_true * prob_pink_true) + (prob_yellow_true_given_pink_false * prob_blue_false_given_pink_false * prob_pink_false)

# Finally, calculate P(Yellow=True | Blue=False)
prob_yellow_true_given_blue_false = prob_yellow_true_and_blue_false / prob_blue_false

# Answer
answer= prob_yellow_true_given_blue_false
""",
"MC":"""
import random
def simulate():
    black = random.random() < prob_black_true
    if black:
        pink = random.random() < prob_pink_true_given_black_true
    else:
        pink = random.random() < prob_pink_true_given_black_false
    if pink:
        yellow = random.random() < prob_yellow_true_given_pink_true
        blue = random.random() < prob_blue_true_given_pink_true
    else:
        yellow = random.random() < prob_yellow_true_given_pink_false
        blue = random.random() < prob_blue_true_given_pink_false
    return pink, yellow, blue

yellow_true_given_blue_false_count = 0
blue_false_count = 0
for _ in range(1000000):
    pink, yellow, blue = simulate()
    if not blue:
        blue_false_count += 1
        if yellow:
            yellow_true_given_blue_false_count += 1

answer = yellow_true_given_blue_false_count / blue_false_count if blue_false_count > 0 else 0
""",}

