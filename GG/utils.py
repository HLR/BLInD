import replicate

def run_LLM(model_name,client,explanation,e1,e2,e3,i):
    if model_name in ["gpt-3.5-turbo", "gpt-4-0613"]:
        openai_messages=[{"role": "system", "content": explanation},
                                    {"role": "user", "content": e1["context"]},
                                    {"role": "assistant", "content": e1["graph"]},
                                    {"role": "user", "content": e2["context"]},
                                    {"role": "assistant", "content": e2["graph"]},
                                    {"role": "user", "content": e3["context"]},
                                    {"role": "assistant", "content": e3["graph"]},
                                    {"role": "user", "content": i["contexts"]},]
        response = client.chat.completions.create(model=model_name, messages=openai_messages, max_tokens=500, temperature=0.2)
        response_text=response.choices[0].message.content
    
    if model_name in ["mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"]:
        if model_name=="mistralai/mistral-7b-instruct-v0.2":model_name="tomasmcm/mistral-7b-instruct-v0.2:366548f07d5859d4c4194f1b3fa28f8be44254928c88ffa4f4e6150df69de1be"
        prompt_messages=f"<s>[INST] \n{explanation}\n [/INST]  "
        if model_name=="meta/llama-2-70b-chat":
            prompt_messages=f"[INST] <<SYS>>\n{explanation}\n<</SYS>> [/INST] "
        prompt_messages+="[INST]"+e1["context"]+"[/INST]"+e1["graph"]+\
                            "[INST]"+e2["context"]+"[/INST]"+e2["graph"]+\
                            "[INST]"+e3["context"]+"[/INST]"+e3["graph"]+\
                            "[INST]"+i["contexts"]+"[/INST]"
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
        e1q, e2q, e3q, e_ask = e1["context"], e2["context"], e3["context"], i["contexts"]
        e1a, e2a, e3a = e1["graph"], e2["graph"], e3["graph"]

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
                "top_p": 0.95,
                "prompt": prompt_messages,
                "max_tokens": 2000,
                "min_tokens": 2,
                "temperature": 0.0,
                "prompt_template": "{prompt}"
            },
        )
        response_text="".join(response)

    return response_text