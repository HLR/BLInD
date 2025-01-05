import os, time, argparse
import pandas as pd
from openai import OpenAI
from prompts import e1,e2,e3

parser = argparse.ArgumentParser(description='Run LLMs for Number Extraction')
parser.add_argument('--testdataset', dest='testdataset', default="../datasets/Colored_1000_examples.csv", help='input test dataset',type=str)
parser.add_argument('--outputdataset', dest='outputdataset', default="../datasets/", help='dataset folder to save the results',type=str)
parser.add_argument('--openaikey', dest='openaikey', default="", help='openai key',type=str)
parser.add_argument('--openaiorg', dest='openaiorg', default="", help='openai org',type=str)
parser.add_argument('--samplenum', dest='samplenum', default=2000, help='how many instances of the dataset to read',type=int)
parser.add_argument('--models', dest='models',default="all", choices=["gpt-3.5-turbo", "gpt-4-0613","all"], help="Choose a model")
parser.add_argument('--maxattempt', dest='maxattempt', default=10, help='max number of attempts after a failed prompt to openai',type=int)
parser.add_argument('--reversed', dest='reversed', action='store_true', help='Whether to reverse the order of operations by including the graph first', default=False)
args = parser.parse_args()

client = OpenAI(api_key=args.openaikey,organization=args.openaiorg)

if args.models=="all":
    LLM_models=["gpt-3.5-turbo", "gpt-4-0613"]
else:
    LLM_models = [args.models]

data = pd.read_csv(args.testdataset)[:args.samplenum]

for attempts in range(args.maxattempt):
    try:
        for graph_use in [False,True]:
            if not graph_use and args.reversed:
                continue
            if not graph_use:
                explanation = "Extract probabilities in the context in the format of given examples."
            else:
                if not args.reversed:
                    explanation = "Extract the graph edges of the described Bayesian network in the context in the format of given examples. After that extract probabilities in the context in the format of given examples. Your asnwer should have two sections simply named graph and numbers."
                else:
                    explanation = "Extract probabilities in the context in the format of given examples. After that extract the graph edges of the described Bayesian network in the context in the format of given examples. Your asnwer should have two sections simply named graph and numbers."

            for model_name in LLM_models:
                if not args.reversed:
                    file_name = args.outputdataset+"number_extraction_model_name "+model_name+" graph included "+str(graph_use)+".csv"
                else:
                    file_name = args.outputdataset+"number_extraction_model_name "+model_name+" graph included "+str(graph_use)+"_reversed.csv"
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
                    if not graph_use:
                        openai_messages=[{"role": "system", "content": explanation},
                                            {"role": "user", "content": e1["context"]},
                                            {"role": "assistant", "content": e1["numbers"]},
                                            {"role": "user", "content": e2["context"]},
                                            {"role": "assistant", "content": e2["numbers"]},
                                            {"role": "user", "content": e3["context"]},
                                            {"role": "assistant", "content": e3["numbers"]},
                                            {"role": "user", "content": i["contexts"]},]
                    else:
                        if not args.reversed:
                            openai_messages=[{"role": "system", "content": explanation},
                                                {"role": "user", "content": e1["context"]},
                                                {"role": "assistant", "content": "graph:\n"+e1["graph"]+"\nnumbers:\n"+e1["numbers"]},
                                                {"role": "user", "content": e2["context"]},
                                                {"role": "assistant", "content": "graph:\n"+e2["graph"]+"\nnumbers:\n"+e2["numbers"]},
                                                {"role": "user", "content": e3["context"]},
                                                {"role": "assistant", "content": "graph:\n"+e3["graph"]+"\nnumbers:\n"+e3["numbers"]},
                                                {"role": "user", "content": i["contexts"]},]
                        else:
                            openai_messages=[{"role": "system", "content": explanation},
                                                {"role": "user", "content": e1["context"]},
                                                {"role": "assistant", "content": "numbers:\n"+e1["numbers"]+"\ngraph:\n"+e1["graph"]},
                                                {"role": "user", "content": e2["context"]},
                                                {"role": "assistant", "content": "numbers:\n"+e2["numbers"]+"\ngraph:\n"+e2["graph"]},
                                                {"role": "user", "content": e3["context"]},
                                                {"role": "assistant", "content": "numbers:\n"+e3["numbers"]+"\ngraph:\n"+e3["graph"]},
                                                {"role": "user", "content": i["contexts"]},]
                            
                    response = client.chat.completions.create(model=model_name, messages=openai_messages, max_tokens=1000, temperature=0.2)
                    response_text=response.choices[0].message.content
                    df = pd.DataFrame([{"raw_text": response_text}])
                    if os.path.exists(file_name):
                        df.to_csv(file_name, mode='a', header=False, index=False)
                    else:
                        df.to_csv(file_name, index=False)
                    if model_name == "gpt-4-0613":
                        time.sleep(16)
                    else:
                        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(100)

