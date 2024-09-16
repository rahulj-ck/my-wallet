salesforceEndpoint = 'https://login.salesforce.com/services/oauth2/token'

def authenticate(clientId: str, clientSecret: str, username: str, password: str) -> str:
    # Authenticate with Salesforce
    payload = {
        'grant_type': 'password',
        'client_id': clientId,
        'client_secret': clientSecret,
        'username': username,
        'password': password
    }
    response = requests.post(salesforceEndpoint, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None
    


def getUserData(token: str, userId: str) -> dict:
    # Get user data from Salesforce
    apiEndpoint = f'https://salesforce.com/api/v1/users/{userId}'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(apiEndpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
    # log user email and phone number
    print(f"User email: {response.json()['email']}")
    print(f"User phone number: {response.json()['phone']}")
    return None


