import os, argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Test LLMs for Graph Generation')
parser.add_argument('--testdataset', dest='testdataset', default="../datasets/Colored_1000_examples.csv", help='input test dataset',type=str)
parser.add_argument('--outputdataset', dest='outputdataset', default="../datasets/", help='Dataset folder that has saved the results',type=str)
parser.add_argument('--models',dest='models',nargs='+',default=["gpt-3.5-turbo", "gpt-4-0613","meta/meta-llama-3-70b-instruct","mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"],choices=["gpt-3.5-turbo", "gpt-4-0613","meta/meta-llama-3-70b-instruct","mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"], help="Specify one or more models.")
args = parser.parse_args()

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

for model_name in args.models:

    model_name_folder=model_name
    if "/" in model_name:
        model_name_folder=model_name.split("/")[1]
    file_name = args.outputdataset+"graph_model_name "+model_name_folder+".csv"

    if not os.path.exists(file_name):
        continue
    asnwer_data = pd.read_csv(file_name)[:]
    ac1, t = [0 for _ in range(11)], [0 for _ in range(11)]
    edge_ac1, edge_t = [0 for _ in range(11)], [0 for _ in range(11)]
    onlyone_ac1 = [0 for _ in range(11)]
    for (num, i), (_, i_LLM) in zip(data.iterrows(), asnwer_data.iterrows()):
        depth = int(i["depth"])
        matches,answer=graphs_match(i_LLM["raw_text"],i["graph"])
        if answer:
            ac1[depth]+=1
        if matches==depth-2:
            onlyone_ac1[depth]+=1
        edge_ac1[depth]+=matches
        t[depth] += 1
        edge_t[depth]+=depth-1

    print(file_name)
    print("Graph Accuracy:")
    print([ac1[depth] / max(t[depth], 1) for depth in range(1, 11)])
    print("Edge Accuracy:")
    print([edge_ac1[depth] / max(edge_t[depth], 1) for depth in range(1, 11)])
    print("Graphs with one incorrect edge:")
    print([onlyone_ac1[depth] / max(t[depth], 1) for depth in range(1, 11)])
