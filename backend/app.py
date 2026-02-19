from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow import keras
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

app = Flask(__name__)
CORS(app)

# Load disease classification model
model = keras.models.load_model('model/plant_disease_model.h5')

# Load ImageNet model for plant detection
imagenet_model = MobileNetV2(weights='imagenet')

# Disease classes
CLASS_LABELS = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Blueberry___healthy',
    'Cherry_(including_sour)___Powdery_mildew',
    'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot',
    'Peach___healthy',
    'Pepper,_bell___Bacterial_spot',
    'Pepper,_bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Raspberry___healthy',
    'Soybean___healthy',
    'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch',
    'Strawberry___healthy',
    'Tomato___Bacterial_spot',
    'Tomato___Early_blight',
    'Tomato___Late_blight',
    'Tomato___Leaf_Mold',
    'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
    'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# Treatment recommendations
TREATMENTS = {
    'Apple___Apple_scab': 'Remove and destroy infected leaves. Apply fungicide sprays. Ensure proper air circulation.',
    'Apple___Black_rot': 'Prune infected branches. Remove mummified fruits. Apply fungicide during growing season.',
    'Apple___Cedar_apple_rust': 'Remove nearby cedar trees if possible. Apply fungicide in spring. Plant resistant varieties.',
    'Apple___healthy': 'No treatment needed. Continue regular care and monitoring.',
    'Blueberry___healthy': 'No treatment needed. Maintain proper watering and fertilization.',
    'Cherry_(including_sour)___Powdery_mildew': 'Apply fungicide. Improve air circulation. Remove infected parts.',
    'Cherry_(including_sour)___healthy': 'No treatment needed. Continue regular maintenance.',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Rotate crops. Use resistant varieties. Apply fungicide if severe.',
    'Corn_(maize)___Common_rust_': 'Plant resistant hybrids. Apply fungicide if infection is severe.',
    'Corn_(maize)___Northern_Leaf_Blight': 'Use resistant hybrids. Rotate crops. Remove infected debris.',
    'Corn_(maize)___healthy': 'No treatment needed. Maintain good agricultural practices.',
    'Grape___Black_rot': 'Remove infected fruit and leaves. Apply fungicide. Improve air circulation.',
    'Grape___Esca_(Black_Measles)': 'Prune infected wood. No chemical treatment available. Focus on prevention.',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Remove infected leaves. Apply copper-based fungicide.',
    'Grape___healthy': 'No treatment needed. Continue regular vineyard management.',
    'Orange___Haunglongbing_(Citrus_greening)': 'Remove infected trees. Control psyllid insects. Use disease-free plants.',
    'Peach___Bacterial_spot': 'Apply copper sprays. Plant resistant varieties. Improve air circulation.',
    'Peach___healthy': 'No treatment needed. Maintain regular pruning and care.',
    'Pepper,_bell___Bacterial_spot': 'Use disease-free seeds. Apply copper-based bactericide. Avoid overhead watering.',
    'Pepper,_bell___healthy': 'No treatment needed. Continue proper watering and fertilization.',
    'Potato___Early_blight': 'Remove infected leaves. Apply fungicide. Practice crop rotation.',
    'Potato___Late_blight': 'Apply fungicide immediately. Remove infected plants. Improve drainage.',
    'Potato___healthy': 'No treatment needed. Monitor regularly for signs of disease.',
    'Raspberry___healthy': 'No treatment needed. Maintain proper spacing and pruning.',
    'Soybean___healthy': 'No treatment needed. Continue good agricultural practices.',
    'Squash___Powdery_mildew': 'Apply fungicide. Improve air circulation. Water at soil level.',
    'Strawberry___Leaf_scorch': 'Remove infected leaves. Improve air circulation. Apply fungicide if needed.',
    'Strawberry___healthy': 'No treatment needed. Maintain proper spacing and watering.',
    'Tomato___Bacterial_spot': 'Use disease-free seeds. Apply copper sprays. Avoid overhead watering.',
    'Tomato___Early_blight': 'Remove infected leaves. Apply fungicide. Mulch around plants.',
    'Tomato___Late_blight': 'Apply fungicide immediately. Remove severely infected plants. Improve air circulation.',
    'Tomato___Leaf_Mold': 'Improve air circulation. Reduce humidity. Apply fungicide if severe.',
    'Tomato___Septoria_leaf_spot': 'Remove infected leaves. Apply fungicide. Mulch to prevent splash.',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Spray with water. Use insecticidal soap. Encourage natural predators.',
    'Tomato___Target_Spot': 'Remove infected leaves. Apply fungicide. Practice crop rotation.',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Remove infected plants. Control whiteflies. Use virus-resistant varieties.',
    'Tomato___Tomato_mosaic_virus': 'Remove infected plants. Disinfect tools. Use virus-free seeds.',
    'Tomato___healthy': 'No treatment needed. Continue proper watering and fertilization.'
}

def is_plant_image(img):
    """Check if image contains plant-related content using ImageNet classifier"""
    # Resize for ImageNet (224x224)
    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    # Get predictions
    preds = imagenet_model.predict(img_array, verbose=0)
    decoded = decode_predictions(preds, top=10)[0]
    
    # Expanded plant-related ImageNet classes and keywords
    plant_keywords = [
        'leaf', 'plant', 'vegetable', 'fruit', 'flower', 'tree', 'vine',
        'corn', 'grape', 'orange', 'strawberry', 'mushroom', 'broccoli',
        'cauliflower', 'cucumber', 'pepper', 'squash', 'pomegranate',
        'cabbage', 'artichoke', 'cardoon', 'bell_pepper', 'zucchini',
        'acorn', 'ear', 'lemon', 'pineapple', 'banana', 'apple',
        'cherry', 'tomato', 'potato', 'head_cabbage', 'butternut_squash',
        'spaghetti_squash', 'cucumber', 'green', 'botanical'
    ]
    
    # Check if any top prediction is plant-related
    max_plant_confidence = 0
    best_match = decoded[0]
    
    for _, label, prob in decoded:
        label_lower = label.lower().replace('_', ' ')
        for keyword in plant_keywords:
            if keyword in label_lower:
                if prob > max_plant_confidence:
                    max_plant_confidence = prob
                    best_match = (_, label, prob)
                # If we find a strong plant match, return True
                if prob > 0.1:
                    return True, label, prob
    
    # If we found any plant-related prediction, even weak, accept it
    if max_plant_confidence > 0.05:
        return True, best_match[1], best_match[2]
    
    return False, decoded[0][1], decoded[0][2]

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        file = request.files['image']
        
        # Read image
        img = Image.open(io.BytesIO(file.read()))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Check if it's a plant first using ImageNet
        is_plant, top_class, confidence_check = is_plant_image(img)
        
        if not is_plant:
            return jsonify({
                'disease': 'Not a Plant',
                'severity': 'N/A',
                'treatment': f'This image appears to be "{top_class}" with {confidence_check*100:.1f}% confidence. Please upload an image of a plant leaf showing any disease symptoms.',
                'confidence': 0,
                'isPlant': False
            })
        
        # Resize to 150x150 for your disease model
        img_150 = img.resize((150, 150))
        
        # Convert to array and normalize (divide by 255)
        img_array = np.array(img_150) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Make prediction with your disease model
        predictions = model.predict(img_array, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class]) * 100
        
        # Get disease name
        disease = CLASS_LABELS[predicted_class]
        
        # Format disease name for display
        disease_display = disease.replace('___', ' - ').replace('_', ' ')
        
        # Determine severity based on confidence
        if confidence > 85:
            severity = "High Confidence"
        elif confidence > 70:
            severity = "Moderate Confidence"
        else:
            severity = "Low Confidence"
        
        # Get treatment
        treatment = TREATMENTS.get(disease, 'Consult a plant specialist for treatment options.')
        
        return jsonify({
            'disease': disease_display,
            'severity': severity,
            'treatment': treatment,
            'confidence': round(confidence, 2),
            'isPlant': True
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Starting Plant Disease Classifier API...")
    print("Loading models...")
    app.run(debug=True, port=5000)