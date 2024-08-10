
import gradio as gr
from gradio_client import Client, file
import tempfile
import os
from PIL import Image

client = Client("zen-vton/IDM-VTON")

# username = "zen-vton"
# password = "Zen@vton2024"

# client = Client(
#   "zen-vton/IDM-VTON",
#   auth=[username, password]
# )


def process_images(human_image, garment_image, garment_description, is_checked, is_checked_crop, denoise_steps, seed):
    if human_image is None and garment_image is None:
        return None, None

    human_image_path = os.path.join(tempfile.gettempdir(), "human_image.png")
    garment_image_path = os.path.join(tempfile.gettempdir(), "garment_image.png")
    
    human_image.save(human_image_path)
    garment_image.save(garment_image_path)
    
    
    try:
        result = client.predict(
            dict={"background": file(human_image_path), "layers": [], "composite": None},
            garm_img=file(garment_image_path),
            garment_des=garment_description,
            is_checked=is_checked,
            is_checked_crop=is_checked_crop,
            denoise_steps=denoise_steps,
            seed=seed,
            api_name="/tryon"
        )
            
        output_image_path, _ = result
        
        # print(f"Output image path: {output_image_path}")
            
        output_image = Image.open(output_image_path)
        
        # Save the output image to a temporary path for download
        output_image_temp_path = os.path.join(tempfile.gettempdir(), "output_image.png")
        output_image.save(output_image_temp_path)
            
        return output_image, output_image_temp_path
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def clear():
    return (None, None, "A Round Neck T-shirt", True, False, 30, 42, None, None)

# Define the Gradio interface
with gr.Blocks(css=".btn-green {background-color: green; color: white;}") as demo:
    with gr.Row():
        with gr.Column():
            human_image = gr.Image(type="pil", label="Human Image")
            garment_image = gr.Image(type="pil", label="Garment Image")
            garment_description = gr.Textbox(label="Garment Description", value="A Round Neck T-shirt", visible=False)
            is_checked = gr.Checkbox(label="Auto Mask", value=True, visible=False)
            is_checked_crop = gr.Checkbox(label="Crop", value=False, visible=False)
            denoise_steps = gr.Slider(label="Denoise Steps", minimum=0, maximum=100, step=1, value=30, visible=False)
            seed = gr.Slider(label="Seed", minimum=0, maximum=100, step=1, value=42, visible=False)
            try_on_button = gr.Button("Try On", elem_classes="btn-green")
            clear_button = gr.Button("Clear")

        with gr.Column():
            output_image = gr.Image(label="Output Image")
            download_button = gr.File(label="Download Image")

    def on_try_on_click(human_image, garment_image, garment_description, is_checked, is_checked_crop, denoise_steps, seed):
        output_image, output_image_temp_path = process_images(human_image, garment_image, garment_description, is_checked, is_checked_crop, denoise_steps, seed)
        return output_image, output_image_temp_path

    def on_clear_click():
        return None, None, "A Round Neck T-shirt", True, False, 30, 42, None, None
    
    try_on_button.click(
        on_try_on_click, 
        inputs=[human_image, garment_image, garment_description, is_checked, is_checked_crop, denoise_steps, seed],

        outputs=[output_image, download_button]   

    )

    clear_button.click(
        on_clear_click, 
        inputs=[], 
        outputs=[human_image, garment_image, garment_description, is_checked, is_checked_crop, denoise_steps, seed, output_image, download_button]  

    )

demo.launch(debug=True, share=True, show_error=True)
