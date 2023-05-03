const imageSelector = document.getElementById('image-selector');
const imageUpload = document.getElementById('image-upload');
const imagePreview = document.getElementById('image-preview');
const sendButton = document.getElementById('send-button');
const responseLabel = document.getElementById('response-label');

let selectedImage = null;

imageSelector.addEventListener('change', () => {
  const imagePath = imageSelector.value;
  if (imagePath) {
    selectedImage = imagePath;
    imagePreview.innerHTML = `<img src="${imagePath}">`;
  }
});

imageUpload.addEventListener('change', () => {
  const file = imageUpload.files[0];
  if (file) {
    const reader = new FileReader();
    reader.addEventListener('load', () => {
      selectedImage = reader.result;
      imagePreview.innerHTML = `<img src="${selectedImage}">`;
    });
    reader.readAsDataURL(file);
  }
});

sendButton.addEventListener('click', async () => {
  if (selectedImage) {
    const data = {
      image: selectedImage
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });

      const prediction = await response.text();
      responseLabel.textContent = prediction;
    } catch (error) {
      console.error(error);
    }
  } else {
    alert('Please select an image first.');
  }
});
