method_explanation={"BQA":"""You solve the following probabilistic question and generate the probability of the answer by only providing a number from 00 to 99 without any explanation:\n""",
"COT":"""
You solve the following probabilistic question and provide a detailed explanation of your solution and mathematical reasoning.
At the end of your answer, write a sentence that will give your final answer rounded to its closest integer, as such:
The answer to this probabilistic question rounded to the closest integer is 71%.
"""}

#2 0.3899999999999999
e1={"context":"If purple event is False, then grey event is True with probability of 39%. If purple event is False, then grey event is False with probability of 61%. If purple event is True, then grey event is True with probability of 3%. If purple event is True, then grey event is False with probability of 97%. purple event is true with probability of 55%. purple event is false with probability of 45%. ",
    "query":"What is the probability that grey event is True given that purple event is False?",
    "BQA":"39",
    "COT":"""This probablity is given to us in the context and as a result if final answer is 39%."""}

#121 0.3996569250317662
e2={"context":"pink event is true with probability of 87%. pink event is false with probability of 13%. If pink event is False, then black event is True with probability of 45%. If pink event is False, then black event is False with probability of 55%. If pink event is True, then black event is True with probability of 62%. If pink event is True, then black event is False with probability of 38%. If pink event is False, then red event is True with probability of 42%. If pink event is False, then red event is False with probability of 58%. If pink event is True, then red event is True with probability of 48%. If pink event is True, then red event is False with probability of 52%. ",
    "query":"What is the probability that black event is False given that red event is True?",
    "BQA":"40",
    "COT":"""
To find: P(Black=False|Red=True) According to Bayes' Theorem:
P(Black=False|Red=True) = P(Black=False and Red=True) / P(Red=True)
First, we find P(Black=False and Red=True)
P(Black=False and Red=True) = P(Black=False|Pink=True)*P(Red=True|Pink=True)*P(Pink=True) + P(Black=False|Pink=False)*P(Red=True|Pink=False)*P(Pink=False) = (0.38 * 0.48 * 0.87) + (0.55 * 0.42 * 0.13) = 0.188718
Next, we find P(Red=True)
P(Red=True) = P(Red=True|Pink=True)*P(Pink=True) + P(Red=True|Pink=False)*P(Pink=False)= (0.48 * 0.87) + (0.42 * 0.13) = 0.4722
Now, we can calculate P(Black=False|Red=True):
P(Black=False|Red=True) = 0.188718 / 0.4722 = 0.3996

So the final answer is approximately 40%.
"""}

#228 0.2319835959421541
e3={"context":"If black event is False, then pink event is True with probability of 22%. If black event is False, then pink event is False with probability of 78%. If black event is True, then pink event is True with probability of 10%. If black event is True, then pink event is False with probability of 90%. black event is true with probability of 61%. black event is false with probability of 39%. If pink event is False, then yellow event is True with probability of 19%. If pink event is False, then yellow event is False with probability of 81%. If pink event is True, then yellow event is True with probability of 72%. If pink event is True, then yellow event is False with probability of 28%. If pink event is False, then blue event is True with probability of 20%. If pink event is False, then blue event is False with probability of 80%. If pink event is True, then blue event is True with probability of 60%. If pink event is True, then blue event is False with probability of 40%. ",
    "query":"What is the probability that yellow event is True given that blue event is False?",
    "BQA": "23",
    "COT":"""
We need to calculate the probability of Yellow event being True given that Blue event is False.
P(Yellow=True | Blue=False) = P(Yellow=True and Blue=False) / P(Blue=False)

First, calculate P(Blue=False)
P(Blue=False) = P(Blue=False | Pink=True)*P(Pink=True) + P(Blue=False | Pink=False)*P(Pink=False)

We need the probablity of P(Pink=True) and P(Pink=False)
P(Pink=True) = P(Pink=True | Black=True) * P(Black=True)+ P(Pink=True | Black=False) * P(Black=False)  = (0.1 * 0.61) + (0.22 * 0.39) = 0.1468
P(Pink=False) = 1 - P(Pink=True) = 0.8532

Now can calcualte P(Blue=False):
P(Blue=False) = P(Blue=False | Pink=True)*P(Pink=True) + P(Blue=False | Pink=False)*P(Pink=False) = (0.4 * 0.1468) + (0.8 * 0.8532) = 0.74128
Next, calculate P(Yellow=True and Blue=False)
P(Yellow=True and Blue=False) = P(Yellow=True | Pink=True)*P(Blue=False | Pink=True)*P(Pink=True) + P(Yellow=True | Pink=False)*P(Blue=False | Pink=False)*P(Pink=False) = (0.72 * 0.4 * 0.1468) + (0.19 * 0.8 * 0.8532) = 0.1719648

# Finally, calculate P(Yellow=True | Blue=False)
P(Yellow=True | Blue=False) = 0.1719648 / 0.74128 = 0.2319
So the final answer is approximately 23%.
"""}
