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
    
    logger.info("Received user with email: " + response.json()['email'])
    return None



def sendUserDataToSalesforce(user: User, email: str, password: str, phone_number: str, date_of_birth: str) -> None:
    # Send user data to Salesforce
    token = authenticate(SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_USERNAME, SALESFORCE_PASSWORD)
    if token:
        user_data = {
            'name': user.name,
            'email': email,
            'phone_number': phone_number,
            'date_of_birth': date_of_birth
        }
        response = createUser(user_data, token)
        if response:
            return True
        else:
            return False
    else:
        return False