---
title: QR Code Image Blender
emoji: 🖼️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 3.23.0
app_file: app.py
pinned: false
---

# QR Code Image Blender

This Gradio app allows you to blend QR codes with your uploaded images using AI-powered image generation techniques.

## Features

- Upload your own image
- Generate a QR code from any text or URL
- Blend the QR code with your image using Stable Diffusion
- Adjust blend strength for custom results
- Set a seed for reproducible outputs

## How to Use

1. Upload an image you want to blend with a QR code.
2. Enter the content for the QR code (text or URL).
3. Adjust the blend strength slider to control how much the QR code affects the final image.
4. (Optional) Set a seed for reproducible results.
5. Click "Submit" to generate your blended image.

## Technical Details

This app uses:
- Stable Diffusion v1.5 for image generation
- ControlNet with a canny edge detector for structure preservation
- QR code generation with the qrcode library
- Gradio for the user interface

The app runs on a GPU for faster processing.

## Installation

To run this app locally, clone the repository and install the required packages:

```
pip install -r requirements.txt
```

Then run:

```
python app.py
```

## Acknowledgements

This project uses models from the Hugging Face model hub and is inspired by various QR code art generators in the AI community.

## License

This project is open source and available under the MIT License.

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
