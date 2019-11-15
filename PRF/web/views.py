from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import ProductRequestForm, CustomerForm, AddressForm, ProductionListForm
from django.http import HttpResponseRedirect
from .models import ProductionJob, ProductionList
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

# Create your views here.


def home(request):
    number_of_jobs = ProductionJob.objects.all().count()
    args = {
        "number_of_jobs":number_of_jobs
    }
    return render(request, "home.html", args)


@login_required(login_url='/user/login/')
def product_request_form(request):
    user = request.user
    prf = ProductRequestForm()
    product_list_form = ProductionListForm()
    if request.POST:
        response = request.POST.copy()
        '''
        Here we get the last Production Job and we find it's PRF number
        '''
        if ProductionJob.objects.count() == 0:
            prf_number = 10001
        else:
            last_prf_job = ProductionJob.objects.last()
            prf_number = last_prf_job.prf_number + 1
        response['prf_number'] = prf_number
        print(response)
        prf = ProductRequestForm(response)
        product_list_form = ProductionListForm(response)
        print(prf.errors)
        print(product_list_form.errors)
        if prf.is_valid and product_list_form.is_valid():
            # We save the forms first and we create an object of each form
            production_job = prf.save()
            production_list = product_list_form.save()
            # We then update all the missing information and link the objects together
            production_job.requested_by = user
            production_job.prf_number = prf_number
            production_job.customer_address_id = response['customer_address_id']
            production_job.production_list.add(production_list)
            production_job.status = "Pending"
            production_job.save()

            messages.success(
                request, 'Your PRF has been submitted for a review.')
            return HttpResponseRedirect('/jobs/all-jobs/')

        else:
            print(prf.errors)
            print(product_list_form.errors)
            print('not valid')
            messages.error(request, prf.errors)
            messages.error(request, product_list_form.errors)
            args = {
                'user': user,
                'prf': prf,
                'product_list_form': product_list_form
            }
            return render(request, "PRF/product_request_form.html", args)
    args = {
        'user': user,
        'prf': prf,
        'product_list_form': product_list_form
    }
    return render(request, "PRF/product_request_form.html", args)

@login_required(login_url='/user/login/')
def add_customer(request):
    customer_form = CustomerForm()
    address_form = AddressForm()
    if request.POST:
        customer_form = CustomerForm(request.POST)
        address_form = AddressForm(request.POST)
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


@login_required(login_url='/user/login/')
def all_jobs(request):
    NUM_USER_TO_SHOW = 30
    production_jobs =ProductionJob.objects.all()
    paginator = Paginator(production_jobs, NUM_USER_TO_SHOW)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    args = {
        "jobs": jobs
    } 
    return render(request, "jobs/all_jobs.html", args)


@login_required(login_url='/user/login/')
def user_jobs(request):
    NUM_USER_TO_SHOW = 30
    user = request.user
    production_jobs =ProductionJob.objects.filter(requested_by=user)
    paginator = Paginator(production_jobs, NUM_USER_TO_SHOW)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    args = {
        "jobs": jobs
    } 
    return render(request, "jobs/user_jobs.html", args)