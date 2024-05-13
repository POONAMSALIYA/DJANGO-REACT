from django.db import models

# Create your models here.
import datetime
from django.db import models
from customer.models import Customer
from properties.models import Property
import uuid

_property = property


class Booking(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="bookings"
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, related_name="bookings")

    uuid = models.UUIDField(default = uuid.uuid4, editable=False, unique=True)
    door_key = models.CharField(max_length=20, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    checkin_time = models.TimeField()
    checkout_time = models.TimeField()
    deposit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    status = models.TextField(
        choices=(
            ("UPCOMING", "UPCOMING"),
            ("ACTIVE", "ACTIVE"),
            ("AWAITING_CLEANING", "AWAITING_CLEANING"),
            ("COMPLETED", "COMPLETED"),
            ("CANCELLED", "CANCELLED"),
        ),
        default="UPCOMING",
    )
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @_property
    def property_details(self):
        try:
            booking_property = self.property
            return {
                "property_gmaps_link": booking_property.gmaps_link,
                "property_name": booking_property.name,
                "apt_number": booking_property.apt_number,
                "neighbourhood": booking_property.neighbourhood,
                "building_name": booking_property.building_name
            }
        except:
            return None

    @_property
    def entry_key(self):
        if self.status == "ACTIVE":
            return self.door_key
        else:
            return None
        
    @_property
    def feedback_submitted(self):
        feed = Feedback.objects.filter(booking= self.id)
        if feed:
            return True
        else:
            return False

    @_property
    def customer_details(self):
        try:
            customer =  self.customer
            return {
                "customer_name": customer.name,
                "customer_phone": customer.contact,
            }
        except:
            return None
        

    @_property
    def late_request_exist(self):
        late_request = LateCheckOutRequest.objects.filter(booking_id = self.id)
        if late_request:
            return True
        return False
    

    @_property
    def payment_details(self):
        try:
            payment = self.payment
            return {
                "intent_id": payment.intent_id,
                "paid": float(payment.paid),
                "refunded": float(payment.refunded),
                "status": payment.status,
                "created_on": payment.created_on,
                "last_modified": payment.last_modified,
            }
        except:
            return None
        
    @_property
    def job_details(self):
        try:
            job = self.jobs.first()
            return {
                "id": job.id,
                "status": job.status,
            }
        except:
            return None


class LateCheckOutRequest(models.Model):

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="check_out_request")
    original_end_date = models.DateField()
    requested_end_date = models.DateField()
    original_checkout_time = models.TimeField()
    requested_checkout_time = models.TimeField()
    status = models.TextField(
        choices=(
            ("REQUESTED", "REQUESTED"),
            ("AWAITING_PARTNER_CLEARANCE", "AWAITING_PARTNER_CLEARANCE"),
            ("DECLINED", "DECLINED"),
            ("APPROVED", "APPROVED"),
        ),
        default="REQUESTED",
    )
    job_status = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


class Feedback(models.Model):
    RATINGS = (
        ("Very Satisfied", "Very Satisfied"),
        ("Satisfied", "Satisfied"),
        ("Neutral", "Neutral"),
        ("Dissatisfied", "Dissatisfied"),
        ("Very Dissatisfied", "Very Dissatisfied"),
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Average", "Average"),
        ("Poor", "Poor"),
        ("Very Poor", "Very Poor"),
    )

    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="feedbacks"
    )
    overall_satisfaction = models.CharField(max_length=20, choices=RATINGS[0:5])
    cleanliness = models.CharField(max_length=20, choices=RATINGS[5:])
    communication = models.CharField(max_length=20, choices=RATINGS[5:])
    service_quality = models.CharField(max_length=20, choices=RATINGS[5:])
    value_for_money = models.CharField(max_length=20, choices=RATINGS[5:])
    comments = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    @_property
    def property_name(self):
        return self.booking.property.name
    




