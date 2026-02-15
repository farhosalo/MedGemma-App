import multiprocessing as mp
from fastapi import FastAPI, UploadFile, Form, HTTPException
from starlette.middleware.cors import CORSMiddleware
from transformers import (
    AutoProcessor,
    AutoModelForImageTextToText,
)
import logging
import torch
from PIL import Image
import io
import markdown
from bs4 import BeautifulSoup

from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def optimizeImage(imageFile, maxSize=(768, 768)):
    img = Image.open(io.BytesIO(imageFile))

    # Convert to RGB if needed
    if img.mode != "RGB":
        img = img.convert("RGB")

    # Resize if larger than max_size (maintain aspect ratio)
    img.thumbnail(maxSize, Image.LANCZOS)

    return img


# Global model and processor
model = None
processor = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, processor
    modelId = "medgemma-1.5-4b-it"

    logging.info("Loading model... This may take a minute.")
    processor = AutoProcessor.from_pretrained(modelId)
    model = AutoModelForImageTextToText.from_pretrained(
        modelId,
        dtype=torch.bfloat16,
        device_map="cpu",
    )
    model.eval()  # Set the model to evaluation mode
    logging.info("Model loaded successfully!")
    yield

    # Shutdown: Clean up resources (optional)
    logging.info("Shutting down...")
    del model
    del processor


app = FastAPI(title="MedGemma API", version="1.0", lifespan=lifespan)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(prompt: str = Form(...), file: UploadFile = None):
    hasImage = file is not None

    if hasImage:
        fileContent = await file.read()
        img = optimizeImage(fileContent, maxSize=(384, 384))

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": img},
                    {"type": "text", "text": prompt},
                ],
            }
        ]
    else:
        messages = [
            {
                "role": "user",
                "content": [
                    # {"type": "image", "image": img},
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ]

    try:
        return generateResponse(messages)
    except Exception as e:
        logging.error("An error occurred while running the server:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


def generateResponse(messages):
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    )

    input_len = inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(
            **inputs,
            max_new_tokens=500,
            do_sample=False,
        )  # .to("mps")
        generation = generation[0][input_len:]
    response_text = processor.decode(generation, skip_special_tokens=True)
    html = markdown.markdown(response_text)
    text = BeautifulSoup(html, "html.parser").get_text()

    return {"response": text}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
