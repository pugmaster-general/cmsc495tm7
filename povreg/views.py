from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.forms import TextInput, DateInput
from django.shortcuts import render, HttpResponseRedirect
from django.template import loader
from django.views import generic
from .models import Car, Driver, Insurance, Officer
from .forms import UserForm

# Create your views here.


@login_required
#@user_passes_test(lambda u: u.groups.filter(name='Officers').exists())
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


# user view
@login_required()
def view_user(request):
    #get pk of logged in user
    pk = request.user.pk

    #query the user object with pk from logged in user
    user = User.objects.get(pk=pk)

    #find user group
    if user.groups.filter(name='Officers').exists():
        group = 'officer'
        profile = user.officer
    elif user.groups.filter(name='Drivers').exists():
        group = 'driver'
        profile = user.driver
    else:
        group = 'none'
        profile = None
    context = {
        'group': group,
        'user': user,
        'profile': profile,
    }

    if request.user.is_authenticated and request.user.id == user.id:
        return render(request, 'povreg/profile_view.html', context=context)
    else:
        raise PermissionDenied


# user update form
@login_required()
def edit_user(request):
    #get pk of logged in user
    pk = request.user.pk

    #query the user object with pk from logged in user
    user = User.objects.get(pk=pk)

    #prepopulate UserProfileForm with retrieved user values from above
    user_form = UserForm(instance=user)

    #so-called sorcery happens below
    widgets = dict()
    fields = ()
    profile = None
    if user.groups.filter(name='Officers').exists():
        fields = ('rank', 'region', 'unit')
        sub = Officer
        profile = user.officer
        group = "officer"

    elif user.groups.filter(name='Drivers').exists():
        fields = ('last_name', 'first_name', 'phone_num', 'country', 'state', 'license_num', 'license_expiry')
        sub = Driver
        profile = user.driver
        group = 'driver'

    for i in fields:
        widgets[str(i)] = TextInput()

    if profile is Driver:
        widgets['license_expiry'] = DateInput()

    profile_inlineformset = inlineformset_factory(User, sub, fields=fields, widgets=widgets, can_delete=False)
    formset = profile_inlineformset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = profile_inlineformset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = profile_inlineformset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    #checking for changes that need verification
                    changes = formset[0].changed_data

                    #dropping items that driver can change w/out verification
                    if group is "driver":
                        if changes.count('phone_num') > 0:
                            changes.pop(changes.index('phone_num'))

                        if len(changes) > 0:
                            user.driver.verified = False

                    formset.save()
                    return HttpResponseRedirect('/povreg/profile_view')

        return render(request, "povreg/profile_update.html", context={
            "profile": profile,
            "noodle_form": user_form,
            "formset": formset,
            "group": group,
        })
    else:
        raise PermissionDenied


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
