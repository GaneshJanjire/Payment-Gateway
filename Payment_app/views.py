from django.http import HttpResponseBadRequest
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Order
from django.views.decorators.csrf import csrf_exempt
import razorpay
# from RazorpayProject.settings import (
#     RAZORPAY_KEY_ID,
#     RAZORPAY_KEY_SECRET,
# )

from .serializers import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
import json
import logging
logger = logging.getLogger(__name__)

# Create your views here.


def home(request):
    return render(request, "index.html")



# from django.shortcuts import render
# from django.views.decorators.csrf import ensure_csrf_cookie

# @ensure_csrf_cookie
# def order_payment(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         amount = request.POST.get("amount")
#         client = razorpay.Client(auth=('rzp_test_SkUIyWYTZQ20H8', '2KuP5OCk3gnPiHqXkp8UDFpG'))
#         razorpay_order = client.order.create(
#             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         )
#         order = Order.objects.create(
#             name=name, amount=amount, provider_order_id=razorpay_order["id"]
#         )
#         order.save()
#         return render(
#             request,
#             "payment.html",
#             {
#                 "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay_integration/callback/",
#                 "razorpay_key": 'rzp_test_SkUIyWYTZQ20H8',
#                 "order": order,
#             },
#         )
#    return render(request, "payment.html")

def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=('rzp_test_KhECfjuAju7F18', 'MmpLb3g2lKt9bVGmLek9WTEE'))  #enter razorpay Key ID, RAZORPAY_KEY_SECRET
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=razorpay_order["id"]
        )
        order.save()
        return render(
            request,
            "payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay_integration/callback/",
                "razorpay_key": 'rzp_test_KhECfjuAju7F18',
                "order": order,
            },
        )
    return render(request, "payment.html")


# @csrf_exempt
# def callback(request):
#     def verify_signature(response_data):
#         client = razorpay.Client(auth=('rzp_test_KhECfjuAju7F18', 'MmpLb3g2lKt9bVGmLek9WTEE'))
#         return client.utility.verify_payment_signature(response_data)

#     logger.info(request)

#     if "razorpay_signature" in request.POST:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         signature_id = request.POST.get("razorpay_signature", "")
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.signature_id = signature_id
#         order.save()
#         signature_verify = verify_signature(request.POST)
#         logger.info('signature verify: ' + str(signature_verify))
#         if signature_verify:
#             order.status = PaymentStatus.SUCCESS
#             order.save()
#             return render(request, "callback.html", context={"status": order.status})
#         else:
#             order.status = PaymentStatus.FAILURE
#             order.save()
#             return render(request, "callback.html", context={"status": order.status})
#     else:
#         error_metadata = request.POST.get("error[metadata]")
#         if error_metadata:
#             try:
#                 metadata_dict = json.loads(error_metadata)
#                 payment_id = metadata_dict.get("payment_id")
#                 provider_order_id = metadata_dict.get("order_id")
#                 order = Order.objects.get(provider_order_id=provider_order_id)
#                 order.payment_id = payment_id
#                 order.status = PaymentStatus.FAILURE
#                 order.save()
#                 return render(request, "callback.html", context={"status": order.status})
#             except json.JSONDecodeError as e:
#                 logger.error(f"Error decoding JSON: {e}")
#                 # Handle JSON decoding error, log it, and possibly take appropriate action
#         else:
#             # Handle the case when "error[metadata]" is not present in request.POST
#             # For example, you may want to log a warning or take appropriate action.
#             logger.warning("No 'error[metadata]' key in request.POST")

#     return HttpResponseBadRequest("Invalid request")
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=('rzp_test_KhECfjuAju7F18', 'MmpLb3g2lKt9bVGmLek9WTEE'))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        signature_verify = verify_signature(request.POST)
        
        if signature_verify:
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", {"status": "Success"})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", {"status": "Failure"})
    else:
        error_data = request.POST.get("error[metadata]", "{}")
        metadata = json.loads(error_data) if error_data else {}
        payment_id = metadata.get("payment_id", "")
        provider_order_id = metadata.get("order_id", "")
        
        if provider_order_id:
            order = Order.objects.get(provider_order_id=provider_order_id)
            order.payment_id = payment_id
            order.status = PaymentStatus.FAILURE
            order.save()
        
        return render(request, "callback.html", {"status": "Failure"})


# @csrf_exempt
# def callback(request):
#     def verify_signature(response_data):
#         client = razorpay.Client(auth=('rzp_test_SkUIyWYTZQ20H8', '2KuP5OCk3gnPiHqXkp8UDFpG'))
#         return client.utility.verify_payment_signature(response_data)

#     logger.info(request)

#     if "razorpay_signature" in request.POST:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         signature_id = request.POST.get("razorpay_signature", "")
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.signature_id = signature_id
#         order.save()
#         signature_verify = verify_signature(request.POST)
#         logger.info('signature verify: ' + str(signature_verify))
#         if signature_verify:
#             order.status = PaymentStatus.SUCCESS
#             order.save()
#             return render(request, "callback.html", context={"status": order.status})
#         else:
#             order.status = PaymentStatus.FAILURE
#             order.save()
#             return render(request, "callback.html", context={"status": order.status})
#     else:
#         payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#         provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
#             "order_id"
#         )
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.status = PaymentStatus.FAILURE
#         order.save()
#         return render(request, "callback.html", context={"status": order.status})


# from django.shortcuts import render
# from django.views import View
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Order
# from .serializers import PaymentStatus
# import json
# import logging
# import razorpay

# logger = logging.getLogger(__name__)

# class HomeView(View):
#     def get(self, request):
#         return render(request, "index.html")

# class OrderPaymentView(View):
#     def post(self, request):
#         name = request.POST.get("name")
#         amount = request.POST.get("amount")
#         client = razorpay.Client(auth=('rzp_test_SkUIyWYTZQ20H8', '2KuP5OCk3gnPiHqXkp8UDFpG'))
#         razorpay_order = client.order.create(
#             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#         )
#         order = Order.objects.create(
#             name=name, amount=amount, provider_order_id=razorpay_order["id"]
#         )
#         order.save()
#         return render(
#             request,
#             "payment.html",
#             {
#                 "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay_integration/callback/",
#                 "razorpay_key": 'rzp_test_SkUIyWYTZQ20H8',
#                 "order": order,
#             },
#         )

# class CallbackView(View):
#     @csrf_exempt
#     def post(self, request):
#         def verify_signature(response_data):
#             client = razorpay.Client(auth=('rzp_test_SkUIyWYTZQ20H8', '2KuP5OCk3gnPiHqXkp8UDFpG'))
#             return client.utility.verify_payment_signature(response_data)

#         logger.info(request)

#         if "razorpay_signature" in request.POST:
#             payment_id = request.POST.get("razorpay_payment_id", "")
#             provider_order_id = request.POST.get("razorpay_order_id", "")
#             signature_id = request.POST.get("razorpay_signature", "")
#             order = Order.objects.get(provider_order_id=provider_order_id)
#             order.payment_id = payment_id
#             order.signature_id = signature_id
#             order.save()
#             signature_verify = verify_signature(request.POST)
#             logger.info('signature verify: ' + str(signature_verify))
#             if signature_verify:
#                 order.status = PaymentStatus.SUCCESS
#                 order.save()
#                 return render(request, "callback.html", context={"status": order.status})
#             else:
#                 order.status = PaymentStatus.FAILURE
#                 order.save()
#                 return render(request, "callback.html", context={"status": order.status})
#         else:
#             payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#             provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
#                 "order_id"
#             )
#             order = Order.objects.get(provider_order_id=provider_order_id)
#             order.payment_id = payment_id
#             order.status = PaymentStatus.FAILURE
#             order.save()
#             return render(request, "callback.html", context={"status": order.status})
