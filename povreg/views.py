from django.shortcuts import render
from povreg.models import Car, Driver, Insurance, Officer
from django.views import generic
from django.db.models import Q
from django.template import loader
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Officers').exists())
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
class CarListView(UserPassesTestMixin, generic.ListView):
    model = Car
    paginate_by = 25

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# car detail view
class CarDetailView(UserPassesTestMixin, generic.DetailView):
    model = Car

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# car search form
class CarSearchForm(UserPassesTestMixin, generic.TemplateView):
    template_name = 'povreg/car_search.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# car search results view
class CarSearchResultsView(UserPassesTestMixin, generic.ListView):
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

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# driver list view
class DriverListView(UserPassesTestMixin, generic.ListView):
    model = Driver
    paginate_by = 25

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# driver detail view
class DriverDetailView(UserPassesTestMixin, generic.DetailView):
    model = Driver

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# driver search form
class DriverSearchForm(UserPassesTestMixin, generic.TemplateView):
    template_name = 'povreg/driver_search.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# driver search results view
class DriverSearchResultsView(UserPassesTestMixin, generic.ListView):
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

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# insurance list view
class InsuranceListView(UserPassesTestMixin, generic.ListView):
    model = Insurance
    paginate_by = 25

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


class InsuranceDetailView(UserPassesTestMixin, generic.DetailView):
    model = Insurance

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# insurance search form
class InsuranceSearchForm(UserPassesTestMixin, generic.TemplateView):
    template_name = 'povreg/insurance_search.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()


# insurance search results view
class InsuranceSearchResultsView(UserPassesTestMixin, generic.ListView):
    model = Insurance
    template_name = 'povreg/insurance_search_results.html'

    def get_queryset(self):
        q = self.request.GET
        query = Q()
        if q.get('policy_num') is not "":
            query.add(Q(policy_num__icontains=q.get('policy_num')), Q.AND)

        if q.get('company') is not "":
            query.add(Q(company__icontains=q.get('company')), Q.AND)

        if q.get('coverage_type') is not "":
            query.add(Q(coverage_type=q.get('coverage_type')), Q.AND)

        object_list = Insurance.objects.filter(query)
        return object_list

    def test_func(self):
        return self.request.user.groups.filter(name='Officers').exists()
