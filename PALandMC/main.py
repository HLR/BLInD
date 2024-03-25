import os, time, argparse,re
import pandas as pd
from openai import OpenAI
from prompts import e1,e2,e3,method_explanation

parser = argparse.ArgumentParser(description='Run LLMs for bayesian infernece')
parser.add_argument('--testdataset', dest='testdataset', default="../datasets/Colored_1000_examples.csv", help='input test dataset',type=str)
parser.add_argument('--outputdataset', dest='outputdataset', default="../datasets/", help='dataset folder to save the results',type=str)
parser.add_argument('--openaikey', dest='openaikey', default="", help='openai key',type=str)
parser.add_argument('--openaiorg', dest='openaiorg', default="", help='openai org',type=str)
parser.add_argument('--method', dest='method', default="PAL",choices=["PAL", "MC"], help='method to solve the problem')
parser.add_argument('--samplenum', dest='samplenum', default=2000, help='how many instances of the dataset to read',type=int)
parser.add_argument('--models', dest='models',default="all", choices=["gpt-3.5-turbo-0613", "gpt-4-0613","all"], help="Choose a model")
parser.add_argument('--maxattempt', dest='maxattempt', default=10, help='max number of attempts after a failed prompt to openai',type=int)
parser.add_argument('--CLADDER', dest='CLADDER', action='store_true', help='use CLADDER dataset', default=False)
args = parser.parse_args()

client = OpenAI(api_key=args.openaikey,organization=args.openaiorg)

if args.CLADDER:
    args.testdataset="../datasets/CLADDER_test.csv"

if args.models=="all":
    LLM_models=["gpt-3.5-turbo-0613", "gpt-4-0613"]
else:
    LLM_models = [args.models]
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
                explanation="With the following instructions asnwer the questions in the requested format with specific sections."
                if number_use:
                    explanation+= "Extract probabilities in the context in the format of given examples."
                if graph_use:
                    explanation+= "Extract the graph edges of the described Bayesian network in the context in the format of given examples."
                explanation+=method_explanation[args.method]

                for model_name in LLM_models:
                    if args.CLADDER:
                        file_name = args.outputdataset+str(args.method)+"_model_name "+model_name+" graph included "+str(graph_use)+" number use "+str(number_use)+"_CLADDER.csv"
                    else:
                        file_name = args.outputdataset+str(args.method)+"_model_name "+model_name+" graph included "+str(graph_use)+" number use "+str(number_use)+".csv"

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
                            if not number_use:
                                e1_msg="solution:\n"+replace_numbers(e1[args.method],e1["numbers"])
                                e2_msg="solution:\n"+replace_numbers(e2[args.method],e2["numbers"])
                                e3_msg="solution:\n"+replace_numbers(e3[args.method],e3["numbers"])
                            else:
                                e1_msg="numbers:\n"+e1["numbers"]+"\nsolution:\n"+e1[args.method]
                                e2_msg="numbers:\n"+e2["numbers"]+"\nsolution:\n"+e2[args.method]
                                e3_msg="numbers:\n"+e3["numbers"]+"\nsolution:\n"+e3[args.method]
                        else:
                            if number_use:
                                e1_msg="numbers:\n"+e1["numbers"]+"\ngraph:\n"+e1["graph"]+"\nsolution:\n"+e1[args.method]
                                e2_msg="numbers:\n"+e2["numbers"]+"\ngraph:\n"+e2["graph"]+"\nsolution:\n"+e2[args.method]
                                e3_msg="numbers:\n"+e3["numbers"]+"\ngraph:\n"+e3["graph"]+"\nsolution:\n"+e3[args.method]
                            else:
                                e1_msg="graph:\n"+e1["graph"]+"solution:\n"+replace_numbers(e1[args.method],e1["numbers"])
                                e2_msg="graph:\n"+e2["graph"]+"solution:\n"+replace_numbers(e2[args.method],e2["numbers"])
                                e3_msg="graph:\n"+e3["graph"]+"solution:\n"+replace_numbers(e3[args.method],e3["numbers"])

                        openai_messages=[{"role": "assistant", "content": explanation},
                                            {"role": "user", "content": e1["context"]+"\nquestion:\n"+e1["query"]},
                                            {"role": "system", "content": e1_msg},
                                            {"role": "user", "content": e2["context"]+"\nquestion:\n"+e2["query"]},
                                            {"role": "system", "content": e2_msg},
                                            {"role": "user", "content": e3["context"]+"\nquestion:\n"+e3["query"]},
                                            {"role": "system", "content": e3_msg},
                                            {"role": "user", "content": i["contexts"]+"\nquestion:\n"+i["query"]},]
 
                        response = client.chat.completions.create(model=model_name, messages=openai_messages, max_tokens=1500, temperature=0.2)
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

