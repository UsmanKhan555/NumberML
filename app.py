from flask import Flask, request, render_template, jsonify
import torch
import torch.nn as nn
from torchvision import transforms
import torchvision.transforms as transforms
from PIL import Image

# Load the trained model
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 10, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
            nn.Conv2d(10, 20, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(320, 50),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(50, 10)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SimpleNN()
model.load_state_dict(torch.load("mnist_model.pth", map_location=device))
model.to(device)
model.eval()

# Define image preprocessing
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
# Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render the upload form

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Process the uploaded image
    try:
        img = Image.open(file).convert('L')  # Convert to grayscale
        img = transform(img).unsqueeze(0).to(device)  # Apply transforms
        with torch.no_grad():
            output = model(img)
            predicted = torch.argmax(output, dim=1).item()
        return jsonify({"digit": predicted})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
