from flask import Flask, request, jsonify, send_file
import os, base64 , zipfile,io
import pydicom as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:54833'],
          methods=['GET', 'POST'],
          allow_headers=['Authorization'])
# Set the maximum content length to 64MB (or any value you prefer)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 32MB
# Route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if any files are uploaded
        if 'file_0' not in request.files:
            return jsonify({'error': 'No files uploaded'})

        # Get the group ID from the form data
        group_id = request.form.get('group_id')
        study_id = request.form.get('study_id')

        for idx in range(len(request.files)):
            file_key = f'file_{idx}'
            if file_key not in request.files:
                return jsonify({'error': f'File {idx} not found'})

            file = request.files[file_key]
            if file.filename == '':
                return jsonify({'error': f'File {idx} has no name'})
            # filename = file.filename.split('.dcm')[0]
            # Save the uploaded file to the 'uploads' folder
            save_path = os.path.join('uploads', file.filename)
            file.save(save_path)

        return jsonify({'message': 'Files uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
# Route for submitting patient data
@app.route('/submit_patient_data', methods=['POST'])
def submit_patient_data():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'})
    print(data)
    # Process the received data (replace this with your data processing logic)
    return jsonify({'message': 'Patient data submitted successfully'})

# Path to the zip file containing DICOM images
zip_file_path = 'uploads/1.2.392.200036.9125.9.0.253704642.1510563065.3715502529.zip'

@app.route('/get_image', methods=['GET'])
def get_image():
    # Extract DICOM files from the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall('temp')

    # Get the list of extracted DICOM files
    dicom_files = [f for f in os.listdir('temp') if f.endswith('.dcm')]

    # Load the first DICOM file
    if dicom_files:
        first_dicom_file = dicom_files[0]
        dicom_file_path = os.path.join('temp', first_dicom_file)
        # Read the DICOM file
    ds = pd.dcmread(dicom_file_path)
    
    # Extract pixel data from the DICOM file
    pixel_data = ds.pixel_array
    
    # Create an in-memory file object to store the pixel data
    pixel_data_file = io.BytesIO()
    
    # Write the pixel data to the in-memory file object
    ds.PixelData = pixel_data.tobytes()
    ds.save_as(pixel_data_file)
    
    # Move the file pointer to the beginning of the file object
    pixel_data_file.seek(0)
    
    # Send the pixel data as a file attachment
    return send_file(pixel_data_file, mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run(debug=True,port=6000)
