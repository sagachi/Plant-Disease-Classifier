# Plant Disease Classifier

An AI-powered web application that identifies plant diseases from leaf images using deep learning. Upload a photo of your plant leaf, and receive instant diagnosis with detailed treatment recommendations.

## Features

- **Instant Disease Detection**: Upload plant images and get results in seconds
- **38 Disease Classifications**: Trained on a comprehensive dataset of common plant diseases
- **Treatment Recommendations**: Get actionable advice for each detected disease
- **Smart Filtering**: Automatically detects if the uploaded image is actually a plant
- **Confidence Scoring**: View the model's confidence level for each prediction
- **User-Friendly Interface**: Clean, intuitive design with drag-and-drop support
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Demo

### Upload Page
Upload a clear image of a plant leaf showing disease symptoms.

### Results Page
Get instant diagnosis with disease name, severity level, confidence score, and treatment recommendations.

## Technology Stack

### Frontend
- **React** - UI framework
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### Backend
- **Flask** - Python web framework
- **TensorFlow/Keras** - Deep learning model
- **PIL (Pillow)** - Image processing
- **MobileNetV2** - Pre-classifier for plant detection

### Machine Learning
- **CNN Architecture** - Custom Convolutional Neural Network
- **Training Dataset** - 70,000+ images from New Plant Diseases Dataset
- **Input Size** - 150x150 pixels
- **Output Classes** - 38 different plant diseases

## Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Step 1: Clone the Repository
```bash
git clone https://github.com/sagachi/Plant-Disease-Classifier.git
cd Plant-Disease-Classifier
```

### Step 2: Backend Setup

Navigate to the backend folder and install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

**Required Python packages:**
- Flask
- flask-cors
- TensorFlow
- NumPy
- Pillow

### Step 3: Frontend Setup

Open a new terminal, navigate to the project root, and install Node dependencies:
```bash
npm install
```

## Usage

### Step 1: Start the Backend Server

In the first terminal, from the `backend` folder:
```bash
python app.py
```

The Flask server will start on `http://localhost:5000`

You should see:
```
Starting Plant Disease Classifier API...
Loading models...
 * Running on http://127.0.0.1:5000
```

### Step 2: Start the Frontend

In a second terminal, from the project root:
```bash
npm start
```

The React app will start on `http://localhost:3000` and automatically open in your browser.

### Step 3: Use the Application

1. **Upload Image**: Click or drag-and-drop a plant leaf image
2. **Analyze**: Click the "Analyze Plant" button
3. **View Results**: See the disease classification, confidence score, and treatment recommendations

## Supported Plants & Diseases

### Plants Supported (15 types)
- Apple
- Blueberry
- Cherry
- Corn (Maize)
- Grape
- Orange
- Peach
- Pepper (Bell)
- Potato
- Raspberry
- Soybean
- Squash
- Strawberry
- Tomato

### Diseases Detected (38 classes)

**Apple**: Apple Scab, Black Rot, Cedar Apple Rust, Healthy

**Cherry**: Powdery Mildew, Healthy

**Corn**: Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy

**Grape**: Black Rot, Esca (Black Measles), Leaf Blight, Healthy

**Peach**: Bacterial Spot, Healthy

**Pepper**: Bacterial Spot, Healthy

**Potato**: Early Blight, Late Blight, Healthy

**Tomato**: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy

**Other**: Blueberry Healthy, Orange Huanglongbing, Raspberry Healthy, Soybean Healthy, Squash Powdery Mildew, Strawberry Leaf Scorch, Strawberry Healthy

## Model Performance

- **Training Accuracy**: ~95%
- **Validation Accuracy**: ~94%
- **Test Accuracy**: ~93%
- **Total Parameters**: 2.5M+
- **Training Dataset**: New Plant Diseases Dataset (Augmented)
- **Training Images**: 70,000+
- **Validation Split**: 20%

### Model Architecture
```
Input (150x150x3)
    ↓
Conv2D (32) + ReLU → MaxPooling
    ↓
Conv2D (32) + ReLU → MaxPooling
    ↓
Conv2D (64) + ReLU → MaxPooling
    ↓
Conv2D (128) + ReLU → MaxPooling
    ↓
Conv2D (256) + ReLU → MaxPooling
    ↓
Conv2D (512) + ReLU → MaxPooling
    ↓
Flatten → Dense (512) + Dropout (0.5)
    ↓
Dense (38) + Softmax
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Saul Galarza**
- GitHub: [@sagachi](https://github.com/sagachi)

## Disclaimer

This application is for educational and informational purposes only. The AI model provides automated analysis and should not replace professional diagnosis from agricultural experts or plant pathologists. For serious plant health concerns, please consult with local agricultural extension offices or certified plant disease specialists.
# PDC-Backend
