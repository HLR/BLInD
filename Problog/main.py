import os, time, argparse,re
import pandas as pd
from openai import OpenAI
from prompts import e1,e2,e3,method_explanation
from utils import run_LLM

parser = argparse.ArgumentParser(description='Run LLMs for bayesian infernece')
parser.add_argument('--testdataset', dest='testdataset', default="../datasets/Colored_1000_examples.csv", help='input test dataset',type=str)
parser.add_argument('--outputdataset', dest='outputdataset', default="../datasets/", help='dataset folder to save the results',type=str)
parser.add_argument('--openaikey', dest='openaikey', default="", help='openai key',type=str)
parser.add_argument('--openaiorg', dest='openaiorg', default="", help='openai org',type=str)
parser.add_argument('--replicatekey', dest='replicatekey', default="", help='replicate key',type=str)
parser.add_argument('--samplenum', dest='samplenum', default=2000, help='how many instances of the dataset to read',type=int)
parser.add_argument('--models',dest='models',nargs='+',default=["gpt-3.5-turbo", "gpt-4-0613","meta/meta-llama-3-70b-instruct","mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"],choices=["gpt-3.5-turbo", "gpt-4-0613","meta/meta-llama-3-70b-instruct","mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"], help="Specify one or more models.")
parser.add_argument('--maxattempt', dest='maxattempt', default=10, help='max number of attempts after a failed prompt to openai',type=int)
parser.add_argument('--CLADDER', dest='CLADDER', action='store_true', help='use CLADDER dataset', default=False)

args = parser.parse_args()

os.environ["REPLICATE_API_TOKEN"] = args.replicatekey
client = OpenAI(api_key=args.openaikey,organization=args.openaiorg)

if args.CLADDER:
    args.testdataset="../datasets/CLADDER_test.csv"

data = pd.read_csv(args.testdataset)[:args.samplenum]

def replace_numbers(text,numbers):
    matches = re.findall(r"(\w+) = ([\d.]+)", numbers)
    probability_gpt = {key: float(value) for key, value in matches}
    for var_name,num in probability_gpt.items():
        text=text.replace(var_name,str(num))
    return text

for attempts in range(args.maxattempt):
    try:
        for number_use in [False,True]:
            for graph_use in [False,True]:
                if not number_use and graph_use:
                    continue
                explanation="With the following instructions asnwer the questions in the requested format with specific sections."
                if number_use:
                    explanation+= "Extract probabilities in the context in the format of given examples."
                if graph_use:
                    explanation+= "Extract the graph edges of the described Bayesian network in the context in the format of given examples."
                explanation+=method_explanation

                for model_name in args.models:
                    model_name_folder=model_name
                    if "/" in model_name:
                        model_name_folder=model_name.split("/")[1]
                    if args.CLADDER:
                        file_name = args.outputdataset+"problog_model_name "+model_name_folder+" graph included "+str(graph_use)+" number use "+str(number_use)+"_CLADDER.csv"
                    else:
                        file_name = args.outputdataset+"problog_model_name "+model_name_folder+" graph included "+str(graph_use)+" number use "+str(number_use)+".csv"

                    if os.path.exists(file_name):
                        existing_df = pd.read_csv(file_name)
                    else:
                        existing_df = []

                    for num, i in data.iterrows():
                        if num > args.samplenum:
                            break
                        if num < len(existing_df):
                            continue
                        print(model_name,num)
                        response_text = run_LLM(model_name,client,explanation,e1,e2,e3,i,graph_use,number_use,args)
                        df = pd.DataFrame([{"raw_text": response_text}])
                        if os.path.exists(file_name):
                            df.to_csv(file_name, mode='a', header=False, index=False)
                        else:
                            df.to_csv(file_name, index=False)
                        if model_name == "gpt-4-0613":
                            time.sleep(4)
                        else:
                            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(100)

