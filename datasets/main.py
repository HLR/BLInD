import random, time, os, argparse
import pandas as pd
from utils import load_from_pickle, save_to_pickle, generate_queries, graph_generator, filter_queries_by_graph,create_bayesian_tables, solve_bayesian_inference,create_text


parser = argparse.ArgumentParser(description='Create BLInD')
parser.add_argument('--seed', dest='seed', default=2023, help='random seed',type=int)
parser.add_argument('--Arborescence', dest='Arborescence', action='store_false', help='Add just Arborescence graphs', default=True)
parser.add_argument('--max_variable_number', dest='max_variable_number', default=10, help='Max number of variables to use in BNs',type=int)
parser.add_argument('--additionalsamples', dest='additionalsamples', default=0, help='chooses additional graphs and queries which increases the randomnes by takes more time',type=int)
parser.add_argument('--answer_threshold', dest='answer_threshold', default=0.03, help='remove very small answers',type=float)
parser.add_argument('--Visize', dest='Visize', default=100, help='Number of samples that are selected for each Vi split',type=int)
parser.add_argument('--outputdataset', dest='outputdataset', default="New_BLInD.csv", help='name of the dataset file to save',type=str)
parser.add_argument('--clear_cache', dest='clear_cache', action='store_true', help='Add just Arborescence graphs', default=False)
args = parser.parse_args()

random.seed(args.seed)

t0=time.time()
all_examples=[]

for i in range(2, args.max_variable_number + 1):
    graph_list_file = f"cache_graph_data/graph_list_{i}.pkl"
    all_possible_queries_file = f"cache_graph_data/all_possible_queries_{i}.pkl"
    if os.path.exists(graph_list_file):
        graph_list = load_from_pickle(graph_list_file)
    else:
        graph_list = graph_generator(i, Arborescence=args.Arborescence)
        save_to_pickle(graph_list, graph_list_file)
    print(f"for variable size of {i},{len(graph_list)} graphs are generated")
    if os.path.exists(all_possible_queries_file):
        all_possible_queries = load_from_pickle(all_possible_queries_file)
    else:
        all_possible_queries = generate_queries(i)
        save_to_pickle(all_possible_queries, all_possible_queries_file)

    graph_max_queries = dict()
    for num,graph in enumerate(graph_list):
        graph_max_queries_file = f"cache_graph_data/graph_max_queries_{i}_{num}.pkl"
        if os.path.exists(graph_max_queries_file):
            graph_max_queries = load_from_pickle(graph_max_queries_file)
        else:
            graph_max_queries[graph] = filter_queries_by_graph(graph, all_possible_queries)
            save_to_pickle(graph_max_queries, graph_max_queries_file)

    for graph in graph_list:
        train_var_sample_num=100+args.additionalsamples
        if i>5:
            train_var_sample_num=2+args.additionalsamples
        for samples in range(train_var_sample_num):
            tables=create_bayesian_tables(graph)
            for query in random.sample(graph_max_queries[graph], min(32-i*3,len(graph_max_queries[graph]))):
                answer,calculation_time=solve_bayesian_inference(graph,tables,query)
                all_examples.append(create_text(graph,tables,query,answer,i,calculation_time))

    print("Time Spent to Generate the Examples: ",time.time()-t0)
    print("Number of Generated Examples",len(all_examples))

contexts,query, answers,graph,depth,query_type,query_state,calculation_time = zip(*all_examples)
contexts,query, answers,graph,depth,query_type,query_state,calculation_time = list(contexts),list(query),list(answers),list(graph),list(depth),list(query_type),list(query_state),list(calculation_time)

df = pd.DataFrame.from_dict({"contexts":contexts,"query":query,"answers":answers,"graph":graph,"depth":depth,"query_type":query_type,"query_state":query_state,"calculation_time":calculation_time})
df = df[df['answers'] >= args.answer_threshold]
df.to_csv("OCT_LLM_TEST.csv")
samples_per_depth = [df[df['depth'] == d].sample(args.Visize, replace=True) for d in df['depth'].unique()]
new_df = pd.concat(samples_per_depth)
new_df.to_csv(args.outputdataset, index=False)

grouped = df.groupby('depth')['answers'].mean()
for depth, avg in grouped.items():
    print(f"Depth: {depth}, Average Answer * 100: {avg * 100:.2f}")

sampled_df = pd.concat(samples_per_depth)
grouped_sampled = sampled_df.groupby('depth')['answers'].mean()
for depth, avg in grouped_sampled.items():
    print(f"Depth: {depth}, Average Answer * 100 (from samples): {avg * 100:.2f}")

print("new_dataset is saved as :",args.outputdataset)
