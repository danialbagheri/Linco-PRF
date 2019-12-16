from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import ProductRequestForm, CustomerForm, AddressForm, ProductionListForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from datetime import timedelta, date
from .models import ProductionJob, ProductionList, ModelChangeLogsModel
from customer.models import Address


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

# Create your views here.


def add_business_days(from_date, number_of_days):
    to_date = from_date
    while number_of_days:
        to_date += timedelta(1)
        if to_date.weekday() < 5:  # i.e. is not saturday or sunday
            number_of_days -= 1
    return to_date


def home(request):
    number_of_jobs = ProductionJob.objects.all().count()
    args = {
        "number_of_jobs": number_of_jobs
    }
    return render(request, "home.html", args)


@login_required(login_url='/user/login/')
def product_request_form(request):
    user = request.user
    prf = ProductRequestForm()
    product_list_form = ProductionListForm()
    if request.POST:
        '''
        Here we get the last Production Job and we find it's PRF number
        '''
        response = request.POST.copy()
        if ProductionJob.objects.count() == 0:
            prf_number = 10001
        else:
            last_prf_job = ProductionJob.objects.last()
            prf_number = last_prf_job.prf_number + 1
        response['prf_number'] = prf_number
        response['requested_by'] = user.id
        prf = ProductRequestForm(response)
        product_list_form = ProductionListForm(response)

        if prf.is_valid() and product_list_form.is_valid():
            # We save the forms first and we create an object of each form
            production_job = prf.save()
            production_list = product_list_form.save()
            # We then update all the missing information and link the objects together
            production_job.customer_address_id = response['customer_address_id']
            production_job.production_list.add(production_list)
            production_job.status = "Pending"
            production_job.save()

            messages.success(
                request, 'Your PRF has been submitted for a review.')
            return HttpResponseRedirect('/jobs/all-jobs/')

        else:
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
    DEADLINE = 1
    production_jobs = ProductionJob.objects.all().exclude(
        status="Saved").order_by("requested_date")
    paginator = Paginator(production_jobs, NUM_USER_TO_SHOW)
    delayed = add_business_days(date.today(), DEADLINE)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    args = {
        "jobs": jobs,
        'delayed': delayed
    }
    return render(request, "jobs/all_jobs.html", args)


@login_required(login_url='/user/login/')
def user_jobs(request):
    NUM_USER_TO_SHOW = 30
    user = request.user
    production_jobs = ProductionJob.objects.filter(requested_by=user)
    paginator = Paginator(production_jobs, NUM_USER_TO_SHOW)

    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    args = {
        "jobs": jobs,
    }
    return render(request, "jobs/user_jobs.html", args)


@login_required(login_url='/user/login/')
def single_job(request, job_id):
    production_job = ProductionJob.objects.get(id=job_id)
    logs = ModelChangeLogsModel.objects.filter(
        table_name="ProductionJob", table_id=production_job.pk)
    users = User.objects.all()
    addresses = Address.objects.all()
    args = {
        "job": production_job,
        "logs": logs,
        "users": users,
        "addresses": addresses
    }
    return render(request, "jobs/single_job.html", args)
