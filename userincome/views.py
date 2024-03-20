from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from datetime import datetime
# Create your views here.

#again same api call but this time on income part
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date_str = request.POST['income_date']
        source_name = request.POST['source']

        try:
            amount = int(amount)
        except ValueError:
            messages.error(request, 'Amount must be an integer')
            return render(request, 'income/add_income.html', context)

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)

        # If no date is provided, default to today's date
        if not date_str:
            date = datetime.now().date()
        else:
            try:
                # Convert the date string to a datetime object
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'Invalid date format. Please use YYYY-MM-DD')
                return render(request, 'income/add_income.html', context)

        try:
            # Trying to fetch corresponding source instance from the database (user ka data)
            source = Source.objects.get(name=source_name)
        except Source.DoesNotExist:
            # If source doesn't exist, create a new one
            source = Source.objects.create(name=source_name)

        # Create UserIncome instance with the obtained source instance for each income different record
        UserIncome.objects.create(owner=request.user, amount=amount, date=date,
                                  source=source, description=description)
        messages.success(request, 'Record saved successfully')

        return redirect('income')


@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date_str = request.POST['income_date']
        source_name = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)

        try:
            # to fetch  corresponding source instance from database
            source = Source.objects.get(name=source_name)
        except Source.DoesNotExist:
            # If source doesn't exist, create a new one
            source = Source.objects.create(name=source_name)

        # Update UserIncome instance with the obtained source instance and other input values
        income.amount = amount
        income.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        income.source = source
        income.description = description
        income.save()
        messages.success(request, 'Record updated successfully')
        return redirect('income')


def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'record removed')
    return redirect('income')
