import random, itertools, re, pickle
import time

import networkx as nx
import numpy as np
from pgmpy.factors.discrete import TabularCPD
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
random.seed(2023)
def random_combination_of_permutations(nodes, number_of_variables):
    random_permutation = random.choice(list(itertools.permutations(nodes, 2)))
    selected_permutations = {random_permutation}
    for _ in range(number_of_variables - 2):
        while True:
            random_permutation = random.choice(list(itertools.permutations(nodes, 2)))
            if random_permutation not in selected_permutations:
                selected_permutations.add(random_permutation)
                break
    return tuple(selected_permutations)

def graph_generator(number_of_variables,max_iter=10000,Arborescence=False):
    nodes = ["n" + str(i) for i in range(number_of_variables)]
    all_graphs = []
    for _ in range(max_iter):
        edges=random_combination_of_permutations(nodes, number_of_variables)
        graph = nx.DiGraph(list(edges))
        if len(graph.nodes())<number_of_variables:
            continue
        if nx.is_directed_acyclic_graph(graph) and nx.is_connected(graph.to_undirected()):
            if Arborescence:
                if max([len(list(graph.predecessors(node))) for node in graph.nodes()]) <= 1:
                    if not any(nx.is_isomorphic(graph, g) for g in all_graphs):
                        all_graphs.append(graph)
            else:
                if not any(nx.is_isomorphic(graph, g) for g in all_graphs):
                    all_graphs.append(graph)

    outputs=[]
    for graph in all_graphs:
        output_dict = {}
        for node in nodes:
            parents = list(graph.predecessors(node))
            if len(parents) == 0:
                output_dict[node] = ()
            else:
                for parent in parents:
                    if node in output_dict:
                        output_dict[node] += (parent,)
                    else:
                        output_dict[node] = (parent,)

        output = ""
        for key, value in output_dict.items():
            output += "{} -> {} | ".format(value, key)
        outputs.append(output.rstrip(" | "))

    return outputs

def create_bayesian_tables(input_graph,fixed_numbers=False):
    list_of_tables_of_probabilities = []
    if fixed_numbers:
        probabilities = [[10*i,100-10*i] for i in range(1,10,1)]
    else:
        probabilities = [[1*i,100-1*i] for i in range(1,100,1)]
    graph_elements = input_graph.split(" | ")
    for element in graph_elements:
        parents_str, node = element.split(" -> ")
        parents = re.findall(r"n\d", parents_str)
        num_parent_states = 2 ** len(parents)
        table = []
        for _ in range(num_parent_states):
            prob_choice = random.choice(probabilities)
            table.append(prob_choice)
        list_of_tables_of_probabilities.append(np.array(table))
    return list_of_tables_of_probabilities

#CHECK THIS
def create_model(input_graph, list_of_tables_of_probabilities):
    edges = []
    cpds = []
    graph_elements = input_graph.split(" | ")
    for i, element in enumerate(graph_elements):
        parents_str, node = element.split(" -> ")
        parents = re.findall(r"n\d", parents_str)
        edges.extend([(parent, node) for parent in parents])
        cpd_table = list_of_tables_of_probabilities[i]/100
        if len(parents) == 0:
            cpd = TabularCPD(node, 2, [cpd_table[:, 1], cpd_table[:, 0]])
        else:
            cpd = TabularCPD(node, 2, cpd_table.T[::-1].tolist(), evidence=parents, evidence_card=[2] * len(parents))
        cpds.append(cpd)
    model = BayesianNetwork(edges)
    model.add_cpds(*cpds)
    return model

def parse_query(query):
    # Parse the query
    query_vars, evidence_vars, ignored_vars = query.split("|")
    # Convert strings to lists of variables
    query_vars = [query_vars[i:i+2] for i in range(0,len(query_vars),2)]
    evidence_vars = [evidence_vars[i:i+2] for i in range(0,len(evidence_vars),2)]
    return query_vars, evidence_vars, ignored_vars

def solve_bayesian_inference(input_graph, list_of_tables_of_probabilities, query="n1|n2|n3"):

    model = create_model(input_graph, list_of_tables_of_probabilities)
    query_vars, evidence_vars, ignored_vars = parse_query(query)
    inference = VariableElimination(model)
    results = []
    query_nodes=query_vars
    evidence_nodes = evidence_vars
    evidence_combinations = list(itertools.product([False, True], repeat=len(evidence_nodes)))
    calculation_times=[]
    for evidence_values in evidence_combinations:
        evidence = dict(zip(evidence_nodes, evidence_values))
        t0 = time.perf_counter()
        result = inference.query(variables=list(query_nodes), evidence=evidence)
        calculation_times.append((time.perf_counter()-t0)*1000)
        results.append(result)
    return results,calculation_times

def all_query_generator(variable_num):
    list_of_queries = []
    variables = ['n' + str(i) for i in range(1, variable_num + 1)]
    for r in range(1, variable_num + 1):
        for query_vars in itertools.combinations(variables, r):
            remaining_vars = list(set(variables) - set(query_vars))
            for s in range(0, len(remaining_vars) + 1):
                for evidence_vars in itertools.combinations(remaining_vars, s):
                    ignored_vars = list(set(remaining_vars) - set(evidence_vars))
                    query = ''.join(query_vars) + '|' + ''.join(evidence_vars) + '|' + ''.join(ignored_vars)
                    list_of_queries.append(query)
    return list_of_queries

from itertools import combinations, permutations

def partitions(n):
    numbers = ["n" + str(i) for i in range(0, n)]
    parts = []
    for i in range(1, len(numbers)+1):  # Start from 1 to avoid empty first group
        for first_group in combinations(numbers, i):
            remaining = [num for num in numbers if num not in first_group]
            for j in range(len(remaining)+1):
                for second_group in combinations(remaining, j):
                    third_group = tuple(num for num in remaining if num not in second_group)
                    parts.append((first_group, second_group, third_group))
    return parts

def generate_queries(n):
    all_parts = partitions(n)
    queries = []
    for part in all_parts:
        query = "|".join("".join(group) for group in part)
        query = query.rsplit("|", 1)[0]+"|"  # Remove everything after the last "|"
        queries.append(query)
    return queries

def create_text(graph, tables, query, answer,depth,calculation_time):
    """
    Explains the bayesian network in form of text. For examples if n1 is true then n2 is true with probality of 30%. n1 is true with probability of 10%.
    :param graph: () -> n1 | ('n1',) -> n2 | ('n1',) -> n3 , () -> n1 | ('n1',) -> n2 | ('n2',) -> n3 , ... of maximum size 5 nodes
    :param tables: [array([[70, 30]]), array([[20, 80], [80, 20]]), array([[70, 30], [50, 50]])] , [array([[10, 90]]),
    array([[80, 20], [70, 30]]), array([[70, 30], [80, 20]])] ,
    ...

    :param query: n1|n2|n3 ,  n1n3|n2| , n1||n2n3
    :param answer: [<DiscreteFactor representing phi(n1:2) at 0x17d385c5070>, <DiscreteFactor representing phi(n1:2) at 0x17d385c5310>],
     [<DiscreteFactor representing phi(n1:2) at 0x17d385c8160>],
     [<DiscreteFactor representing phi(n1:2, n3:2) at 0x17d385c7d00>],
     ...
    :return: ( context: if n1 is true then n2 is true with probality of 30%. n1 is true with probability of 10%. ...  )
    """
    explanation = ""

    for node_parents, table in zip(graph.split("|"), tables):
        # Extract node and its parents
        node_parents = node_parents.strip().split(" -> ")
        node = node_parents[-1]
        parents = node_parents[0].strip("()").replace("'","").split(",")
        parents=[p for p in parents if not p=='']
        # Build explanation from the probability table
        table = np.squeeze(table)
        if len(parents)==0:
            explanation += f"{node} is true with probability of {table[0]}%. "
            explanation += f"{node} is false with probability of {table[1]}%. "
        else:
            for parent_states in itertools.product([False, True], repeat=len(parents)):
                for j, state in enumerate(['True', 'False']):
                    parent_conditions = " and ".join(
                        [f"{parent.strip()} is {str(parent_state)}" for parent, parent_state in
                         zip(parents, parent_states)])
                    probability = table[tuple(int(state) for state in parent_states), j][0]
                    explanation += f"If {parent_conditions}, then {node} is {state} with probability of {probability}%. "

    queries=[]
    answers=[]
    query_nodes=query.split("|")[0].strip()
    query_nodes=[query_nodes[i:i + 2] for i in range(0, len(query_nodes), 2)]
    evidence=query.split("|")[1].strip()
    evidence=[evidence[i:i + 2] for i in range(0, len(evidence), 2)]
    for evidence_states in itertools.product(["False", "True"], repeat=len(evidence)):
        evidence_conditions = " and ".join([f"{e} is {state}" for e, state in zip(evidence, evidence_states)])
        for query_states in itertools.product(['False', 'True'], repeat=len(query_nodes)):
            query_conditions = " and ".join([f"{qn} is {state}" for qn, state in zip(query_nodes, query_states)])
            queries.append(f"What is the probability that {query_conditions} given that {evidence_conditions}?".replace(" given that ?","?"))

    def find_booleans(text):
        matches = re.findall(r'\b(true|false)\b', text, re.IGNORECASE)
        return ''.join('t' if match.lower() == 'true' else 'f' for match in matches)

    for a,c in zip(answer,calculation_time):
        for i in list(a.values.flatten()):
            answers.append((i,c))

    assert len(queries)==len(answers)

    return random.choice([(explanation, q, a[0],graph,depth,query,find_booleans(q),a[1]) for q, a in zip(queries, answers)])

def query_uses_all_nodes(graph, query):
    nodes=dict()
    edges=dict()
    for node_parents in graph.split("|"):
        node_parents = node_parents.strip().split(" -> ")
        node = node_parents[-1]
        parents = node_parents[0].strip("()").replace("'", "").split(",")
        parents = [p for p in parents if not p == '']
        if len(parents)==1:
            edges[parents[-1]] = node
            nodes[parents[-1]] = False
        nodes[node]=False
    query_vars, evidence_vars, _ = parse_query(query)
    for i in query_vars+evidence_vars:
        nodes[i]=True

    for node in nodes.keys():
        if not nodes[node] and not node in edges:
            return False
    return True

def filter_queries_by_graph(graph, all_possible_queries):
    return [query for query in all_possible_queries if query_uses_all_nodes(graph,query)]

def save_to_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_from_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

