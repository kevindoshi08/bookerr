from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import *
from django.http import HttpResponse


def getUserDetails(request):
    user = User.objects.filter(id=request.user.id)
    userDet = UserDetails.objects.filter(user__in=user)
    return userDet[0]


def home(request):
    message = ''
    try:
        message = request.GET.get("message")
    except:
        pass
    if request.user.is_authenticated:
        userDet = getUserDetails(request)
        books = Book.objects.all()
        context = {'books': books, 'userDet': userDet, 'nbar': 'home', 'message': message}
        return render(request, 'portal/home.html', context)
    else:
        return redirect('login')


def profile(request):
    if request.user.is_authenticated:
        userDet = getUserDetails(request)
        return render(request, 'portal/profile.html', {'user': request.user, 'userDet': userDet, 'nbar': 'profile'})
    else:
        return redirect('login')


def cart(request):
    if request.user.is_authenticated:
        userDet = getUserDetails(request)
        bookIds = BookUserModel.objects.filter(user=userDet)
        cartBooks = []
        for bookId in bookIds:
            cartBooks += Book.objects.filter(id=bookId.book.id).values()
        return render(request, 'portal/cart.html', {'userDet': userDet, 'cartBooks': cartBooks, 'nbar': 'cart'})
    else:
        return redirect('login')


def about(request):
    if request.user.is_authenticated:
        userDet = getUserDetails(request)
        return render(request, 'portal/about.html', {'userDet': userDet, 'nbar': 'about'})
    else:
        return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user.set_password(raw_password)
            user.save()

            userdetails = UserDetails(user=user, wallet=2000)
            userdetails.save()

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'portal/signup.html', {'form': form})


def buynow(request):
    bookId = request.GET.get('id')
    userDet = getUserDetails(request)
    book = Book.objects.filter(id=bookId)
    bookuser = BookUserModel.objects.filter(user=userDet, book=book[0])
    bookPrice = book[0].getPrice()
    bucount = bookuser.count()

    if bucount > 0:
        return HttpResponse('duplicate')
    else:
        if userDet.wallet >= bookPrice:
            userDet.wallet = userDet.wallet - bookPrice
            userDet.save()
            bookuser = BookUserModel(user=userDet, book=book[0])
            bookuser.save()
            return HttpResponse('success')
        else:
            return HttpResponse('insufficient')
