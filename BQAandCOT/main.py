import os, time, argparse
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
parser.add_argument('--method', dest='method', default="BQA",choices=["BQA", "COT"], help='method to solve the problem')
parser.add_argument('--samplenum', dest='samplenum', default=2, help='how many instances of the dataset to read',type=int)
parser.add_argument('--models',dest='models',nargs='+',default=["gpt-3.5-turbo", "gpt-4-0613","meta/meta-llama-3-70b-instruct","mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"],choices=["gpt-3.5-turbo", "gpt-4-0613","meta/meta-llama-3-70b-instruct","mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"], help="Specify one or more models.")
parser.add_argument('--maxattempt', dest='maxattempt', default=10, help='max number of attempts after a failed prompt to openai',type=int)
parser.add_argument('--CLADDER', dest='CLADDER', action='store_true', help='use CLADDER dataset', default=False)
args = parser.parse_args()

os.environ["REPLICATE_API_TOKEN"] = args.replicatekey
client = OpenAI(api_key=args.openaikey,organization=args.openaiorg)

if args.CLADDER:
    args.testdataset="../datasets/CLADDER_test.csv"

data = pd.read_csv(args.testdataset)[:args.samplenum]

for attempts in range(args.maxattempt):
    try:
        for few_shot in [False,True]:
            explanation=method_explanation[args.method]

            for model_name in args.models:
                model_name_folder=model_name
                if "/" in model_name:
                    model_name_folder=model_name.split("/")[1]
                if args.CLADDER:
                    file_name = args.outputdataset+str(args.method)+"_model_name "+model_name_folder+"_few_shot_"+str(few_shot)+"_CLADDER.csv"
                else:
                    file_name = args.outputdataset+str(args.method)+"_model_name "+model_name_folder+"_few_shot_"+str(few_shot)+".csv"

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
                    response_text = run_LLM(model_name,client,explanation,e1,e2,e3,i,few_shot,args)

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

