#2 
e1={"context":"If purple event is False, then grey event is True with probability of 39%. If purple event is False, then grey event is False with probability of 61%. If purple event is True, then grey event is True with probability of 3%. If purple event is True, then grey event is False with probability of 97%. purple event is true with probability of 55%. purple event is false with probability of 45%. ",
    "graph": "purple event -> grey event",
    "numbers":"""prob_grey_true_given_purple_false = 0.39
prob_grey_false_given_purple_false = 0.61
prob_grey_true_given_purple_true = 0.03
prob_grey_false_given_purple_true = 0.97
prob_purple_true = 0.55
prob_purple_false = 0.45"""}

#121
e2={"context":"pink event is true with probability of 87%. pink event is false with probability of 13%. If pink event is False, then black event is True with probability of 45%. If pink event is False, then black event is False with probability of 55%. If pink event is True, then black event is True with probability of 62%. If pink event is True, then black event is False with probability of 38%. If pink event is False, then red event is True with probability of 42%. If pink event is False, then red event is False with probability of 58%. If pink event is True, then red event is True with probability of 48%. If pink event is True, then red event is False with probability of 52%. ",
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
prob_red_false_given_pink_true = 0.52"""}

#228
e3={"context":"If black event is False, then pink event is True with probability of 22%. If black event is False, then pink event is False with probability of 78%. If black event is True, then pink event is True with probability of 10%. If black event is True, then pink event is False with probability of 90%. black event is true with probability of 61%. black event is false with probability of 39%. If pink event is False, then yellow event is True with probability of 19%. If pink event is False, then yellow event is False with probability of 81%. If pink event is True, then yellow event is True with probability of 72%. If pink event is True, then yellow event is False with probability of 28%. If pink event is False, then blue event is True with probability of 20%. If pink event is False, then blue event is False with probability of 80%. If pink event is True, then blue event is True with probability of 60%. If pink event is True, then blue event is False with probability of 40%. ",
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
prob_blue_false_given_pink_true = 0.40"""}
