import os, argparse, re
import pandas as pd
from openai import OpenAI

parser = argparse.ArgumentParser(description='Test LLMs for Number Extraction')
parser.add_argument('--testdataset', dest='testdataset', default="../datasets/Colored_1000_examples.csv", help='input test dataset',type=str)
parser.add_argument('--outputdataset', dest='outputdataset', default="../datasets/", help='Dataset folder that has saved the results',type=str)
parser.add_argument('--models', dest='models',default="all", choices=["gpt-3.5-turbo-0613", "gpt-4-0613","all"], help="Choose a model")
parser.add_argument('--reversed', dest='reversed', action='store_true', help='Whether to reverse the order of operations by including the graph first', default=False)
args = parser.parse_args()


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

for graph_use in [False,True]:
    for model_name in LLM_models:
        if not graph_use and args.reversed:
            continue
        if not args.reversed:
            file_name = args.outputdataset+"number_extraction_model_name "+model_name+" graph included "+str(graph_use)+".csv"
        else:
            file_name = args.outputdataset+"number_extraction_model_name "+model_name+" graph included "+str(graph_use)+"_reversed.csv"        
        if not os.path.exists(file_name):
            continue
        asnwer_data = pd.read_csv(file_name)[:]

        ac1, t = [0 for _ in range(11)], [0 for _ in range(11)]
        edge_ac1, edge_t = [0 for _ in range(11)], [0 for _ in range(11)]
        onlyone_ac1 = [0 for _ in range(11)]

        numbers_ac1, numbers_t = [0 for _ in range(11)], [0 for _ in range(11)]
        numbers_edge_ac1, numbers_edge_t = [0 for _ in range(11)], [0 for _ in range(11)]
        numbers_onlyone_ac1 = [0 for _ in range(11)]
        for (num, i), (_, i_LLM) in zip(data.iterrows(), asnwer_data.iterrows()):
            depth = int(i["depth"])
            if graph_use:
                if not args.reversed:
                    matches,answer=graphs_match(i_LLM["raw_text"].split("numbers:")[0].split("graph:")[1],i["graph"])
                else:
                    try:
                        matches,answer=graphs_match(i_LLM["raw_text"].split("graph:")[1].split("numbers:")[0],i["graph"])
                    except Exception as e:
                        matches,answer=0,0
                if answer:
                    ac1[depth]+=1
                if matches==depth-2:
                    onlyone_ac1[depth]+=1
                edge_ac1[depth]+=matches
                t[depth] += 1
                edge_t[depth]+=depth-1
            if graph_use:
                if not args.reversed:
                    matches,answer=correct_probablities(i["contexts"],i_LLM["raw_text"].split("numbers:")[1])
                else:
                    matches,answer=correct_probablities(i["contexts"],i_LLM["raw_text"].split("numbers:")[1].split("graph:")[0])
            else:
                matches,answer=correct_probablities(i["contexts"],i_LLM["raw_text"])
            if answer:
                numbers_ac1[depth]+=1
            if matches==depth*4-3:
                numbers_onlyone_ac1[depth]+=1
            numbers_edge_ac1[depth]+=matches
            numbers_t[depth] += 1
            numbers_edge_t[depth]+=depth*4-2

        print(file_name)
        print("Graph Generation (if included otherwise 0)")
        print("Graph Accuracy:")
        print([ac1[depth] / max(t[depth], 1) for depth in range(1, 11)])
        print("Edge Accuracy:")
        print([edge_ac1[depth] / max(edge_t[depth], 1) for depth in range(1, 11)])
        print("Graphs with one incorrect edge:")
        print([onlyone_ac1[depth] / max(t[depth], 1) for depth in range(1, 11)])

        print(file_name)
        print("Number Generation")
        print("Accuracy:")
        print([numbers_ac1[depth] / max(numbers_t[depth], 1) for depth in range(1, 11)])
        print("Individual Number Accuracy:")
        print([numbers_edge_ac1[depth] / max(numbers_edge_t[depth], 1) for depth in range(1, 11)])
        print("Instances with one incorrect number:")
        print([numbers_onlyone_ac1[depth] / max(numbers_t[depth], 1) for depth in range(1, 11)])

