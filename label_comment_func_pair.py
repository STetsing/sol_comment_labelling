import gradio as gr
import numpy as np
import json
from tqdm import tqdm
from datasets import load_dataset
from datetime import datetime


data = load_dataset("Pipper/SolFuncs", split="test")
label_results_file = './labels.txt'
flagged = "./flagged.txt"

def com_code_generator(dataset):
    for x in range(0, len(dataset)):
        fname = dataset[x]["file_name"]
        comment = dataset[x]["comments"]
        code = dataset[x]["code_string"]
        yield fname, comment, code

    return "Done"

data_gen = com_code_generator(data)

def record_input(fname, com, code, flag=False):
    if flag:
        output = {"file_name":fname, "comments":com, "code_string":code}
        with open(flagged, 'wa') as fhl: 
            json.dump(output, fhl)
            fhl.write("\n")
    else:
        output = {"comments":com, "code_string":code}
        with open(label_results_file, 'a') as fhl: 
            json.dump(output, fhl)
            fhl.write("\n")
    f, co, cd = next(data_gen)
    return f, co, cd 

def Start():
    f, co, cd = next(data_gen)
    return f, co, cd 

with gr.Blocks(theme=gr.themes.Default(primary_hue=gr.themes.colors.green, secondary_hue=gr.themes.colors.green)) as app:
    gr.Markdown(
    """
    # Label Solidity Comment-Code Pair
    - First press the `Start` button to get started.
    - Analyze both the comment and the associated code
    - Correct either the comment or the code to be aligned. Also correct both is necessary
    - If possible reduce the comment to be shorter and precise
    - Press `Submit` to submit a valid label pair
    - Press `Flag` to flag the comment-code pair if those do the fit at all
    - A new comment-code pair will be displyed to be labeled

    P.S. Each piece of code originates from a contract file, therefore some variable might be declared outside the function scope
    """)

    start_btn = gr.Button("Start", variant="primary")
    fname = gr.Textbox("Contract File name", visible=False)
    comment = gr.Textbox("Comment", visible=True, show_copy_button=True, label="Comment", )
    code = gr.Textbox("Code", visible=True, show_copy_button=True, label="Associated code")
    with gr.Row():
        submit = gr.Button("Submit", variant="secondary")
        flag = gr.Button("Flag", variant="secondary")

    start_btn.click(fn=Start, outputs= [fname, comment, code])
    submit.click(record_input, inputs=[fname, comment, code], outputs=[fname, comment, code])
    flag.click(record_input, inputs=[fname, comment, code], outputs=[fname, comment, code])

if __name__ == "__main__":
    app.queue()
    app.launch(share=False)

# demo = gr.ChatInterface(random_response)

# demo.launch()