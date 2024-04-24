from urllib.parse import urlencode

def get_google_login_url(group_id):
    authorize_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': f'{REDIRECT_URI}?group={group_id}',  # Append group ID to redirect_uri
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
    }
    return authorize_url + '?' + urlencode(params)

@app.route('/google-callback')
def google_callback():
    # Get the group ID from the query parameters
    group_id = request.args.get('group_id')

    # Do something with the group ID
    # For example, associate the user with the specified group

    # Continue with the rest of your authentication process
####### Sample code 
from flask import Flask, request
from flask_restx import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# Define parser for arguments
parser = reqparse.RequestParser()
parser.add_argument('parameter1', type=str, required=True, help='This parameter is required')
parser.add_argument('parameter2', type=str, required=False, help='This parameter is optional')

@api.route('/upload')
class UploadFiles(Resource):
    def post(self):
        args = parser.parse_args()
        parameter1 = args['parameter1']
        parameter2 = args.get('parameter2')

        # Access uploaded files
        files = request.files.getlist('file')  # Use getlist for multiple files

        # Process files and parameters
        for file in files:
            # You can access filename and data using file.filename and file.read()
            print(f"Uploaded file: {file.filename}")
            # Process file data here

        # Return response based on processing
        return {'message': 'Files and parameters uploaded successfully!',
                'parameter1': parameter1,
                'parameter2': parameter2}

if __name__ == '__main__':
    app.run(debug=True)
