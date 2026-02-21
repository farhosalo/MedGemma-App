import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def checkPythonVersion():
    if sys.version_info < (3, 10):
        logging.info(f"Current version is: {sys.version}")
        return False
    return True


def checkDependencies():
    try:
        import fastapi
        import uvicorn
        import starlette
        import transformers
        import logging
        import torch
        import PIL
        import io
        import markdown
        import bs4
        import Configuration
        import contextlib

        return True
    except ImportError:
        return False


def openUI(url, delay=3):
    time.sleep(delay)
    try:
        webbrowser.open(url)
    except:
        logging.error(f"💡 Please open {url} in your browser manually")


def main():
    outputSeparator = "=" * 64
    print(outputSeparator)
    print("🩺 MedGemma Medical Assistant - Launcher")
    print(outputSeparator)
    print()

    # Check Python version
    if not checkPythonVersion():
        logging.error("❌ ERROR: Python 3.10 or higher is required")
        sys.exit(1)

    # Check if app.py exists
    if not Path("Server.py").exists() or not Path("MedGemmaUi.html").exists():
        logging.error(
            "❌ ERROR: Server.py or MegGemmaUi.html not found in current directory"
        )
        sys.exit(1)

    # Check dependencies
    if not checkDependencies():
        logging.error("⚠️  Not all dependencies are installed.")
        exit(1)

    print("⚠️  This app runs LOCALLY ONLY")
    print("   (Not accessible from other devices)")
    print()
    print("Press CTRL+C to stop the server")
    print("💡 Tip: Keep this terminal open while using the app")
    print(outputSeparator)

    # Open browser in background
    from threading import Thread

    UiPath = Path("MedGemmaUi.html").absolute().as_uri()
    browser_thread = Thread(target=openUI, args=(UiPath,))
    browser_thread.daemon = True
    browser_thread.start()

    # Start the app
    try:
        subprocess.run([sys.executable, "Server.py"])
    except KeyboardInterrupt:
        logging.info("\n✅ Server stopped.")
    except Exception as e:
        logging.error(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
