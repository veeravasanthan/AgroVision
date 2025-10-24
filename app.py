from flask import Flask, render_template, request
import pickle
import numpy as np
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
# Complete crop information database
CROP_INFO = {
    'Rice': {
        'season': 'Kharif (June-September)',
        'soil': 'Clayey loam with good water retention',
        'temperature': '20-35°C',
        'rainfall': '150-300 cm',
        'ph': '5.0-7.5',
        'insights': [
            'Requires standing water during growth period',
            'High nitrogen requirement for optimal yield',
            'Suitable for areas with good irrigation facilities',
            'Harvest in 3-6 months depending on variety'
        ]
    },
    'Maize': {
        'season': 'Kharif (June-September)',
        'soil': 'Well-drained sandy loam',
        'temperature': '18-27°C',
        'rainfall': '60-110 cm',
        'ph': '5.5-7.5',
        'insights': [
            'Responds well to nitrogen fertilizers',
            'Requires warm weather and frost-free period',
            'Sensitive to waterlogging',
            'Harvest in 80-110 days'
        ]
    },
    'Chickpea': {
        'season': 'Rabi (October-March)',
        'soil': 'Well-drained sandy loam to clay loam',
        'temperature': '15-25°C',
        'rainfall': '60-90 cm',
        'ph': '6.0-8.0',
        'insights': [
            'Drought-resistant crop',
            'Fixes atmospheric nitrogen',
            'Suitable for rainfed conditions',
            'Harvest in 90-120 days'
        ]
    },
    'Kidneybeans': {
        'season': 'Rabi (October-March)',
        'soil': 'Well-drained loamy soil',
        'temperature': '15-25°C',
        'rainfall': '60-120 cm',
        'ph': '6.0-7.5',
        'insights': [
            'Requires moderate temperature',
            'Sensitive to waterlogging',
            'Needs well-drained soil',
            'Harvest in 90-120 days'
        ]
    },
    'Pigeonpeas': {
        'season': 'Kharif (June-September)',
        'soil': 'Well-drained sandy loam',
        'temperature': '20-30°C',
        'rainfall': '60-140 cm',
        'ph': '6.0-7.5',
        'insights': [
            'Drought-tolerant crop',
            'Deep root system',
            'Grows well in marginal soils',
            'Harvest in 120-180 days'
        ]
    },
    'Mothbeans': {
        'season': 'Kharif (June-September)',
        'soil': 'Sandy loam to clay loam',
        'temperature': '25-35°C',
        'rainfall': '50-75 cm',
        'ph': '6.5-7.5',
        'insights': [
            'Drought-resistant',
            'Short duration crop',
            'Suitable for arid regions',
            'Harvest in 60-90 days'
        ]
    },
    'Mungbean': {
        'season': 'Kharif (June-September)',
        'soil': 'Well-drained sandy loam',
        'temperature': '25-35°C',
        'rainfall': '60-90 cm',
        'ph': '6.2-7.2',
        'insights': [
            'Short duration crop',
            'Drought tolerant',
            'Improves soil fertility',
            'Harvest in 60-75 days'
        ]
    },
    'Blackgram': {
        'season': 'Kharif (June-September)',
        'soil': 'Well-drained loamy soil',
        'temperature': '25-35°C',
        'rainfall': '60-75 cm',
        'ph': '6.5-7.5',
        'insights': [
            'Short duration pulse crop',
            'Improves soil fertility',
            'Drought resistant',
            'Harvest in 80-90 days'
        ]
    },
    'Lentil': {
        'season': 'Rabi (October-March)',
        'soil': 'Well-drained loamy soil',
        'temperature': '15-25°C',
        'rainfall': '40-50 cm',
        'ph': '6.0-7.5',
        'insights': [
            'Cool season crop',
            'Drought tolerant',
            'Improves soil nitrogen',
            'Harvest in 100-110 days'
        ]
    },
    'Pomegranate': {
        'season': 'Perennial',
        'soil': 'Well-drained loamy soil',
        'temperature': '25-35°C',
        'rainfall': '50-75 cm',
        'ph': '5.5-7.0',
        'insights': [
            'Drought resistant fruit tree',
            'Requires hot, dry climate',
            'Long-lived perennial',
            'Fruits in 2-3 years'
        ]
    },
    'Banana': {
        'season': 'Perennial',
        'soil': 'Deep, well-drained loamy soil',
        'temperature': '20-35°C',
        'rainfall': '150-200 cm',
        'ph': '6.0-7.5',
        'insights': [
            'Requires high humidity',
            'Needs good drainage',
            'High water requirement',
            'Harvest in 12-15 months'
        ]
    },
    'Mango': {
        'season': 'Perennial',
        'soil': 'Deep, well-drained loamy soil',
        'temperature': '24-30°C',
        'rainfall': '75-250 cm',
        'ph': '5.5-7.5',
        'insights': [
            'Tropical fruit tree',
            'Sensitive to frost',
            'Long-lived tree',
            'Fruits in 4-6 years'
        ]
    },
    'Grapes': {
        'season': 'Perennial',
        'soil': 'Well-drained sandy loam',
        'temperature': '15-35°C',
        'rainfall': '50-150 cm',
        'ph': '6.5-7.5',
        'insights': [
            'Requires pruning',
            'Needs support system',
            'Drought tolerant once established',
            'Fruits in 2-3 years'
        ]
    },
    'Watermelon': {
        'season': 'Summer (March-June)',
        'soil': 'Sandy loam with good drainage',
        'temperature': '25-35°C',
        'rainfall': '50-75 cm',
        'ph': '6.0-7.0',
        'insights': [
            'Requires warm temperature',
            'Needs plenty of space',
            'Drought sensitive',
            'Harvest in 80-100 days'
        ]
    },
    'Muskmelon': {
        'season': 'Summer (March-June)',
        'soil': 'Well-drained sandy loam',
        'temperature': '25-35°C',
        'rainfall': '50-75 cm',
        'ph': '6.0-7.0',
        'insights': [
            'Warm season crop',
            'Requires good drainage',
            'Sensitive to frost',
            'Harvest in 70-90 days'
        ]
    },
    'Apple': {
        'season': 'Perennial',
        'soil': 'Well-drained loamy soil',
        'temperature': '15-25°C',
        'rainfall': '100-125 cm',
        'ph': '6.0-6.5',
        'insights': [
            'Requires chilling hours',
            'Temperate fruit tree',
            'Needs cross-pollination',
            'Fruits in 4-5 years'
        ]
    },
    'Orange': {
        'season': 'Perennial',
        'soil': 'Deep, well-drained loamy soil',
        'temperature': '20-30°C',
        'rainfall': '100-120 cm',
        'ph': '6.0-7.5',
        'insights': [
            'Subtropical fruit tree',
            'Sensitive to frost',
            'Requires regular pruning',
            'Fruits in 3-4 years'
        ]
    },
    'Papaya': {
        'season': 'Perennial',
        'soil': 'Well-drained sandy loam',
        'temperature': '25-30°C',
        'rainfall': '150-200 cm',
        'ph': '6.0-6.5',
        'insights': [
            'Fast-growing tropical tree',
            'Sensitive to waterlogging',
            'Short-lived perennial',
            'Fruits in 9-11 months'
        ]
    },
    'Coconut': {
        'season': 'Perennial',
        'soil': 'Sandy loam, coastal soils',
        'temperature': '27-32°C',
        'rainfall': '150-250 cm',
        'ph': '5.0-8.0',
        'insights': [
            'Coastal tropical tree',
            'Requires high humidity',
            'Salt tolerant',
            'Fruits in 6-10 years'
        ]
    },
    'Cotton': {
        'season': 'Kharif (April-September)',
        'soil': 'Black cotton soil',
        'temperature': '21-30°C',
        'rainfall': '50-100 cm',
        'ph': '6.0-8.0',
        'insights': [
            'Requires long frost-free period',
            'Sensitive to waterlogging',
            'Needs warm climate with sunshine',
            'Harvest in 150-180 days'
        ]
    },
    'Jute': {
        'season': 'Kharif (March-August)',
        'soil': 'Alluvial loamy soil',
        'temperature': '24-35°C',
        'rainfall': '150-250 cm',
        'ph': '6.0-7.5',
        'insights': [
            'Requires high rainfall',
            'Needs standing water initially',
            'Fiber crop',
            'Harvest in 120-150 days'
        ]
    },
    'Coffee': {
        'season': 'Perennial',
        'soil': 'Volcanic, well-drained soil',
        'temperature': '15-28°C',
        'rainfall': '150-250 cm',
        'ph': '6.0-6.5',
        'insights': [
            'Requires shade in early growth',
            'Sensitive to frost and strong winds',
            'Needs well-distributed rainfall',
            'First harvest in 3-4 years'
        ]
    }
}

# Updated crop label mapping - Double check this matches your model training
CROP_LABELS = {
    0: 'Rice', 1: 'Maize', 2: 'Chickpea', 3: 'Kidneybeans', 4: 'Pigeonpeas',
    5: 'Mothbeans', 6: 'Mungbean', 7: 'Blackgram', 8: 'Lentil', 9: 'Pomegranate',
    10: 'Banana', 11: 'Mango', 12: 'Grapes', 13: 'Watermelon', 14: 'Muskmelon',
    15: 'Apple', 16: 'Orange', 17: 'Papaya', 18: 'Coconut', 19: 'Cotton',
    20: 'Jute', 21: 'Coffee'
}

# Alternative label mapping (try this if above doesn't work)
CROP_LABELS_ALTERNATIVE = {
    1: 'Rice', 2: 'Maize', 3: 'Chickpea', 4: 'Kidneybeans', 5: 'Pigeonpeas',
    6: 'Mothbeans', 7: 'Mungbean', 8: 'Blackgram', 9: 'Lentil', 10: 'Pomegranate',
    11: 'Banana', 12: 'Mango', 13: 'Grapes', 14: 'Watermelon', 15: 'Muskmelon',
    16: 'Apple', 17: 'Orange', 18: 'Papaya', 19: 'Coconut', 20: 'Cotton',
    21: 'Jute', 22: 'Coffee'
}

try:
    standard_scaler = pickle.load(open('scalerstand.pkl', 'rb'))
    minmax_scaler = pickle.load(open('minmaxscaler.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
    print("✅ All models loaded successfully!")
    print(f"Model type: {type(model)}")
    
    # Test the model with sample data
    sample_input = np.array([[90, 42, 43, 20, 80, 6.5, 200]])
    sample_prediction = model.predict(sample_input)
    print(f"Sample prediction: {sample_prediction}")
    
except Exception as e:
    print(f"❌ Error loading models: {e}")
    # Create a smarter mock model that varies predictions
    class SmartMockModel:
        def __init__(self):
            self.counter = 0
            self.crops = list(CROP_LABELS.values())
        
        def predict(self, features):
            # Use input values to determine crop (simple logic)
            nitrogen = features[0][0]
            temperature = features[0][3]
            rainfall = features[0][6]
            
            # Simple logic based on inputs
            if nitrogen > 100 and rainfall > 150:
                return [0]  # Rice
            elif temperature > 25 and rainfall < 100:
                return [1]  # Maize
            elif temperature < 20:
                return [2]  # Chickpea
            elif rainfall > 200:
                return [20]  # Jute
            else:
                # Cycle through different crops
                self.counter = (self.counter + 1) % len(self.crops)
                return [self.counter]
    
    model = SmartMockModel()
    standard_scaler = None
    minmax_scaler = None
    print("⚠️ Using mock model for testing")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prediction')
def prediction_page():
    return render_template('prediction.html', crop_data=None)

@app.route('/predict', methods=['POST'])
def predict():
    crop_data = None
    
    try:
        # Get form data
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        
        # Create input array for model
        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        
        print(f"📊 Input features: {features}")
        
        # Apply scaling
        features_scaled = features
        if standard_scaler:
            try:
                features_scaled = standard_scaler.transform(features)
                print("✅ Used Standard Scaler")
            except Exception as e:
                print(f"❌ Standard scaler failed: {e}")
                features_scaled = features
        elif minmax_scaler:
            try:
                features_scaled = minmax_scaler.transform(features)
                print("✅ Used MinMax Scaler")
            except Exception as e:
                print(f"❌ MinMax scaler failed: {e}")
                features_scaled = features
        
        print(f"📊 Scaled features: {features_scaled}")
        
        # Make prediction
        prediction = model.predict(features_scaled)
        predicted_value = prediction[0]
        
        print(f"🔢 Raw prediction: {predicted_value} (type: {type(predicted_value)})")
        
        # Convert numerical prediction to crop name
        crop_name = "Unknown Crop"
        if isinstance(predicted_value, (int, float, np.integer, np.floating)):
            predicted_int = int(predicted_value)
            print(f"🔢 Predicted integer: {predicted_int}")
            
            # Try different label mappings
            if predicted_int in CROP_LABELS:
                crop_name = CROP_LABELS[predicted_int]
                print(f"✅ Found in CROP_LABELS: {crop_name}")
            elif predicted_int in CROP_LABELS_ALTERNATIVE:
                crop_name = CROP_LABELS_ALTERNATIVE[predicted_int]
                print(f"✅ Found in CROP_LABELS_ALTERNATIVE: {crop_name}")
            else:
                crop_name = f"Unknown Code: {predicted_int}"
                print(f"❌ Not found in any label mapping")
        else:
            crop_name = str(predicted_value)
            print(f"🔢 String prediction: {crop_name}")
        
        # Get crop insights
        crop_data = CROP_INFO.get(crop_name, {
            'name': crop_name,
            'season': 'Information not available',
            'soil': 'Information not available',
            'temperature': 'Information not available',
            'rainfall': 'Information not available',
            'ph': 'Information not available',
            'insights': ['Detailed growing information coming soon.']
        })
        crop_data['name'] = crop_name
        
        print(f"🌱 Final crop prediction: {crop_name}")
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        
        crop_data = {
            'name': 'Error in prediction',
            'season': 'N/A',
            'soil': 'N/A',
            'temperature': 'N/A',
            'rainfall': 'N/A',
            'ph': 'N/A',
            'insights': [f'Error: {str(e)}. Please check your input values.']
        }
    
    return render_template('prediction.html', crop_data=crop_data)

@app.route('/debug')
def debug():
    """Debug page to test different inputs"""
    test_cases = [
        [90, 42, 43, 20, 80, 6.5, 200],   # Rice conditions
        [80, 30, 40, 25, 70, 6.0, 100],   # Maize conditions  
        [40, 50, 40, 18, 60, 7.0, 80],    # Chickpea conditions
        [50, 40, 45, 30, 75, 6.8, 50],    # Cotton conditions
        [60, 35, 42, 22, 85, 6.2, 180]    # Coffee conditions
    ]
    
    results = []
    for i, test_case in enumerate(test_cases):
        features = np.array([test_case])
        if standard_scaler:
            features_scaled = standard_scaler.transform(features)
        else:
            features_scaled = features
            
        prediction = model.predict(features_scaled)
        predicted_int = int(prediction[0])
        crop_name = CROP_LABELS.get(predicted_int, f"Unknown: {predicted_int}")
        
        results.append({
            'input': test_case,
            'prediction': predicted_int,
            'crop': crop_name
        })
    
    return f"""
    <h1>Model Debug Info</h1>
    <h2>Test Predictions:</h2>
    <pre>{results}</pre>
    <h2>Label Mapping:</h2>
    <pre>{CROP_LABELS}</pre>
    <h2>Model Info:</h2>
    <pre>Type: {type(model)}</pre>
    """

if __name__ == '__main__':
       port = int(os.environ.get('PORT', 5000))
       app.run(host='0.0.0.0', port=port, debug=False)
app = app