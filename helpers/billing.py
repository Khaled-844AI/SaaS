from email.policy import default

import stripe
from decouple import config

STRIP_API_KEY = config('STRIPE_SECRET_KEY', default="", cast=str)
DJANGO_DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

if 'sk_test' in STRIP_API_KEY and not DJANGO_DEBUG:
  raise ValueError('Invalid strip key for production')

stripe.api_key = STRIP_API_KEY

def create_user(name="", email="", raw=False, metadata={}):
  response = stripe.Customer.create(
    name=name,
    email=email,
    metadata=metadata,
  )
  if raw:
    return response
  return response.id


def create_product(name="", raw=False, metadata={}):
  response = stripe.Product.create(
    name=name,
    metadata=metadata)
  if raw:
    return response
  return response.id

def create_price(currency="usd",
                unit_amount="9999",
                recurring={"interval": "month"},
                product=None,
                metadata={},
                raw=False):
  if product is None:
    return None

  response = stripe.Price.create(
                currency=currency,
                unit_amount=unit_amount,
                recurring=recurring,
                product=product,
                metadata=metadata
            )

  if raw:
    return response
  return response.id

def start_checkout_session(customer_id,
        success_url="",
        cancel_url="",
        price_stripe_id="",
        raw=True):
    if not success_url.endswith("?session_id={CHECKOUT_SESSION_ID}"):
        success_url = f"{success_url}" + "?session_id={CHECKOUT_SESSION_ID}"
    response= stripe.checkout.Session.create(
        customer=customer_id,
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=[{"price": price_stripe_id, "quantity": 1}],
        mode="subscription",
    )
    if raw:
        return response
    return response.url


def get_checkout_session(session_id, raw=True):
    response = stripe.checkout.Session.retrieve(
              session_id
            )

    if raw:
        return response
    return response.url

def get_subscription(stripe_id, raw=True):
    response = stripe.Subscription.retrieve(
              stripe_id
            )

    if raw:
        return response
    return response.url