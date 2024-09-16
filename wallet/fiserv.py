

def createUser(name: str, email: str, password: str, ) -> None:
    # Create a new user at fiserv
    apiEndpoint = 'http://fiserv.com/api/v1/users/'
    payload = {
        'name': name,
        'email': email,
        'password': password
    }
    response = requests.post(apiEndpoint, data=payload)
    if response.status_code == 201:
        return True
    else:
        return False


def createBankAccount(user: User, accountNumber: str, balance: float, ) -> None:
    # Create a bank account for a user at fiserv
    apiEndpoint = 'http://fiserv.com/api/v1/accounts/'
    payload = {
        'user': user.id,
        'account_number': accountNumber,
        'balance': balance
    }
    response = requests.post(apiEndpoint, data=payload)
    if response.status_code == 201:
        return True
    else:
        return False
    



