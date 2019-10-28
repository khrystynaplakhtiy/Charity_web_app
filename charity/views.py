from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from charity.models import *
from django.db.models import Sum
from charity.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


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


class DonationConfirmation(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "form-confirmation.html")


class AddDonation(LoginRequiredMixin,View):
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

    def post (self, request):
        user = request.user
        inst = request.POST.get('organization')
        institution = Institution.objects.get(name=inst)

        categories = [int(x) for x in request.POST.getlist('categories')]
        quantity = request.POST.get('bags')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('date')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')

        if quantity and address and phone_number and city and zip_code and pick_up_time and pick_up_date:

            Donation.objects.create(institution=institution, user_id=user.id,
                                    quantity=quantity, address=address, city=city, phone_number=phone_number,
                                    zip_code=zip_code, pick_up_date=pick_up_date,
                                    pick_up_time=pick_up_time, pick_up_comment=pick_up_comment)

            latest_donation = Donation.objects.all().order_by('-id')[:1][0]
            latest_donation.categories.set(categories)


            return redirect('donation-confirmation')
        return render(request, 'form.html')


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
        return render(request, 'register_2.html')

    def post(self, request):

        first_name = request.POST.get('name')
        last_name = request.POST.get('surname')
        username = request.POST.get('email')
        if len(request.POST.get('password')) >= 8 and request.POST.get('password') == request.POST.get('password2'):
            password = request.POST.get('password')

            User.objects.create_user(first_name=first_name,
                                     last_name=last_name,
                                     username=username,
                                     password=password)
            return redirect('/login')
        elif len(request.POST.get('password')) < 8:
            info_1 = 'Hasło jest za krótkie, powinno mieć min. 8 znaków.'
            return render(request, 'register_2.html', {'info_1': info_1})
        else:
            info_2 = 'Hasło inne niż wpisane wcześniej, spróbuj ponownie.'
            return render(request, 'register_2.html', {'info_2': info_2})




class UserProfile(LoginRequiredMixin, View):
    def get(self, request):

        user = request.user
        quantity = Donation.objects.filter(user_id=user.id).aggregate(Sum('quantity'))['quantity__sum']
        donations_obj = [donation_obj for donation_obj in Donation.objects.filter(user_id=user.id)]
        institutions_id = [obj.institution_id for obj in donations_obj]
        institutions_name = ", ".join([str(Institution.objects.get(pk=id)) for id in institutions_id])
        donation_id = [obj.id for obj in donations_obj]
        categories = []
        for id in donation_id:
            donation_categories = (Donation.objects.get(pk=id).categories.all()).values_list('name', flat=True)
            for item in donation_categories:
                categories.append(item)
        categories_name = ", ".join([str(name) for name in categories])


        return render(request, "user-profile2.html", {'quantity': quantity,
                                                      'institutions_name':institutions_name,
                                                      'categories_name': categories_name
                                                      })








