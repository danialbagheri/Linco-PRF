from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import ProductRequestForm, CustomerForm, AddressForm, ProductionListForm
from django.http import HttpResponseRedirect

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

# Create your views here.


def home(request):
    return render(request, "home.html", context={})


@login_required(login_url='/user/login/')
def product_request_form(request):
    user = request.user
    prf = ProductRequestForm()
    product_list_form = ProductionListForm()
    args = {
        'user': user,
        'prf': prf,
        'product_list_form': product_list_form 
    }
    return render(request, "PRF/product_request_form.html", args)

def add_customer(request):
    customer_form = CustomerForm()
    address_form = AddressForm()
    if request.POST:
        customer_form = CustomerForm(request.POST)
        address_form = AddressForm(request.POST)
        print('customer is posting')
        if customer_form.is_valid() and address_form.is_valid():
            print('valid')
            address = address_form.save()
            print(address)
            customer = customer_form.save()
            print(customer)
            customer.address.add(address)
            customer.save()
            messages.success(
                request, 'A new customer has successfully added to our database.')
            return HttpResponseRedirect('/request-form/')
        else:
            print('not valid')
            messages.error(request, customer_form.errors)
            messages.error(request, address_form.errors)
            args = {
                'customer_form': customer_form,
                'address_form': address_form
            }
            return render(request, "PRF/add_customer.html", args)
    args = {
        'customer_form': customer_form,
        'address_form': address_form
    }
    return render(request, "PRF/add_customer.html", args)

