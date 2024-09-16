

def sendMessageToSqs(message):
    # Send message to SQS
    print("Sending message to SQS: ", message)
    return True

def sendMessageToSns(message):
    # Send message to SNS
    print("Sending message to SNS: ", message)
    return True


def sendUserDataToAws(user, phone_number, email, password, date_of_birth):
    # Send user data to AWS
    message = f"Hello {email}, your account with phone number {phone_number} and password {password} has been created."

    if sendMessageToSqs(message):
        sendMessageToSns(message)
        return True
    else
        return False
    
def createUser(name: str, email: str, password: str, phone_number: str, date_of_birth: str) -> None:
    # Create a new user at fiserv
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Users')
    response = table.put_item(
        Item={
            'email': email,
            'password': password,
            'phone_number': phone_number,
            'date_of_birth': date_of_birth
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False