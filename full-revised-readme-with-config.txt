---
title: AI-Styled QR Code Generator
emoji: 🎨
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 3.35.2
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# AI-Styled QR Code Generator with Logo (ZeroGPU Integration)

This application generates custom QR codes with embedded logos and applies AI-generated styles using ZeroGPU's API. It combines traditional QR code generation with advanced AI image styling, all without requiring a local GPU.

## Features

- Generate QR codes with customizable content
- Embed logos into QR codes
- Apply AI-generated styles to QR codes using ZeroGPU
- Adjustable parameters for logo size, style strength, and more
- Web-based interface using Gradio

## Requirements

- Python 3.7+
- Gradio
- Pillow
- qrcode
- requests
- python-dotenv

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-styled-qr-generator.git
   cd ai-styled-qr-generator
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, set up the necessary configuration:

1. Environment Variables:
   Create a `.env` file in the root directory of the project with the following content:
   ```
   ZEROGPU_API_KEY=your_api_key_here
   ZEROGPU_API_URL=https://api.zerogpu.com/generate
   ```
   Replace `your_api_key_here` with your actual ZeroGPU API key.

2. Hugging Face Spaces Configuration:
   The configuration at the top of this README is used by Hugging Face Spaces. Ensure it's updated with your specific details:
   - `title`: The name of your Hugging Face Space
   - `emoji`: An emoji representing your project
   - `colorFrom` and `colorTo`: Colors for the Space's gradient
   - `sdk`: Should be set to "gradio"
   - `sdk_version`: The version of Gradio you're using (update if necessary)
   - `app_file`: The main Python file of your application (typically "app.py")

3. Model Configuration:
   The application uses specific models for QR code styling. These are currently set in the code:
   - ControlNet Model: "monster-labs/control_v1p_sd15_qrcode_monster"
   - Base Model: "SG161222/Realistic_Vision_V5.1_noVAE"

   If you need to change these, modify the `style_qr_code_zerogpu` function in `app.py`.

4. Gradio Interface Configuration:
   The Gradio interface settings (such as slider ranges) are defined in the `demo` block in `app.py`. Adjust these if you need to change the UI parameters.

5. QR Code Generation Settings:
   Basic QR code generation settings (like error correction level) are set in the `create_qr_with_logo` function. Modify these if you need different QR code characteristics.

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and go to the URL displayed in the console (typically http://127.0.0.1:7860)

3. Use the web interface to:
   - Enter the content for your QR code
   - Upload a logo (optional)
   - Adjust the logo size
   - Enter a style prompt for AI-generated styling
   - Adjust guidance scale and ControlNet conditioning scale
   - Click "Generate Styled QR Code" to create your custom QR code

## How It Works

1. The application generates a QR code with the given content and embeds the logo if provided.
2. The QR code image is sent to the ZeroGPU API along with the style prompt and other parameters.
3. ZeroGPU processes the image using AI models to apply the requested style while maintaining QR code functionality.
4. The styled QR code is returned and displayed in the web interface.

## Customization

You can customize various aspects of the application:

1. QR Code Appearance:
   - Modify the `create_qr_with_logo` function to change basic QR code appearance (colors, shape of modules, etc.)

2. AI Styling Parameters:
   - Adjust the payload sent to ZeroGPU API in the `style_qr_code_zerogpu` function to change default values or add new parameters.

3. User Interface:
   - Modify the Gradio interface in the `demo` block to add new input fields or change the layout.

## Limitations

- The application requires an internet connection to use the ZeroGPU API.
- Processing time may vary depending on ZeroGPU's server load and your internet connection.
- There may be usage limits based on your ZeroGPU account type.
- The quality and consistency of AI-generated styles can vary based on the input prompt and the underlying models.

## Troubleshooting

- If you encounter a "Module not found" error, ensure all required packages are installed.
- If you get an API error, check that your ZeroGPU API key is correctly set in the `.env` file.
- For persistent issues, check your internet connection or ZeroGPU's status page.
- If you're experiencing unexpected results in QR code styling, check the `controlnet_model` and `base_model` parameters in the `style_qr_code_zerogpu` function to ensure they're set to the desired models.
- Ensure that the QR code content is not too complex, as this can affect the ability to apply styles while maintaining scannability.

## Performance Optimization

- Consider implementing caching for frequently generated QR codes to reduce API calls and improve response times.
- For high-traffic scenarios, implement a queuing system to manage API requests efficiently.

## Security Considerations

- Never expose your ZeroGPU API key in client-side code or public repositories.
- Implement input validation to prevent potential security issues with user-provided content.
- Consider implementing rate limiting to prevent abuse of the system.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to ZeroGPU for providing the API for AI-powered image styling.
- The QR code generation is based on the `qrcode` library.
- UI is created using Gradio.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers directly.
