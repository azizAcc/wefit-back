import stripe as stripe
from flask import jsonify, request
import os
from flask_restx import Namespace, Resource
from dotenv import load_dotenv

load_dotenv()

stripe_api = Namespace(
    'stripe',
    description='stripe checkout api'
)

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}
stripe.api_key = stripe_keys["secret_key"]


@stripe_api.route("/config")
class PublishKey(Resource):
    def get(self):
        print(stripe_keys)
        stripe_config = {"publicKey": stripe_keys["publishable_key"]}
        return jsonify(stripe_config)

@stripe_api.route("/create-checkout-session", methods=['POST'])
class CreateCheckoutSession(Resource):
    def post(self):
        stripe.api_key = stripe_keys["secret_key"]
        print(request.get_json())
        data_request = request.get_json()
        basic_domain = 'http://localhost:9000'
        print(type(basic_domain))
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=basic_domain + data_request['success_url'],
                cancel_url=basic_domain + data_request['cancel_url'],
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        'price_data': {
                            'currency': "usd",
                            'unit_amount': request.get_json()['price'],
                            'product_data': {
                                'name': "shirt",
                                'description': "new model",
                            }
                        },
                        'quantity': 1,
                    },
                ]
            )
            print(checkout_session["id"])
            return {"sessionId": checkout_session["id"]}

        except Exception as e:
            return jsonify(error=str(e)), 403
