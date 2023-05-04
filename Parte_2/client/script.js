// const imageSelector = document.getElementById('image-selector');
const imageUpload = document.getElementById('image-upload');
const imagePreview = document.getElementById('image-preview');
const sendButton = document.getElementById('send-button');
const responseLabel = document.getElementById('response-label');

let selectedImage = null;

// imageSelector.addEventListener('change', () => {
//   const imagePath = imageSelector.value;
//   if (imagePath) {
//     let reader = new FileReader();
//     reader.addEventListener('load', () => {
//       selectedImage = reader.result;
//     });
//     reader.readAsDataURL(imageSelector.files[0]);
//   }
// });

imageUpload.addEventListener('change', () => {
  const file = imageUpload.files[0];
  if (file) {
    selectedImage = file;
    let reader = new FileReader();
    reader.addEventListener('load', () => {
      imagePreview.innerHTML = `<img src="${reader.result}">`;
    });
    reader.readAsDataURL(file);
  }
});

sendButton.addEventListener('click', async () => {
  if (selectedImage) {
    const response = await sendImage(selectedImage);
    const prediction = response.Prediction;
    console.log(prediction);
    // Parse the response
    if (prediction == 0) {
      responseLabel.textContent = "Acoustic";
    }
    if (prediction == 1) {
      responseLabel.textContent = "Double Cut";
    }
    if (prediction == 2) {
      responseLabel.textContent = "Single Cut";
    }
    if (prediction == 3) {
      responseLabel.textContent = "S Style";
    }
    if (prediction == 4) {
      responseLabel.textContent = "T Style";
    }
    if (prediction == 5) {
      responseLabel.textContent = "Ukulele";
    }

    // responseLabel.textContent = `Prediction: ${prediction}`;
  } else {
    alert('Please select an image');
  }
});

async function sendImage(image) {
  const formData = new FormData();
  formData.append('img', image);

  const response = await fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const json = await response.json();
  return json;
}
