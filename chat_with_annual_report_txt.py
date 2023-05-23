import openai
import gradio as gr
from search_model import SearchModel, load_searching_model


def generate_text(openAI_key, prompt, engine="gpt-3.5-turbo"):
    openai.api_key = openAI_key
    completions = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = completions.choices[0].text
    return message


def generate_answer(question, openAI_key, searching_model, prompt_instructions):
    topn_chunks = searching_model(question)
    prompt = "Background: This data contains the annual report of a company."
    prompt += "search results:\n\n"
    for c in topn_chunks:
        # Decrease the amount of text to fit in 2000 tokens
        # Because of the models context limits
        if len(prompt) >= 2800:
            break
        prompt += c + "\n\n"

    if len(prompt) > 2800:
        prompt = prompt[:2800]

    prompt += prompt_instructions
    prompt += f"Query: {question}\nAnswer:"
    print(prompt)
    answer = generate_text(openAI_key, prompt, "text-davinci-003")
    return answer


def question_answer(company, year, question, openAI_key):
    global searching_model
    global prompt_instructions

    if openAI_key.strip() == "":
        return "[ERROR]: Please enter you Open AI Key. Key found here : https://platform.openai.com/account/api-keys"
    if company not in ["AAPL", "AMZN", "GOOGL", "MSFT"]:
        return "[ERROR]: Please provide company name in AAPL, AMZN, GOOGL, MSFT"
    if year not in ["2018", "2019", "2020", "2021", "2022"]:
        return "[ERROR]: Please provide year in 2018-2022(inclusive)"

    if question.strip() == "":
        return "[ERROR]: Question field is empty"

    file_path = f"annual_report_data/{company}_json/{year}-Annual-Report.json"
    searching_model = load_searching_model(searching_model, file_path)
    return generate_answer(question, openAI_key, searching_model, prompt_instructions)


searching_model = SearchModel()
# Open Prompt instructions file
with open("prompt_instructions.txt", "r") as f:
    prompt_instructions = f.read()

title = "Financial Analysis GPT"
description = """ Financial GPT allows you to get finiancial analysis using Sentence Transformers and Open AI GPT-3.5-turbo."""
with gr.Blocks() as demo:
    gr.Markdown(f"<center><h1>{title}</h1></center>")
    gr.Markdown(description)
    with gr.Row():
        with gr.Group():
            gr.Markdown(
                f'<p style="text-align:center">Get your Open AI API key <a href="https://platform.openai.com/account/api-keys">here</a></p>'
            )
            openAI_key = gr.Textbox(label="Enter your OpenAI API key here")
            company = gr.Textbox(label="Enter the company name here")
            year = gr.Textbox(label="Enter the annual report year here")
            question = gr.Textbox(label="Enter your question here")
            btn = gr.Button(value="Submit")
            btn.style(full_width=True)

        with gr.Group():
            answer = gr.Textbox(label="The answer to your question is :")

        btn.click(
            question_answer,
            inputs=[company, year, question, openAI_key],
            outputs=[answer],
        )
demo.launch()
