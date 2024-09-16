


def create_transaction_with_stripe(email: str, amount: int, name: str) -> None:
    # Create a transaction in stripe
    stripe.api_key = STRIPE_API_KEY
    logging.info(f"Creating transaction for user {email} with amount {amount}")
    transaction = stripe.PaymentIntent.create(
        amount=amount,
        currency="usd",
        payment_method_types=["card"],
        receipt_email=email,
        name=name
        card_number=card_number,
    )

    stripeEndpoint = 'http://stripe.com/api/v1/transactions/'

    response = requests.post(stripeEndpoint, data=transaction)
    if response.status_code == 201:
        return True
    else:
        return False

    logging.info(f"Creating transaction in stripe for {email}")
    return None