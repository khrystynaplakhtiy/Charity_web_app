from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from charity.models import *
from django.db.models import Sum
from charity.forms import *
from django.contrib.auth import authenticate, login, logout


# Create your views here.



class LandingPage(View):
    def get(self, request):
        quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        institutions_count = Institution.objects.all().count()
        institutions = Institution.objects.all()
        ctx = {
            "quantity": quantity,
            "institutions_count": institutions_count,
            "institutions": institutions,
            "fund": "fundacja",
            "ngo": "organizacja pozarządowa",
            "local_charity": "zbiórka lokalna"
        }
        return render(request, "index.html", ctx)


class AddDonation(View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        institutions_categories = []
        for institution in institutions:
            institutions_categories.append([v.id for v in institution.categories.all()])

        ctx = {
            "categories": categories,
            "institutions": institutions,
            "institutions_categories": institutions_categories,
        }
        if not request.user.is_authenticated:
            return redirect('login_page')
        else:
            return render(request, 'form.html', ctx)

    # def post (self, request):





class LoginPage(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('landing_page')
        else:
            return redirect('register_page')
        return render(request, 'login.html')


class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')


class RegisterPage(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            u = form.save()
            login(request, u)
            return redirect('/login')

        return render(request, 'register.html', {'form': form})












