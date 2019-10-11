from django.shortcuts import render, redirect
from django.views import View
from charity.models import *
from django.db.models import Sum

# Create your views here.


class LandingPage(View):
    def get(self, request):
        quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        institutions_count = Institution.objects.all().count()
        ctx = {
            "quantity": quantity,
            "institutions_count": institutions_count
        }
        return render(request, "index.html", ctx)


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterPage(View):
    def get(self, request):
        return render(request, 'register.html')


