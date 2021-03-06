from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from products.models import Product
from samples.models import SampleStatus
from django.core.mail import send_mail
import stripe


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET


@login_required()
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.user = request.user
            order.save()

            cart = request.session.get('cart', {})
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=quantity
                    )
                order_line_item.save()
                for x in range(quantity):
                    sample = SampleStatus(
                        status='Ordered',
                        order=order,
                        testing_required=product.test_type,
                        ordered_by=request.user,
                        ordered_date=timezone.now(),
                        )

                    sample.save()
                    sample.sample_ref = "{0}-{1}".format(
                        sample.testing_required,
                        sample.id)

                    sample.save()
            try:
                # using stripe API
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'])

            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.success(request, "You have successfully paid")
                request.session['cart'] = {}

                user = order.user
                print(user.email)
                send_mail('Order Confirmation',
                          order_confirm_email(order),
                          'eascatest@gmail.com',
                          [user.email],
                          fail_silently=False,
                          )

                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request,
                           "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
    arg = {'order_form': order_form,
           'payment_form': payment_form,
           'publishable': settings.STRIPE_PUBLISHABLE}

    return render(request, "checkout.html", arg)


def order_confirm_email(order):
    """Return email content to be sent to customer when their
    results are complete"""
    email_content = """\
    Hi {0},

    You will receive your soil sample kit in the post in the next few days.
    To upload the samples details online, just log into 'Your Portal':

    https://dc-easca-environmental.herokuapp.com/yourportal


    Regards,

    Dan Casey

    Lab Rat
    Easca Environmental

    """.format(order.user.username)
    return email_content
