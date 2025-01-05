import replicate

def run_LLM(model_name,client,explanation,e1,e2,e3,i,few_shot,args):
    if model_name in ["gpt-3.5-turbo", "gpt-4-0613"]:
        if few_shot:
            openai_messages=[{"role": "system", "content": explanation},
                                {"role": "user", "content": e1["context"]+"\nquestion:\n"+e1["query"]},
                                {"role": "assistant", "content": e1[args.method]},
                                {"role": "user", "content": e2["context"]+"\nquestion:\n"+e2["query"]},
                                {"role": "assistant", "content": e2[args.method]},
                                {"role": "user", "content": e3["context"]+"\nquestion:\n"+e3["query"]},
                                {"role": "assistant", "content": e3[args.method]},
                                {"role": "user", "content": i["contexts"]+"\nquestion:\n"+i["query"]},]
        else:
            openai_messages=[{"role": "assistant", "content": explanation},
                                {"role": "user", "content": i["contexts"]+"\nquestion:\n"+i["query"]},]

        response = client.chat.completions.create(model=model_name, messages=openai_messages, max_tokens=1500, temperature=0.2)
        response_text=response.choices[0].message.content
    if model_name in ["mistralai/mistral-7b-instruct-v0.2", "meta/llama-2-70b-chat"]:
        if model_name=="mistralai/mistral-7b-instruct-v0.2":model_name="tomasmcm/mistral-7b-instruct-v0.2:366548f07d5859d4c4194f1b3fa28f8be44254928c88ffa4f4e6150df69de1be"
        prompt_messages=f"<s>[INST] \n{explanation}\n [/INST] [INST] example : what is the probablity of a coin flip?[/INST] 50 "
        if model_name=="meta/llama-2-70b-chat":
            prompt_messages=f"[INST] <<SYS>>\n{explanation}\n<</SYS>> example : what is the probablity of a coin flip?[/INST] 50 "

        if few_shot:
            prompt_messages+="[INST]"+e1["context"]+"\nquestion:\n"+e1["query"]+"\nAsnwer:"+"[/INST]"+e1[args.method]+\
                            "[INST]"+e2["context"]+"\nquestion:\n"+e2["query"]+"\nAsnwer:"+"[/INST]"+e2[args.method]+\
                            "[INST]"+e3["context"]+"\nquestion:\n"+e3["query"]+"\nAsnwer:"+"[/INST]"+e3[args.method]+\
                            "[INST]"+i["contexts"]+"\nquestion:\n"+ i["query"]+"\nAsnwer:"+"[/INST]"
        else:
            prompt_messages+= "[INST]"+i["contexts"]+"\nquestion:\n"+i["query"]+"\nAsnwer:"+"[/INST]"

        response = replicate.run(
            model_name,
            input={
            "prompt": prompt_messages,
            "temperature": 0.01,
            "max_new_tokens": 2000 if args.method=="COT" else 20,
            "min_new_tokens":-1,
            "top_p":0.999,
            "prompt_template":"{prompt}"}
        )
        response_text="".join(response)

    if model_name=="meta/meta-llama-3-70b-instruct":
        e_ask=i["contexts"]+"\nquestion:\n"+ i["query"]+"\nAsnwer:"
        if few_shot:
            e1q=e1["context"]+"\nquestion:\n"+e1["query"]+"\nAsnwer:"
            e1a=e1[args.method]
            e2q=e2["context"]+"\nquestion:\n"+e2["query"]+"\nAsnwer:"+"[/INST]"
            e2a=e2[args.method]
            e3q=e3["context"]+"\nquestion:\n"+e3["query"]+"\nAsnwer:"+"[/INST]"
            e3a=e3[args.method]
            
            prompt_messages=f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{explanation}<|eot_id|>\
                    <|start_header_id|>user<|end_header_id|>\n\n{e1q}<|eot_id|>\
                    <|start_header_id|>assistant<|end_header_id|>\n\n{e1a}<|eot_id|>\
                    <|start_header_id|>user<|end_header_id|>\n\n{e2q}<|eot_id|>\
                    <|start_header_id|>assistant<|end_header_id|>\n\n{e2a}<|eot_id|>\
                    <|start_header_id|>user<|end_header_id|>\n\n{e3q}<|eot_id|>\
                    <|start_header_id|>assistant<|end_header_id|>\n\n{e3a}<|eot_id|>\
                    <|start_header_id|>user<|end_header_id|>\n\n{e_ask}<|eot_id|>\
                    <|start_header_id|>assistant<|end_header_id|>\n\n"
        else:
            prompt_messages=f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{explanation}<|eot_id|>\
                    <|start_header_id|>user<|end_header_id|>\n\n{e_ask}<|eot_id|>\
                    <|start_header_id|>assistant<|end_header_id|>\n\n"

        response = replicate.run(
            model_name,
            input={
                "top_p": 0.95,
                "prompt": prompt_messages,
                "max_tokens": 2000 if args.method=="COT" else 20,
                "min_tokens": 2,
                "temperature": 0.0,
                "prompt_template": "{prompt}"
            },
        )
        response_text="".join(response)

    return response_text