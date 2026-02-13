from fastapi import FastAPI, UploadFile, Form
from starlette.middleware.cors import CORSMiddleware
import logging

app = FastAPI(title="MedGemma API", version="1.0")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
# async def chat(prompt: str = Form(...), image: UploadFile = None):
async def chat(prompt: str = Form(...), file: UploadFile = None):
    logging.info("\n--- New Request ---")
    size = 0
    fileName = ""
    if file:
        fileName = file.filename
        size = len(await file.read())
        logging.info(f"Received file: {fileName}")
        logging.info(f"Content type: {file.content_type}")
        logging.info(f"file size: {size} bytes")

    logging.info(f"Received text: {prompt}")

    return {
        "response": "Your  message: "
        + prompt
        + ", file name: "
        + fileName
        + ", size: "
        + str(size)
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
