from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from models.ml_model import MLModel
from report_generator import generate_report
from config import Config
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize ML model
ml_model = MLModel()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Run ML model prediction
        diagnosis = ml_model.predict(filepath)
        
        # Generate report
        report = generate_report(diagnosis)
        
        return jsonify({
            'filename': filename,
            'diagnosis': diagnosis,
            'report': report
        }), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
