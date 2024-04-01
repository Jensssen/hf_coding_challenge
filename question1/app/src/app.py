import random
import gradio as gr


def random_response(message, history):
    return random.choice(["Yes", "No"])


# run the app
gr.ChatInterface(random_response).launch(server_name="0.0.0.0",
                                         server_port=8080)
