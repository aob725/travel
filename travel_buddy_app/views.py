from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.db.models import Q

def index(request):
    return render(request, 'main.html')

def register(request):
    errors = User.objects.registerValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    newuser = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashedpw)
    request.session['loggedinId'] = newuser.id
    return redirect('/travels')

def travels(request):
    if 'loggedinId' not in request.session:
        return redirect('/')
    alltrips = Trip.objects.all()
    loggedinuser = User.objects.get(id = request.session['loggedinId'])
    context = {
        'loggedinUser': loggedinuser,
        'mytrips': Trip.objects.filter(Q(uploader = loggedinuser) | Q(joiner = loggedinuser)),
        'notmytrips': Trip.objects.exclude(Q(uploader = loggedinuser) | Q(joiner = loggedinuser)),
    }
    return render(request, 'travels.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    user = User.objects.get(username = request.POST['username'])
    request.session['loggedinId'] = user.id
    return redirect('/travels')

def addTripForm(request):
    return render(request, 'addTrip.html')

def createTrip(request):
    print(request.POST)
    errors = Trip.objects.tripValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/travels/add')

    loggedinuser = User.objects.get(id = request.session['loggedinId'])

    newtrip = Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'], travelstart = request.POST['travelstart'], travelend = request.POST['travelend'], uploader = loggedinuser)
    return redirect('/travels')

def viewDest(request, tripid):
    alltrips = Trip.objects.all()
    tripToView = Trip.objects.get(id = tripid)
    # Google Maps API goes here, pass it through to context
    context = {
        'users': Trip.objects.get(id=tripid),
        'trips': alltrips,
        'tripinfo': tripToView,
    }
    return render(request, 'dest.html', context)

def addTraveler(request, tripid):
    loggedinuser = User.objects.get(id= request.session['loggedinId'])
    trip = Trip.objects.get(id= tripid)
    trip.joiner.add(loggedinuser)
    return redirect('/travels')

def search(request):
    loggedinuser = User.objects.get(id= request.session['loggedinId'])
    if request.method == 'GET':
        search = request.GET.get('search')
        trips = Trip.objects.all().filter(destination__contains = search)
        context = {
            'trips' : trips,
            'loggedinuser' : loggedinuser,
        }
        return render(request, 'search.html', context)