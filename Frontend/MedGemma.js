const API_URL = 'http://localhost:8080/chat';

const imageButton = document.getElementById('imageButton');
const inputImage = document.getElementById('inputImage');
const imagePreview = document.getElementById('imagePreview');
const inputPrompt = document.getElementById('inputPrompt');
const sendButton = document.getElementById('sendButton');

let selectedImages = [];

sendButton.disabled = true; 
inputPrompt.focus();

inputPrompt.addEventListener('input', () => {
    sendButton.disabled = inputPrompt.value.trim() === '' 
});

inputPrompt.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

imageButton.addEventListener('click', () => {
    inputImage.click();
});

inputImage.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (event) => {
            // Replace existing image with new one
            selectedImages = [{
                file: file,
                dataUrl: event.target.result
            }];
            updateImagePreview();
        };
        reader.readAsDataURL(file);
    }
    inputImage.value = ''; // Reset input
});

 sendButton.addEventListener('click', sendMessage);

 inputPrompt.addEventListener('keydown', (e) => {
     if (e.key === 'Enter' && !e.shiftKey) {
         e.preventDefault();
         sendMessage();
     }
 });

 
function updateImagePreview() {
    imagePreview.innerHTML = '';
    if (selectedImages.length > 0) {
        const img = selectedImages[0];
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';
        previewItem.innerHTML = `
            <img src="${img.dataUrl}" class="preview-image" alt="Preview">
            <button class="remove-preview" onclick="removeImage()">×</button>
        `;
        imagePreview.appendChild(previewItem);
    }
}

window.removeImage = function() {
    selectedImages = [];
    updateImagePreview();
};

function addMessage(text, isUser) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = text;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addLoadingMessage() {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'loadingMessage';
    messageDiv.innerHTML = '<div class="loading"></div>';
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeLoadingMessage() {
    const loadingMsg = document.getElementById('loadingMessage');
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

async function sendMessage() {
    const prompt = inputPrompt.value.trim();

    if (!prompt) return

    inputPrompt.disabled = true;
    
    addMessage(prompt, true);
    inputPrompt.value = '';

    addLoadingMessage();

    const formData = new FormData();
    formData.append('prompt', prompt);
    if (selectedImages.length> 0) {
        formData.append('file',  selectedImages[0].file);
    }
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        removeLoadingMessage();
        addMessage(data.response, false);

    } catch (error) {
        removeLoadingMessage();
        addMessage(`Error: ${error.message}. Please check if the API server is running.`, false);
    } finally {
        inputPrompt.disabled = false;
        removeImage(); 
        inputPrompt.focus();
    }
}