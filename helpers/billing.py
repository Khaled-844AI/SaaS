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