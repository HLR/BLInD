import re

def extract_sections(text):
    numbers_pattern = r'numbers:(.*?)(?=graph:|solution:|$)'
    graph_pattern = r'graph:(.*?)(?=numbers:|solution:|$)'
    solution_pattern = r'solution:(.*?)(?=numbers:|graph:|$)'

    numbers_section = re.search(numbers_pattern, text, re.DOTALL)
    graph_section = re.search(graph_pattern, text, re.DOTALL)
    solution_section = re.search(solution_pattern, text, re.DOTALL)

    numbers_text = numbers_section.group(1).strip() if numbers_section else ''
    graph_text = graph_section.group(1).strip() if graph_section else ''
    solution_text = solution_section.group(1).strip() if solution_section else ''

    return numbers_text, graph_text, solution_text

