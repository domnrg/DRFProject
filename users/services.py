import stripe
from decimal import Decimal
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name: str):
    """Создает продукт в страйпе"""

    return stripe.Product.create(name=name)


def create_stripe_price(amount: Decimal, product_id: str):
    """Создает цену в страйпе"""

    return stripe.Price.create(
        currency="usd",
        unit_amount=int(amount * 100),
        product=product_id,
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return {
        "session_id": session.id,
        "payment_url": session.url,
    }


def create_stripe_payment(amount: Decimal, name: str):
    product = create_stripe_product(name)
    price = create_stripe_price(amount, product.id)
    return create_stripe_session(price)
