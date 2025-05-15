from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
import json
from django.http import FileResponse
from .utils import generate_invoice
from .models import Payment
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from cart.models import Order
from rentals.models import Rental
from subscriptions.models import Subscription
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_invoice(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
        invoice = generate_invoice(payment)
        filename = f"invoice_{payment.id}.pdf"
        return FileResponse(invoice, as_attachment=True, filename=filename)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_invoice(request, payment_id=None, rental_id=None, subscription_id=None):
    try:
        if payment_id:
            payment = Payment.objects.get(id=payment_id, user=request.user)
        elif rental_id:
            payment = Payment.objects.get(rental_id=rental_id, user=request.user)
        elif subscription_id:
            payment = Payment.objects.get(subscription_id=subscription_id, user=request.user)
        else:
            return Response({'error': 'Payment ID or rental/subscription ID required'}, status=400)

        invoice = generate_invoice(payment)
        filename = f"invoice_{payment.id}.pdf"
        return FileResponse(invoice, as_attachment=True, filename=filename)

    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoice_ready(request, rental_id=None, subscription_id=None):
    try:
        if rental_id:
            rental = Rental.objects.get(id=rental_id, user=request.user)
            return Response({'invoice_ready': rental.invoice_generated})
        elif subscription_id:
            sub = Subscription.objects.get(id=subscription_id, user=request.user)
            return Response({'invoice_ready': sub.invoice_generated})
        else:
            return Response({'error': 'No rental or subscription ID provided'}, status=400)
    except Exception as e:
        return Response({'error': str(e)}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_invoice(request, payment_id=None, rental_id=None, subscription_id=None):
    try:
        if payment_id:
            payment = Payment.objects.get(id=payment_id, user=request.user)
        elif rental_id:
            payment = Payment.objects.get(rental_id=rental_id, user=request.user)
        elif subscription_id:
            payment = Payment.objects.get(subscription_id=subscription_id, user=request.user)
        else:
            return Response({'error': 'Payment ID or rental/subscription ID required'}, status=400)

        invoice = generate_invoice(payment)
        filename = f"invoice_{payment.id}.pdf"
        return FileResponse(invoice, as_attachment=True, filename=filename)

    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=404)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'whsec_test_key'  # Replace with your Stripe webhook secret

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        payment_intent_id = intent['id']
        payment.status = 'succeeded'
        payment.save()

        if payment.rental:
            payment.rental.is_paid = True
            payment.rental.invoice_generated = True
            payment.rental.save()

        if payment.subscription:
            payment.subscription.active = True
            payment.subscription.invoice_generated = True
            payment.subscription.save()    

        if payment.order:
            payment.order.is_paid = True
            payment.order.save()
        
        try:
            payment = Payment.objects.get(payment_intent=payment_intent_id)
            payment.status = 'succeeded'
            payment.save()
        except Payment.DoesNotExist:
            pass

    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        payment_intent_id = intent['id']

        try:
            payment = Payment.objects.get(payment_intent=payment_intent_id)
            payment.status = 'failed'
            payment.save()

            if payment.order:
                payment.order.delete()  # delete failed order

        except Payment.DoesNotExist:
            pass

        return HttpResponse(status=200)

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripePaymentIntent(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            amount = float(request.data.get('amount')) * 100  # convert to paisa
            intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency='inr',
                metadata={'user_id': request.user.id}
            )

            order_id = request.data.get('order_id')
            order = Order.objects.filter(id=order_id, user=request.user).first()

            if order:
                amount = order.total_amount * 100  # to paisa
            else:
                amount = float(request.data.get('amount')) * 100  # fallback

            rental_id = request.data.get('rental_id')
            subscription_id = request.data.get('subscription_id')

            rental = Rental.objects.filter(id=rental_id).first() if rental_id else None
            subscription = Subscription.objects.filter(id=subscription_id).first() if subscription_id else None

            payment = Payment.objects.create(
            user=request.user,
            amount=amount / 100,
            currency='INR',
            payment_intent=intent['id'],
            status=intent['status'],
            order=order
            )

            return Response({
                'client_secret': intent['client_secret'],
                'payment': PaymentSerializer(payment).data
            })

        except Exception as e:
            return Response({'error': str(e)}, status=400)
        

