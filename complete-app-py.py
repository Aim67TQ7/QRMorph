import gradio as gr
from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import requests
import base64
import os
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()

# ZeroGPU API details
ZEROGPU_API_URL = "https://api.zerogpu.com/generate"
ZEROGPU_API_KEY = os.getenv("ZEROGPU_API_KEY")

def create_qr_with_logo(url, logo, logo_size=0.2):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white", image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()).convert('RGBA')
    
    if logo:
        logo_img = Image.open(logo).convert('RGBA')
        logo_max_size = int(min(qr_img.size) * logo_size)
        logo_img.thumbnail((logo_max_size, logo_max_size), Image.LANCZOS)
        
        box = ((qr_img.size[0] - logo_img.size[0]) // 2,
               (qr_img.size[1] - logo_img.size[1]) // 2)
        
        white_box = Image.new('RGBA', logo_img.size, 'white')
        qr_img.paste(white_box, box, white_box)
        qr_img.paste(logo_img, box, logo_img)
    
    return qr_img

def style_qr_code_zerogpu(qr_image, prompt, guidance_scale=7.5, controlnet_conditioning_scale=1.0):
    # Convert PIL Image to base64
    buffered = BytesIO()
    qr_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Prepare the payload for ZeroGPU API
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, low quality",
        "image": img_str,
        "guidance_scale": guidance_scale,
        "controlnet_conditioning_scale": controlnet_conditioning_scale,
        "num_inference_steps": 30,
        "controlnet_model": "monster-labs/control_v1p_sd15_qrcode_monster",
        "base_model": "SG161222/Realistic_Vision_V5.1_noVAE"
    }

    # Make API request
    headers = {
        "Authorization": f"Bearer {ZEROGPU_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(ZEROGPU_API_URL, json=payload, headers=headers)

    if response.status_code == 200:
        # Decode the image from base64
        img_data = base64.b64decode(response.json()["image"])
        return Image.open(BytesIO(img_data))
    else:
        raise Exception(f"Error from ZeroGPU API: {response.text}")

def generate_styled_qr(url, logo, logo_size, prompt, guidance_scale, controlnet_conditioning_scale):
    # Step 1: Generate QR code with logo
    qr_with_logo = create_qr_with_logo(url, logo, logo_size)
    
    # Step 2: Style the QR code using ZeroGPU
    styled_qr = style_qr_code_zerogpu(qr_with_logo, prompt, guidance_scale, controlnet_conditioning_scale)
    
    return styled_qr

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# AI-Styled QR Code Generator with Logo (ZeroGPU)")
    
    with gr.Row():
        with gr.Column():
            url_input = gr.Textbox(label="QR Code Content (URL or Text)")
            logo_upload = gr.Image(type="filepath", label="Upload Logo (optional)")
            logo_size = gr.Slider(minimum=0.1, maximum=0.5, value=0.2, step=0.05, label="Logo Size")
            prompt = gr.Textbox(label="Style Prompt")
            guidance_scale = gr.Slider(minimum=1, maximum=20, value=7.5, step=0.5, label="Guidance Scale")
            controlnet_scale = gr.Slider(minimum=0.1, maximum=2.0, value=1.0, step=0.1, label="ControlNet Conditioning Scale")
            generate_btn = gr.Button("Generate Styled QR Code")
        
        with gr.Column():
            output_image = gr.Image(label="Styled QR Code")
    
    generate_btn.click(
        generate_styled_qr,
        inputs=[url_input, logo_upload, logo_size, prompt, guidance_scale, controlnet_scale],
        outputs=output_image
    )

if __name__ == "__main__":
    demo.launch()
