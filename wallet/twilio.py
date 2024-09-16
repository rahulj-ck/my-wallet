

def send_sms(to, body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(to=to, from_=TWILIO_PHONE_NUMBER, body=body)


def send_sms_with_twilio(to, phone_number, email: str, password: str, ) -> None:
    # Send a message to the user with the twilio api
    message = f"Hello {email}, your account with phone number {phone_number} and password {password} has been created."

    logging.info(f"Sending message to {email} with twilio: {message}")
    send_sms(to, message)
    return None
   
