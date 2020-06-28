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
            query.add(Q(v_plate__icontains=q.get('v_plate')), Q.OR)

        if q.get('v_make') is not "":
            query.add(Q(v_make__icontains=q.get('v_make')), Q.OR)

        if q.get('v_model') is not "":
            query.add(Q(v_model_icontains=q.get('v_model')), Q.OR)

        if q.get('registration') is not "":
            query.add(Q(v_registration__icontains=q.get('registration')), Q.OR)

        if q.get('v_country') is not "":
            query.add(Q(v_country__icontains=q.get('v_country')), Q.OR)

        if q.get('v_state') is not "":
            query.add(Q(v_state__icontains=q.get('v_state')), Q.OR)

        object_list = Car.objects.filter(query)
        return object_list






# driver list view
class DriverListView(generic.ListView):
    model = Driver
    paginate_by = 25


# driver detail view
class DriverDetailView(generic.DetailView):
    model = Driver


# insurance list view
class InsuranceListView(generic.ListView):
    model = Insurance
    paginate_by = 25


class InsuranceDetailView(generic.DetailView):
    model = Insurance
