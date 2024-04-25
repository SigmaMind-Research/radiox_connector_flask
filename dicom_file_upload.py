import os
import requests
import tempfile
import zipfile

def upload_dicom_to_api(file_paths, api_url, group_id, study_instance_id):
    try:
        files_data = []
        for file_path in file_paths:
            # Get the filename from the file path
            file_name = os.path.basename(file_path)
            
            # Read the DICOM file content
            with open(file_path, 'rb') as dicom_file:
                file_content = dicom_file.read()

            # Add file name and content to the list
            files_data.append((file_name, file_content))

        # Prepare files to send to the API
        files = {f'file_{idx}': (file_name, file_content, 'application/dicom') for idx, (file_name, file_content) in enumerate(files_data)}

        # Prepare data to send to the API
        data = {'group_id': group_id, 'study_id': study_instance_id}
        print(files_data)
        # Send POST request to the API
        response = requests.post(api_url, files=files, data=data)

        # Check response status
        if response.status_code == 200:
            print("File uploaded successfully!")
        else:
            print(f"Failed to upload file: {response.text}")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")


def send_patient_data_to_api(patient_study_ids, api_url):
    try:
        # Prompt user to input mobile number
        mobile_number = input("Enter patient's mobile number: ")

        # Prepare data to send to the API
        data = {
            'patient_study_ids': patient_study_ids,
            'mobile_number': mobile_number
        }

        # Send POST request to the API
        response = requests.post(api_url, json=data)

        # Check response status
        if response.status_code == 200:
            print("Data sent to API successfully!")
        else:
            print(f"Failed to send data to API: {response.text}")
    except Exception as e:
        print(f"Error sending data to API: {str(e)}")


file_paths = []
for file in os.listdir(file_path):
  file_paths.append(os.path.join(file_path, file))   
  # print('flask route') 
upload_dicom_to_api(file_paths,"http://localhost:6000/upload",'xyz123',study_id)
send_patient_data_to_api(study_id, "http://localhost:6000/submit_patient_data")
