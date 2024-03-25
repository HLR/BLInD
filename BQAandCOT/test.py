import os, argparse, re
import pandas as pd
parser = argparse.ArgumentParser(description='Test LLMs for bayesian infernece')
parser.add_argument('--testdataset', dest='testdataset', default="../datasets/Colored_1000_examples.csv", help='input test dataset',type=str)
parser.add_argument('--outputdataset', dest='outputdataset', default="../datasets/", help='dataset folder to save the results',type=str)
parser.add_argument('--models', dest='models',default="all", choices=["gpt-3.5-turbo-0613", "gpt-4-0613","all"], help="Choose a model")
parser.add_argument('--clutter', dest='clutter', default=True, help='use clutter dataset',type=bool)


args = parser.parse_args()

if args.models=="all":
    LLM_models=["gpt-3.5-turbo", "gpt-4"]
else:
    LLM_models = [args.models]

if args.clutter:
    args.testdataset="../datasets/clutter_test.csv"

data = pd.read_csv(args.testdataset)

def asnwer_extractor(response):

    pattern = r'-?\d+(?:\.\d+)?'
    numbers = re.findall(pattern, response)
    return float(numbers[-1])

for model_name in LLM_models:
    for args_method in ["Direct","COT"]:
        for few_shot in [False,True]:
        
            if args.clutter:
                file_name = args.outputdataset+str(args_method)+"_model_name "+model_name+"_few_shot_"+str(few_shot)+"_clutter.csv"
            else:
                file_name = args.outputdataset+str(args_method)+"_model_name "+model_name+"_few_shot_"+str(few_shot)+".csv"
            if not os.path.exists(file_name):
                continue
            print(model_name)
            asnwer_data = pd.read_csv(file_name)[:]
            solution_ac1, solution_t = [0 for _ in range(11)], [0 for _ in range(11)]
            for (num, i), (_, i_LLM) in zip(data.iterrows(), asnwer_data.iterrows()):
                depth = int(i["depth"])
                try:
                    predicted_answer=asnwer_extractor(i_LLM["raw_text"])
                except:
                    predicted_answer = 0.5
                while predicted_answer>1:
                    predicted_answer/=10
                true_answer=float(i["answers"])
                if (abs(predicted_answer - true_answer) <= 0.01):
                    solution_ac1[depth] += 1
                solution_t[depth] += 1
            print(file_name)
            if args.clutter:
                print("Solution:")
                print([solution_ac1[depth] / max(solution_t[depth], 1) for depth in range(10, 11)][0])
            else:
                print("Solution:")
                print([solution_ac1[depth] / max(solution_t[depth], 1) for depth in range(1, 11)])

