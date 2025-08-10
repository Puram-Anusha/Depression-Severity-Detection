function uploadImage() {
  const imageInput = document.getElementById('imageInput');
  const resultText = document.getElementById('result');
  const descriptionText = document.getElementById('description');
  const preview = document.getElementById('preview');

  if (!imageInput.files[0]) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("image", imageInput.files[0]);

  // Show preview
  const reader = new FileReader();
  reader.onload = function (e) {
    preview.src = e.target.result;
    preview.style.display = "block";
  };
  reader.readAsDataURL(imageInput.files[0]);

  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    resultText.innerText = `Result: ${data.result}`;
    descriptionText.innerText = data.details || "";
  })
  .catch(err => {
    resultText.innerText = "Error: Could not connect to server.";
    console.error(err);
  });
}
