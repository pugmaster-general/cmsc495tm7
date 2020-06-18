from django.shortcuts import render
from povreg.models import Car, Driver, Insurance, Officer
from django.views import generic


# Create your views here.
def index(request):
    """view function for the home page of the site"""

    #counts of records
    num_cars = Car.objects.all().count()
    num_drivers = Driver.objects.all().count()
    num_insurance = Insurance.objects.all().count()
    num_officers = Officer.objects.all().count()

    context = {
        'num_cars': num_cars,
        'num_drivers': num_drivers,
        'num_insurance': num_insurance,
        'num_officers': num_officers,
    }

    # render HTML template index.html with date in context
    return render(request, 'index.html', context=context)


# car list view
class CarListView(generic.ListView):
    model = Car
    paginate_by = 25


# car detail view
class CarDetailView(generic.DetailView):
    model = Car


# driver list view
class DriverListView(generic.ListView):
    model = Driver
    paginate_by = 25


# driver detail view
class DriverDetailView(generic.DetailView):
    model = Driver
