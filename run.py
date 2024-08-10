# from fastapi import FastAPI

# import gradio as gr


# from vton_demo import demo


# app = FastAPI()

# @app.get('/')
# async def root():
#     return "running",200

# app = gr.mount_gradio_app(app, demo, path='/gradio')





import os
from fastapi import FastAPI
import gradio as gr
from vton_demo import demo
import uvicorn

app = FastAPI()

@app.get('/')
async def root():
    return "include /gradio/ in the url", 200

# Mount the Gradio demo app at the '/gradio' path
app = gr.mount_gradio_app(app, demo, path='/gradio')

if __name__ == "__main__":
    # Bind to the port provided by the environment variable `PORT`, or default to 8000
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)