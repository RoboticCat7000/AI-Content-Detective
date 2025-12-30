let mode = "text";

const form = document.getElementById("form");
const textButton = document.getElementById("text");
const imageButton = document.getElementById("image");
const videoButton = document.getElementById("video");
const results = document.getElementById("results");

// Helper to highlight the selected button
function setActiveTab(activeBtn) {
  [textButton, imageButton, videoButton].forEach((btn) =>
    btn.classList.remove("active")
  );
  activeBtn.classList.add("active");
  results.style.display = "none";
  results.textContent = "";
}

function displayResult(data) {
  if (data.error) {
    results.innerHTML = `<div style="color: red; font-weight: bold;">Error: ${data.error}</div>`;
    return;
  }
  console.log(data);
  // Dynamic Color: Red for AI, Green for Real
  const isAI = data.output.verdict.includes("AI");
  const colorClass = isAI ? "#e74c3c" : "#27ae60"; // Red vs Green

  results.style.borderLeft = `5px solid ${colorClass}`;
  results.style.display = "block";

  results.innerHTML = `
        <h2 style="color: ${colorClass}; margin-top: 0;">${data.output.verdict}</h2>
        <p><strong>Percentage:</strong> ${data.output.confidence}</p>
        <hr style="border: 0; border-top: 1px solid #ddd; margin: 15px 0;">
        <p><strong>AI Content Detective:</strong> "${data.output.mentor_response}"</p>
        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px;">
            <strong> Recommendation:</strong> ${data.output.recommendation}
        </div>
    `;
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const input = document.getElementById("input");

  // Show loading
  results.style.display = "block";
  results.textContent = "Analyzing...";

  if (mode == "text") {
    const text = input.value;
    const formData = new FormData();
    formData.append("text", text);

    fetch("http://127.0.0.1:5000/text", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        displayResult(data);
      })
      .catch((error) => {
        console.error("Error:", error);
        results.textContent = "Error: " + error;
      });
  }

  if (mode == "image") {
    const image = input.files[0];
    const formData = new FormData();

    formData.append("file", image);

    fetch("http://127.0.0.1:5000/image", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        displayResult(data);
      })
      .catch((error) => {
        console.log("Error:", error);
        results.textContent = "Error: " + error;
      });
  }

  if (mode == "video") {
    const video = input.files[0];
    const formData = new FormData();
    formData.append("file", video);

    fetch("http://127.0.0.1:5000/video", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        displayResult(data);
      })
      .catch((error) => {
        console.log("Error:", error);
        results.textContent = "Error: " + error;
      });
  }
});

textButton.addEventListener("click", () => {
  mode = "text";
  setActiveTab(textButton);
  form.innerHTML = `
    <label for="input">Enter text:</label>
    <textarea id="input" name="input" rows="6" placeholder="Paste text here..."></textarea>
    <button type="submit">Analyze Text</button>
  `;
});

imageButton.addEventListener("click", () => {
  mode = "image";
  setActiveTab(imageButton);
  form.innerHTML = `
    <label for="input">Upload Image:</label>
    <input id="input" type="file" accept=".png,.jpg,.jpeg"/>
    <button type="submit">Submit</button>
  `;
});

videoButton.addEventListener("click", () => {
  mode = "video";
  setActiveTab(videoButton);
  form.innerHTML = `
    <label for="input">Upload Video:</label>
    <input id="input" type="file" accept=".mp4"/>
    <button type="submit">Submit</button>
  `;
});
["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  form.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

["dragenter", "dragover"].forEach((eventName) => {
  form.addEventListener(eventName, highlight, false);
});

["dragleave", "drop"].forEach((eventName) => {
  form.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
  form.classList.add("drag-active");
}

function unhighlight(e) {
  form.classList.remove("drag-active");
}

form.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;
  const fileInput = document.getElementById("input");

  if (files.length > 1) {
    alert("Please drop only one file at a time!");
    return;
  }

  if ((mode === "image" || mode === "video") && fileInput) {
    fileInput.files = files;

    const label = document.querySelector("label[for='input']");
    if (label) label.textContent = `File Selected: ${files[0].name}`;
  }
}
