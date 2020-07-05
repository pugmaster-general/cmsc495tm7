from django.db import models
from django.urls import reverse  # used to general URLs by reersing the URL patterns
from django.contrib.auth.models import User
from datetime import date

import uuid  # required for unique book instances
# Create your models here.


class Driver(models.Model):
    """model to represent a driver"""
    #driver id, might not need to declare a pk

    # driver name
    first_name = models.TextField(max_length=30, help_text='driver\'s first name')
    last_name = models.TextField(max_length=30, help_text='driver\'s last name')

    # driver license number
    license_num = models.TextField(max_length=20, help_text='driver\'s license number', unique=True)
    license_expiry = models.DateField(help_text='driver\'s license expiration date')

    # state
    state = models.TextField(max_length=30, help_text="State for the driver's license", blank=True)
    country = models.TextField(max_length=30, help_text="Country for the driver's license")

    phone_num = models.TextField(max_length=12, help_text="the driver's phone number")

    verified = models.BooleanField(help_text="whether driver data is verified by admin", default=False)

    #can be blank and null for now, for the data
    dob = models.DateField(help_text="driver's date of birth", blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True,
                                help_text="This is the user account that corresponds to the driver")

    @property
    def is_expired(self):
        if self.license_expiry < date.today():
            return True
        return False

    def __str__(self):
        """string for representing the Driver object"""
        return str(self.last_name + ', ' + self.first_name)

    def get_absolute_url(self):
        """returns url to access a detail record of the driver"""
        return reverse('driver-detail', args=[str(self.id)])


class Car(models.Model):
    """Model to represent a car"""

    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, blank=True, null=True)
    insurance = models.OneToOneField('Insurance', on_delete=models.SET_NULL, blank=True, null=True)
    v_make = models.TextField(max_length=30, help_text="vehicle's make")
    is_commercial = models.BooleanField(default=False,
                                        help_text="true if commercial vehicle, false if private. default is false")
    v_plate = models.TextField(max_length=10, help_text="vehicle's license plate")
    owner = models.TextField(max_length=30, help_text="vehicle's owner")
    REPORTED_STATUS = {
        ('st', 'stolen'),
        ('go', 'good'),
    }
    status = models.TextField(choices=REPORTED_STATUS, default='go', help_text="vehicle's current reported status")

    #can be blank and null for now, for the data
    registration = models.TextField(max_length=30, help_text="vehicle registration", null=True, blank=True)
    v_model = models.TextField(max_length=30, help_text="vehicle's model", null=True, blank=True)
    v_state = models.TextField(max_length=30, help_text="vehicle's state of registration", null=True, blank=True)
    v_country = models.TextField(max_length=30, help_text="vehicle's country of registration", null=True, blank=True)

    @property
    def is_insured(self):
        if self.insurance is None:
            return False
        elif self.insurance.is_expired:
            return False
        else:
            return True

    def __str__(self):
        """string for representing the car"""
        if (self.v_model is None) or (self.v_model == ""):
            return str(self.v_make + ": " + self.v_plate)

        else:
            return str(self.v_model + ", " + self.v_make + ": " + self.v_plate)

    def get_absolute_url(self):
        """:returns url to access a detailed record of the car"""
        return reverse('car-detail', args=[str(self.id)])

    class Meta:
        unique_together = ("v_plate", "v_state", "v_country")


class Insurance(models.Model):
    """model for each car's insurance"""
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, blank=True, null=True)

    company = models.TextField(max_length=200, help_text="Company issuing insurance")
    policy_num = models.TextField(max_length=30, unique=True, help_text="Insurance Policy number")
    expiry = models.DateField(help_text="Insurance expiration date")
    coverage_type = models.TextField(max_length=30, help_text="type of insurance coverage")
    STATUS_TYPE = {
        ('ex', 'Expired'),
        ('su', 'Suspended'),
        ('ac', 'Active'),
    }
    status = models.TextField(choices=STATUS_TYPE, default='ac', help_text="vehicle's current insurance status")

    @property
    def is_expired(self):
        if self.expiry and date.today() > self.expiry:
            self.status = 'ex'
            return True
        return False

    def get_absolute_url(self):
        """:returns url to access a detailed record of the insurance"""
        return reverse('insurance-detail', args=[str(self.id)])

    def __str__(self):
        """:returns string for representing the insurance policy"""
        return str(self.driver.__str__() + "'s policy for " + self.car.__str__())


class Officer(models.Model):
    """model for each officer's details"""
    badge_num = models.TextField(max_length=30, help_text="officer's badge number", unique=True)
    unit = models.TextField(max_length=30, help_text="officer's division, district, or unit")
    region = models.TextField(max_length=30, help_text="officer's operating region (country, state, province)")
    id_num = models.TextField(max_length=30, help_text="officer's personal ID number", unique=True)

    verified = models.BooleanField(help_text="whether driver data is verified by admin", default=False)

    #can be blank and null for now, for the data
    first_name = models.TextField(max_length=30, help_text="officer's first name", blank=True, null=True)
    last_name = models.TextField(max_length=30, help_text="officer's last name", blank=True, null=True)
    rank = models.TextField(max_length=30, help_text="officer's current rank", blank=True, null=True)

    #using text field for now, may update to photo later
    id_photo = models.TextField(help_text="upload of the officer's photo ID", blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
                                help_text="this is the user account connected to this officer")

    def get_absolute_url(self):
        """:returns url to access a detailed record of the officer"""
        return reverse('officer-detail', args=[str(self.id)])

    def __str__(self):
        """:returns string for representing the officer"""
        officer_str = str()
        if not(self.rank is None or self.rank==""):
            officer_str+=self.rank + " "

        if not(self.last_name is None or self.last_name==""):
            officer_str+=self.last_name + " "

        if not(self.first_name is None or self.first_name==""):
            officer_str+=self.first_name + " "

        if officer_str=="":
            officer_str = f"Officer {self.id}"
        else:
            officer_str = officer_str.strip()

        return officer_str
