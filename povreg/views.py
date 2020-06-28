from django.shortcuts import render
from povreg.models import Car, Driver, Insurance, Officer
from django.views import generic
from django.db.models import Q
from django.template import loader

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


# car search form
class CarSearchForm(generic.TemplateView):
    template_name = 'povreg/car_search.html'


# car search results view
class CarSearchResultsView(generic.ListView):
    model = Car
    template_name = 'povreg/car_search_results.html'

    def get_queryset(self):
        q = self.request.GET
        query = Q()
        if q.get('v_plate') is not "":
            query.add(Q(v_plate__icontains=q.get('v_plate')), Q.AND)

        if q.get('v_make') is not "":
            query.add(Q(v_make__icontains=q.get('v_make')), Q.AND)

        if q.get('v_model') is not "":
            query.add(Q(v_model_icontains=q.get('v_model')), Q.AND)

        if q.get('registration') is not "":
            query.add(Q(v_registration__icontains=q.get('registration')), Q.AND)

        if q.get('v_country') is not "":
            query.add(Q(v_country__icontains=q.get('v_country')), Q.AND)

        if q.get('v_state') is not "":
            query.add(Q(v_state__icontains=q.get('v_state')), Q.AND)

        object_list = Car.objects.filter(query)
        return object_list


# driver list view
class DriverListView(generic.ListView):
    model = Driver
    paginate_by = 25


# driver detail view
class DriverDetailView(generic.DetailView):
    model = Driver


# car search form
class DriverSearchForm(generic.TemplateView):
    template_name = 'povreg/driver_search.html'


# car search results view
class DriverSearchResultsView(generic.ListView):
    model = Driver
    template_name = 'povreg/driver_search_results.html'

    def get_queryset(self):
        q = self.request.GET
        query = Q()
        if q.get('license_num') is not "":
            query.add(Q(license_num__icontains=q.get('license_num')), Q.AND)

        if q.get('first_name') is not "":
            query.add(Q(first_name__icontains=q.get('first_name')), Q.AND)

        if q.get('last_name') is not "":
            query.add(Q(last_name__icontains=q.get('last_name')), Q.AND)

        if q.get('country') is not "":
            query.add(Q(country__icontains=q.get('country')), Q.AND)

        if q.get('state') is not "":
            query.add(Q(state__icontains=q.get('state')), Q.AND)

        if q.get('phone_num') is not "":
            query.add(Q(phone_num__icontains=q.get('phone_num')), Q.AND)

        if q.get('dob') is not "":
            query.add(Q(dob__icontains=q.get('dob')), Q.AND)

        object_list = Driver.objects.filter(query)
        return object_list

# insurance list view
class InsuranceListView(generic.ListView):
    model = Insurance
    paginate_by = 25


class InsuranceDetailView(generic.DetailView):
    model = Insurance
