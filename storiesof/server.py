# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_PSzgLd5UfWwzWgOzQtVbAI2q00K0R7BBna'

intent = stripe.PaymentIntent.create(
  amount=1099,
  currency='eur',
  # Verify your integration in this guide by including this parameter
  metadata={'integration_check': 'accept_a_payment'},
)