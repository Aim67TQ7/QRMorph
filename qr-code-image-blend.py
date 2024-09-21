import torch
import gradio as gr
from PIL import Image
import qrcode
from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel
from diffusers.schedulers import DDIMScheduler
import numpy as np

# Load models
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet,
    safety_checker=None,
    torch_dtype=torch.float16
).to("cuda")
pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

def generate_qr_code(url, size=512):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size))
    return img

def preprocess_image(image):
    image = image.resize((512, 512))
    image = np.array(image)
    image = torch.from_numpy(image).float() / 255.0
    image = image.permute(2, 0, 1).unsqueeze(0)
    return image

def blend_images(uploaded_image, qr_code_content, blend_strength=0.5, seed=-1):
    # Generate QR code
    qr_image = generate_qr_code(qr_code_content)
    
    # Preprocess images
    init_image = preprocess_image(uploaded_image)
    qr_image = preprocess_image(qr_image)
    
    # Set up generator
    if seed != -1:
        generator = torch.manual_seed(seed)
    else:
        generator = torch.Generator(device="cuda").manual_seed(torch.randint(0, 1000000, (1,)).item())
    
    # Run Stable Diffusion
    output = pipe(
        prompt="Seamless blend of image and QR code",
        image=init_image,
        control_image=qr_image,
        strength=blend_strength,
        guidance_scale=7.5,
        controlnet_conditioning_scale=1.0,
        generator=generator,
        num_inference_steps=50
    ).images[0]
    
    return output

# Gradio interface
def run_interface(uploaded_image, qr_code_content, blend_strength, seed):
    if uploaded_image is None:
        raise gr.Error("Please upload an image")
    if not qr_code_content:
        raise gr.Error("Please enter QR code content")
    
    result = blend_images(uploaded_image, qr_code_content, blend_strength, seed)
    return result

iface = gr.Interface(
    fn=run_interface,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Textbox(label="QR Code Content"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.5, label="Blend Strength"),
        gr.Slider(minimum=-1, maximum=9999999999, step=1, value=-1, label="Seed", randomize=True)
    ],
    outputs=gr.Image(type="pil", label="Result"),
    title="QR Code Image Blender",
    description="Upload an image and enter QR code content to blend them using AI."
)

iface.launch()
