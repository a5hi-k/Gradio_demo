from fastapi import FastAPI

import gradio as gr


from vton_demo import demo


app = FastAPI()

@app.get('/')
async def root():
    return "running",200

app = gr.mount_gradio_app(app, demo, path='/gradio')