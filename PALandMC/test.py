import os, argparse, re
import pandas as pd
from utils import extract_sections
parser = argparse.ArgumentParser(description='Test LLMs for bayesian infernece')
parser.add_argument('--testdataset', dest='testdataset', default="../datasets/Colored_1000_examples.csv", help='input test dataset',type=str)
parser.add_argument('--outputdataset', dest='outputdataset', default="../datasets/", help='Dataset folder that has saved the results',type=str)
parser.add_argument('--models', dest='models',default="all", choices=["gpt-3.5-turbo-0613", "gpt-4-0613","all"], help="Choose a model")
parser.add_argument('--method', dest='method', default="PAL",choices=["PAL", "MC"], help='method to solve the problem')
parser.add_argument('--CLADDER', dest='CLADDER', action='store_true', help='use CLADDER dataset', default=False)

args = parser.parse_args()

if args.CLADDER:
    args.testdataset="../datasets/CLADDER_test.csv"

if args.models=="all":
    LLM_models=["gpt-3.5-turbo-0613", "gpt-4-0613"]
else:
    LLM_models = [args.models]
data = pd.read_csv(args.testdataset)

def parse_graph1(graph_string):

    try:
        trimmed_string = graph_string.strip(" \n").replace("\n",",")
        edges=trimmed_string.split(",")
        graph= {edge.split("->")[1].strip("' \n").strip('"'): edge.split("->")[0].strip("' \n").strip('"') for edge in edges}
        return {i:j for i,j in graph.items() if 'event' in i and 'event' in j}
    except:
        return {}

def parse_graph2(graph_string):
    edges = graph_string.split(" | ")
    graph= {edge.split(" -> ")[1].strip("' ").strip('"'): edge.split(" -> ")[0].strip("(,)").strip("' ").strip('"') for edge in edges}
    return {i:j for i,j in graph.items() if 'event' in i and 'event' in j}

def graphs_match(graph1, graph2):
    return len(set(parse_graph1(graph1).items()) & set(parse_graph2(graph2).items())),parse_graph1(graph1) == parse_graph2(graph2)

def correct_probablities(text,g_text):

    probabilities = {}
    pattern = r"([\d\w]+ event) is (true|false) with probability of (\d+)%"

    matches = re.findall(pattern, " ".join([sentence for sentence in text.split(".") if not 'then ' in sentence]), re.IGNORECASE)

    for match in matches:
        key = f"prob_{match[0].split(' ')[0]}_{match[1].lower()}"
        probabilities[key]=float(match[2])/100

    for match in matches:
        key = f"prob_{match[0].split(' ')[0]}_{match[1].lower()}"
        probabilities[key]=float(match[2])/100

    pattern_conditional = r"If ([\d\w]+ event) is (True|False), then ([\d\w]+ event) is (True|False) with probability of (\d+)%"

    matches = re.findall(pattern_conditional, text)

    for match in matches:
        key = f"prob_{match[2].lower().split(' ')[0]}_{match[3].lower()}_given_{match[0].lower().split(' ')[0]}_{match[1].lower()}"
        probabilities[key]=float(match[4])/100
    
    ##############################################################
    matches = re.findall(r"(\w+) = ([\d.]+)", g_text)
    probability_gpt = {key: float(value) for key, value in matches}

    return len(set(probabilities.items()) & set(probability_gpt.items())),probabilities==probability_gpt

def extract_import_random_section(text):
    import_index = text.find('import random')
    if import_index != -1:
        return text[import_index:]
    else:
        return ""

for model_name in LLM_models:
    for number_use in [False,True]:
        for graph_use in [False,True]:
        
            if args.CLADDER:
                file_name = args.outputdataset+str(args.method)+"_model_name "+model_name+" graph included "+str(graph_use)+" number use "+str(number_use)+"_CLADDER.csv"
            else:
                file_name = args.outputdataset+str(args.method)+"_model_name "+model_name+" graph included "+str(graph_use)+" number use "+str(number_use)+".csv"
            if not os.path.exists(file_name):
                continue

            asnwer_data = pd.read_csv(file_name)[:]

            ac1, t = [0 for _ in range(11)], [0 for _ in range(11)]
            edge_ac1, edge_t = [0 for _ in range(11)], [0 for _ in range(11)]
            onlyone_ac1 = [0 for _ in range(11)]

            numbers_ac1, numbers_t = [0 for _ in range(11)], [0 for _ in range(11)]
            numbers_edge_ac1, numbers_edge_t = [0 for _ in range(11)], [0 for _ in range(11)]
            numbers_onlyone_ac1 = [0 for _ in range(11)]

            solution_ac1, solution_t = [0 for _ in range(11)], [0 for _ in range(11)]
            code_ac1, code_t = [0 for _ in range(11)], [0 for _ in range(11)]

            for (num, i), (_, i_LLM) in zip(data.iterrows(), asnwer_data.iterrows()):
                depth = int(i["depth"])
                number_section,graph_section,solution_section=extract_sections(i_LLM["raw_text"].lower())

                if solution_section=="":
                    solution_section=extract_import_random_section(i_LLM["raw_text"].lower())
                    if solution_section=="":
                        solution_section=i_LLM["raw_text"].lower()
                if not args.CLADDER:
                    matches,answer=correct_probablities(i["contexts"],number_section)
                    if answer:
                        numbers_ac1[depth]+=1
                    if matches==depth*4-3:
                        numbers_onlyone_ac1[depth]+=1
                    numbers_edge_ac1[depth]+=matches
                    numbers_t[depth] += 1
                    numbers_edge_t[depth]+=depth*4-2

                    matches,answer=graphs_match(graph_section,i["graph"])
                    if answer:
                        ac1[depth]+=1
                    if matches==depth-2:
                        onlyone_ac1[depth]+=1
                    edge_ac1[depth]+=matches
                    t[depth] += 1
                    edge_t[depth]+=depth-1


                try:
                    exec(number_section+"\n\n"+solution_section)
                    predicted_answer = float(locals()['answer'])
                    code_ac1[depth]+=1
                except:
                    predicted_answer = 0.5
                code_t[depth]+=1
                while predicted_answer>1:
                    predicted_answer/=10

                true_answer=float(i["answers"])
                if (abs(predicted_answer - true_answer) <= 0.01):
                    solution_ac1[depth] += 1
                solution_t[depth] += 1

            print(file_name)
            if not args.CLADDER:
                print("Numbers:")
                print([numbers_ac1[depth] / max(numbers_t[depth], 1) for depth in range(1, 11)])
                print([numbers_edge_ac1[depth] / max(numbers_edge_t[depth], 1) for depth in range(1, 11)])
                print([numbers_onlyone_ac1[depth] / max(numbers_t[depth], 1) for depth in range(1, 11)])

                print("Graph:")
                print([ac1[depth] / max(t[depth], 1) for depth in range(1, 11)])
                print([edge_ac1[depth] / max(edge_t[depth], 1) for depth in range(1, 11)])
                print([onlyone_ac1[depth] / max(t[depth], 1) for depth in range(1, 11)])

                print("Code Accuracy:")
                print([code_ac1[depth] / max(code_t[depth], 1) for depth in range(1, 11)])

                print("Solution:")
                print([solution_ac1[depth] / max(solution_t[depth], 1) for depth in range(1, 11)])
            else:
                print("Solution:")
                print([solution_ac1[depth] / max(solution_t[depth], 1) for depth in range(10, 11)][0])
