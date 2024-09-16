

def create_ticket_with_freshdesk(email: str, password: str) -> None:
    # Create a ticket in freshdesk
    freshdeskClient = FreshdeskClient(FRESHDESK_API_KEY, FRESHDESK_DOMAIN)
    ticket = {
        "description": f"Hello {email}, your account with password {password} has been created.",
        "subject": "Account Created",
        "email": email,
        "priority": 1,
        "status": 2,
    }

    logging.info(f"Creating ticket in freshdesk for {email}")
    freshdeskClient.create_ticket(ticket)
    return None


def update_user_data_with_freshdesk(email: str, phone_number: str, date_of_birth: str) -> None:
    # Update user data in freshdesk
    freshdeskClient = FreshdeskClient(FRESHDESK_API_KEY, FRESHDESK_DOMAIN)
    user = {
        "email": email,
        "phone_number": phone_number,
        "date_of_birth": date_of_birth
    }

    logging.info(f"Updating user data in freshdesk for {email}")
    freshdeskClient.update_user(user)
    return None