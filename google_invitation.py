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
