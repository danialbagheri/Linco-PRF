from django.shortcuts import render
from .models import Customer, Address
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
# Create your views here.


def all_customer_addresses(request, id):
    # customer = get_object_or_404(Customer, pk=id)
    customer = Customer.objects.get(id=id)
    print(customer)
    customer_addresses = Address.objects.filter(customer=customer).all()
    print(customer_addresses.count())
    if customer_addresses.count() >= 1:
        list_of_Addresses = []
        for addresses in customer_addresses:
            address = {
                "address_line_1": addresses.address_line_1,
                "address_line_2": addresses.address_line_2,
                "city": addresses.city,
                "country": addresses.country,
                "post_code": addresses.post_code,
            }
            list_of_Addresses.append(address)

        args = {
            "customer_addresses": list_of_Addresses
        }
    else:
        raise Http404()

    return JsonResponse(args, safe=False)
