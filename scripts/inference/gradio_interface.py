import torch
from transformers import LlamaForCausalLM, LlamaTokenizer
import gradio as gr
from flask import Flask, request, jsonify

app = Flask(__name__)
# Perform inference
@torch.no_grad()
def run_inference(input_text, tokenizer, model, **kwargs):
    input_ids = tokenizer.encode(input_text, add_special_tokens=True, return_tensors="pt")
    input_ids = input_ids.to(model.device)

    # Perform model inference
    outputs = model.generate(input_ids, **kwargs)
    predicted_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return predicted_text

# Gradio interface
def gradio_interface(tokenizer, model):
    def chatbot_interface(input_text):
        predicted_text = run_inference(input_text, tokenizer, model)
        return predicted_text

    iface = gr.Interface(
        fn=chatbot_interface,
        inputs=gr.inputs.Textbox(lines=10, label="Input Text"),
        outputs="text",
        title="Chatbot",
        live=True
    )
    return iface

# Load and initialize the model
def load_model(base_model_path, tokenizer_path, lora_model_path, load_in_8bit):
    tokenizer = LlamaTokenizer.from_pretrained(tokenizer_path, legacy=True)
    base_model = LlamaForCausalLM.from_pretrained(
        base_model_path,
        load_in_8bit=load_in_8bit,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        device_map='auto',
    )
    # ... Initialize the model based on your requirements ...
    return tokenizer, base_model

# API endpoint for prediction
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_text = data['input_text']
    result = run_inference(input_text, tokenizer, model)
    return jsonify({'prediction': result})


if __name__ == '__main__':
    base_model_path = '/mnt/mydisk/llama2_models/chinese-alpaca-2-7b/'
    tokenizer_path = '/mnt/mydisk/llama2_models/chinese-alpaca-2-7b/'
    lora_model_path = '/mnt/mydisk/llama2_models/chinese-alpaca-2-lora-7b/'  # If applicable
    load_in_8bit = True  # Set to True if using 8-bit quantified model

    tokenizer, model = load_model(
        base_model_path, tokenizer_path, lora_model_path, load_in_8bit)

    gr_interface = gradio_interface(tokenizer, model)
    gr_interface.launch(share=True)
