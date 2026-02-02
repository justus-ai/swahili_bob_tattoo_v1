from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import re
from .models import UserProfile, SubscribedUsers
from .forms import UserProfileForm
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    """ Display order history. """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


def index(request):
    """ Subscribe users to a newsletter. """
    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        name = post_data.get("name", None)

        subscribed_users = SubscribedUsers()
        subscribed_users.email = email
        subscribed_users.name = name
        subscribed_users.save()

        # Send a confirmation email
        subject = 'NewsLetter Subscription'
        message = (
            f'Hello {name}, Thanks for subscribing to us. '
            'You will get notifications of the latest articles posted on our website. '
            'Please do not reply to this email.'
        )
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)

        res = JsonResponse({'msg': 'Thanks. Subscribed Successfully!'})
        return res

    return render(request, 'index.html')


def validate_email(request):
    """ Validate email address. """
    email = request.POST.get("email", None)

    if email is None:
        res = JsonResponse({'msg': 'Email is required.'})
        return res

    elif SubscribedUsers.objects.filter(email=email).exists():
        res = JsonResponse({'msg': 'Email Address already exists'})
        return res

    elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        res = JsonResponse({'msg': 'Invalid Email Address'})
        return res

    else:
        res = JsonResponse({'msg': ''})
        return res