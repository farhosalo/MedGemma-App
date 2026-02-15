# 🩺 MedGemma Medical Assistant

A FastAPI web application for medical image and text analysis using Google's MedGemma model (for educational purposes only).

## ⚠️ Important Disclaimers

### Medical Disclaimer

This application is intended solely for educational purposes and is not a medical device. Please refrain from using it for any actual medical diagnosis. Always seek guidance from healthcare professionals.

### Model License

This application utilizes MedGemma 1.5-4B, which is governed by Google’s Gemma Terms of Use. The model weights are not included and must be downloaded separately.

### Technical disclaimer

- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.  
- This is not a medical device and should not be used for medical diagnosis.
- This repository exclusively contains original source code.
- Pretrained model weights are downloaded directly from official sources.
- Users are responsible for ensuring that they comply with the license terms when using third-party models.

## Installation

- Clone the repository:

```bash
   git clone https://github.com/farhosalo/MedGemma-App.git
   cd medgemma-app
```

- Install dependencies:

```bash
   pip install -r requirements.txt
```

- Download MedGemma model (required):

```bash
   # You must accept the license at https://huggingface.co/google/medgemma-1.5-4b-it
   # Replace „your_hf_token“ with your actual HuggingFace token.

   hf download google/medgemma-1.5-4b-it --local-dir ./medgemma-1.5-4b-it --token your_hf_token  
```

- Update model path in `Configuration.py`

## Run the application

- Start the backend

```bash
   python Server.py
```

- Open the chat UI: Double click on MedGemmaUI.html

## Usage

TBD

## Contributing

Contributions are welcome! If you find any bugs or have ideas for new features, feel free to open an issue or submit a pull request.

## License

- **Project**: This project is licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](LICENSE) file for details.
- **Third-Party Libraries and Licenses**: This project uses several third-party libraries. See [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES.md) for a complete list of dependencies and their licenses.
- **MedGemma Model**: Gemma Terms of Use (<https://ai.google.dev/gemma/terms>)
- **Users must obtain model weights separately from Google/HuggingFace**

## Attribution

This application uses:

- MedGemma 1.5-4B by Google
- FastAPI
- PyTorch
- Hugging Face Transformers
