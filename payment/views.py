from django.shortcuts import render
from arts.models import Art
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
# Create your views here.
# def checkOut(request, art_id):
#
#     art = Art.objects.get(id=art_id)
#
#     host = request.get_host()
#
#     paypal_checkout = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': art.price,
#         'item_name': art.title,
#         'invoice': uuid.uuid4(),
#         'currency_code': 'USD',
#         'notify_url': f"http://{host}{reverse('paypal-ipn')}",
#         'return_url': f"http://{host}{reverse('payment-success', kwargs = {'art_id': art.id})}",
#         'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'art_id': art.id})}",
#     }
#
#     paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
#
#     context = {
#         'art': art,
#         'paypal': paypal_payment
#     }
#
#     return render(request, 'payments/checkout.html', context)
#
# def paymentSuccessful(request, art_id):
#
#     art = Art.objects.get(id=art_id)
#
#     return render(request, 'payments/payment-success.html', {'art': art})
#
# def paymentFailed(request, art_id):
#
#     art = Art.objects.get(id=art_id)
#
#     return render(request, 'payments/payment-failed.html', {'art': art})

def checkOut(request):
    cart = request.session.get('cart', {})
    total = 0
    item_names = []

    for art_id, quantity in cart.items():
        art = Art.objects.get(id=art_id)
        total += art.price * quantity
        item_names.append(f"{art.title} (x{quantity})")

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'item_name': ", ".join(item_names[:5]) + ("..." if len(item_names) > 5 else ""),
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs={'art_id': cart.art.id})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'art_id': cart.art.id})}"
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'cart': cart,
        'total': total,
        'paypal': paypal_payment,
    }

    return render(request, 'payments/checkout.html', context)

def paymentSuccessful(request):
    total = 0
    cart = request.session.get('cart', {})

    # Calculate total price
    for art_id, quantity in cart.items():
        art = Art.objects.get(id=art_id)
        total += art.price * quantity

    # Clear cart after successful payment
    request.session['cart'] = {}

    return render(request, 'payments/payment-success.html', {'total': total})

def paymentFailed(request):
    cart = request.session.get('cart', {})
    total = 0

    # Calculate total price for display
    for art_id, quantity in cart.items():
        art = Art.objects.get(id=art_id)
        total += art.price * quantity

    return render(request, 'payments/payment-failed.html', {'total': total, 'cart': cart})
