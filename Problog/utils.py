from problog.program import PrologString
from problog import get_evaluatable
import re, replicate

def problog_excexution(p):
    p += "query(q1).\n"
    p = PrologString(p)
    output = get_evaluatable().create_from(p).evaluate()
    return list(output.values())[0]

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

def replace_numbers(text,numbers):
    matches = re.findall(r"(\w+) = ([\d.]+)", numbers)
    probability_gpt = {key: float(value) for key, value in matches}
    for var_name,num in probability_gpt.items():
        text=text.replace(var_name,str(num))
    return text

def run_LLM(model_name,client,explanation,e1,e2,e3,i,graph_use,number_use,args):
    if model_name in ["gpt-3.5-turbo", "gpt-4-0613"]:
        if not graph_use:
            if not number_use:
                e1_msg="solution:\n"+e1["problog"]
                e2_msg="solution:\n"+e2["problog"]
                e3_msg="solution:\n"+e3["problog"]
            else:
                e1_msg="numbers:\n"+e1["numbers"]+"\nsolution:\n"+e1["problog_with_numbers"]
                e2_msg="numbers:\n"+e2["numbers"]+"\nsolution:\n"+e2["problog_with_numbers"]
                e3_msg="numbers:\n"+e3["numbers"]+"\nsolution:\n"+e3["problog_with_numbers"]
        else:
            e1_msg="numbers:\n"+e1["numbers"]+"\ngraph:\n"+e1["graph"]+"\nsolution:\n"+e1["problog_with_numbers"]
            e2_msg="numbers:\n"+e2["numbers"]+"\ngraph:\n"+e2["graph"]+"\nsolution:\n"+e2["problog_with_numbers"]
            e3_msg="numbers:\n"+e3["numbers"]+"\ngraph:\n"+e3["graph"]+"\nsolution:\n"+e3["problog_with_numbers"]

        openai_messages=[{"role": "system", "content": explanation},
                            {"role": "user", "content": e1["context"]+"\nquestion:\n"+e1["query"]},
                            {"role": "assistant", "content": e1_msg},
                            {"role": "user", "content": e2["context"]+"\nquestion:\n"+e2["query"]},
                            {"role": "assistant", "content": e2_msg},
                            {"role": "user", "content": e3["context"]+"\nquestion:\n"+e3["query"]},
                            {"role": "assistant", "content": e3_msg},
                            {"role": "user", "content": i["contexts"]+"\nquestion:\n"+i["query"]},]

        response = client.chat.completions.create(model=model_name, messages=openai_messages, max_tokens=1500, temperature=0.2)
        response_text=response.choices[0].message.content

    if model_name in ["mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"]:
        if model_name=="mistralai/mistral-7b-instruct-v0.2":model_name="tomasmcm/mistral-7b-instruct-v0.2:366548f07d5859d4c4194f1b3fa28f8be44254928c88ffa4f4e6150df69de1be"
        if not graph_use:
            if not number_use:
                e1_msg="solution:\n"+e1["problog"]
                e2_msg="solution:\n"+e2["problog"]
                e3_msg="solution:\n"+e3["problog"]
            else:
                e1_msg="numbers:\n"+e1["numbers"]+"\nsolution:\n"+e1["problog_with_numbers"]
                e2_msg="numbers:\n"+e2["numbers"]+"\nsolution:\n"+e2["problog_with_numbers"]
                e3_msg="numbers:\n"+e3["numbers"]+"\nsolution:\n"+e3["problog_with_numbers"]
        else:
            e1_msg="numbers:\n"+e1["numbers"]+"\ngraph:\n"+e1["graph"]+"\nsolution:\n"+e1["problog_with_numbers"]
            e2_msg="numbers:\n"+e2["numbers"]+"\ngraph:\n"+e2["graph"]+"\nsolution:\n"+e2["problog_with_numbers"]
            e3_msg="numbers:\n"+e3["numbers"]+"\ngraph:\n"+e3["graph"]+"\nsolution:\n"+e3["problog_with_numbers"]

        prompt_messages=f"<s>[INST] \n{explanation}\n [/INST]  "
        if model_name=="meta/llama-2-70b-chat":
            prompt_messages=f"[INST] <<SYS>>\n{explanation}\n<</SYS>> [/INST] "
        prompt_messages+="[INST]"+e1["context"]+"\nquestion:\n"+e1["query"]+"\nAsnwer:"+"[/INST]"+e1_msg+\
                            "[INST]"+e2["context"]+"\nquestion:\n"+e2["query"]+"\nAsnwer:"+"[/INST]"+e2_msg+\
                            "[INST]"+e3["context"]+"\nquestion:\n"+e3["query"]+"\nAsnwer:"+"[/INST]"+e3_msg+\
                            "[INST]"+i["contexts"]+"\nquestion:\n"+ i["query"]+"\nAsnwer:"+"[/INST]"
        response = replicate.run(
            model_name,
            input={
            "prompt": prompt_messages,
            "temperature": 0.01,
            "max_new_tokens": 2000,
            "min_new_tokens":-1,
            "top_p":0.999,
            "prompt_template":"{prompt}"}
        )
        response_text="".join(response)

    if model_name=="meta/meta-llama-3-70b-instruct":
        
        e1q=e1["context"]+"\nquestion:\n"+e1["query"]
        e2q=e2["context"]+"\nquestion:\n"+e2["query"]
        e3q=e3["context"]+"\nquestion:\n"+e3["query"]
        e_ask=i["contexts"]+"\nquestion:\n"+i["query"]

        if not graph_use:
            if not number_use:
                e1a="solution:\n"+e1["problog"]
                e2a="solution:\n"+e2["problog"]
                e3a="solution:\n"+e3["problog"]
            else:
                e1a="numbers:\n"+e1["numbers"]+"\nsolution:\n"+e1["problog_with_numbers"]
                e2a="numbers:\n"+e2["numbers"]+"\nsolution:\n"+e2["problog_with_numbers"]
                e3a="numbers:\n"+e3["numbers"]+"\nsolution:\n"+e3["problog_with_numbers"]
        else:
            e1a="numbers:\n"+e1["numbers"]+"\ngraph:\n"+e1["graph"]+"\nsolution:\n"+e1["problog_with_numbers"]
            e2a="numbers:\n"+e2["numbers"]+"\ngraph:\n"+e2["graph"]+"\nsolution:\n"+e2["problog_with_numbers"]
            e3a="numbers:\n"+e3["numbers"]+"\ngraph:\n"+e3["graph"]+"\nsolution:\n"+e3["problog_with_numbers"]

        prompt_messages=f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{explanation}<|eot_id|>\
            <|start_header_id|>user<|end_header_id|>\n\n{e1q}<|eot_id|>\
            <|start_header_id|>assistant<|end_header_id|>\n\n{e1a}<|eot_id|>\
            <|start_header_id|>user<|end_header_id|>\n\n{e2q}<|eot_id|>\
            <|start_header_id|>assistant<|end_header_id|>\n\n{e2a}<|eot_id|>\
            <|start_header_id|>user<|end_header_id|>\n\n{e3q}<|eot_id|>\
            <|start_header_id|>assistant<|end_header_id|>\n\n{e3a}<|eot_id|>\
            <|start_header_id|>user<|end_header_id|>\n\n{e_ask}<|eot_id|>\
            <|start_header_id|>assistant<|end_header_id|>\n\n"

        response = replicate.run(
            model_name,
            input={
                "top_p": 0.9999,
                "prompt": prompt_messages,
                "max_tokens": 2000,
                "min_tokens": 2,
                "temperature": 0.0,
                "prompt_template": "{prompt}"
            },
        )
        response_text="".join(response)

    return response_text

