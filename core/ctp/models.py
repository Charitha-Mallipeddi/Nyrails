import secrets
import string

from django.conf import settings
from django.db import models
from django.utils import timezone

from core.contrib.db.fields import DecimalIntField


def generate_sequence_number():
    """Generates a 12-digit random number string."""
    return "".join(secrets.choice(string.digits) for x in range(12))


class Ctp(models.Model):
    sequence_number = models.CharField(
        max_length=20, unique=True, help_text="Sequence#", blank=True
    )

    ROUTING_STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("re-open", "Re-Open"),
        ("re-closed", "Re-Closed"),
    ]
    routing_status = models.CharField(
        max_length=15, choices=ROUTING_STATUS_CHOICES, default="open"
    )
    open_date = models.DateTimeField(null=True, blank=True)

    DEPARTMENT_CHOICES = [
        ("finance", "Finance"),
        ("customer_service", "Customer Service"),
        ("operations", "Operations"),
        ("legal", "Legal"),
        ("field_ops", "Field Operations"),
        ("executive", "Executive Management"),
    ]

    TITLE_CHOICES = [("mr", "Mr"), ("mrs", "Mrs")]

    from_dept = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ctp_from",
    )

    route_to_dept = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    route_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ctp_routed_to",
    )

    originally_entered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ctp_entered",
    )
    date_entered = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="ctp_updated",
    )
    update_date = models.DateTimeField(auto_now=True)

    # Personal Information
    title = models.CharField(max_length=20, blank=True, choices=TITLE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    IDENTIFICATION_TYPE_CHOICES = [
        ("normal", "Normal"),
    ]

    identification_type = models.CharField(
        max_length=200, choices=IDENTIFICATION_TYPE_CHOICES
    )
    address_1 = models.CharField(max_length=255)
    lic_number = models.CharField(max_length=100, blank=True)
    dob = models.DateField(blank=True, null=True)
    address_2 = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="United States")
    intl_zip = models.CharField(max_length=20, blank=True)
    day_phone = models.CharField(max_length=20, blank=True)
    evening_phone = models.CharField(max_length=20, blank=True)
    extension = models.CharField(max_length=10, blank=True)
    email = models.EmailField(blank=True)
    invalid_id = models.BooleanField(blank=True)
    invalid_address = models.BooleanField(blank=True)

    # Commit to pay information
    waived = models.BooleanField()

    WAIVED_REASONS = [
        ("approved_by_cust_engagement", "Approved By Cust Engagement"),
        ("approved_by_cust_engagement", "Approved By Revenue Engagement"),
    ]

    waived_reason = models.CharField(max_length=100, choices=WAIVED_REASONS, blank=True)
    train_num = models.CharField(max_length=100)

    TICKET_TYPE_CHOICES = [
        ("peak", "Peak"),
        ("peak_half", "Peak Half"),
        ("off_peak", "Off Peak"),
        ("military", "Military"),
        ("ten_trip_peak", "Ten Trip Peak"),
        ("ten_trip_off_peak", "Ten Trip Off Peak"),
        ("ten_trip_senior", "Ten Trip Senior"),
        ("family", "Family"),
        ("belmont", "Belmont"),
        ("city_ticket", "City Ticket"),
        ("special_event_rail", "Special Event Rail"),
        ("hampton_reserve_seat", "Hampton Reserve - Seat"),
        ("lost_and_found", "Lost & Found"),
        ("mail_and_ride", "Mail & Ride"),
        ("credit_overcharge", "Credit Overcharge"),
        ("no_ticket_type_defined", "No Ticket Type Defined"),
        ("uniticket_nyct", "UniTicket NYCT"),
        ("uniticket_long_beach", "UniTicket Long Beach"),
        ("uniticket_nice_bus", "UniTicket NICE Bus"),
        ("uniticket_mta_bus", "UniTicket MTA Bus"),
        ("overpayment_school", "Overpayment (School)"),
        ("ny_metro_card", "NY Metro Card"),
        ("nyct_metro_card", "NYCT Metro Card"),
        ("nyc_ui_getaway_vendors", "NYC/UI Getaway Vendors"),
        ("tsm_web_unticket_subsidy", "TSM/Web UniTicket Subsidy"),
        ("mail_and_ride_unlimited", "Mail & Ride Unlimited"),
        ("refund_processing_fee", "Refund Processing Fee"),
    ]

    ticket_type = models.CharField(max_length=100, choices=TICKET_TYPE_CHOICES)
    invoice_date = models.DateField()
    bill_num = models.CharField(max_length=100)

    LINE_CHOICES = [
        ("summary_branch", "Summary Branch"),
        ("port_jefferson_branch", "Port Jefferson Branch"),
        ("oyster_bay_branch", "Oyster Bay Branch"),
        ("port_washington_branch", "Port Washington Branch"),
        ("hempstead_branch", "Hempstead Branch"),
        ("babylon_branch", "Babylon Branch"),
        ("far_rockaway_branch", "Far Rockaway Branch"),
        ("west_hempstead_branch", "West Hempstead Branch"),
        ("city_zone_branch", "City Zone Branch"),
        ("long_beach_branch", "Long Beach Branch"),
        ("ronkonkoma_branch", "Ronkonkoma Branch"),
        ("hempstead_branch", "Hempstead Branch"),
        ("greenport_branch", "Greenport Branch"),
    ]

    line = models.CharField(max_length=100, choices=LINE_CHOICES)

    STATION_CHOICES = [
        ("STN01", "Central Station"),
        ("STN02", "North Station"),
        ("STN03", "East Station"),
        ("STN04", "West Station"),
    ]

    from_station = models.CharField(max_length=100, choices=STATION_CHOICES)
    to_station = models.CharField(max_length=100, choices=STATION_CHOICES)

    amount_due = DecimalIntField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = DecimalIntField(max_digits=10, decimal_places=2, default=0.00)
    balance = DecimalIntField(max_digits=10, decimal_places=2, default=0.00)

    # CTP Letters
    letter_print_batch = models.CharField(max_length=100, blank=True)
    letter_sent_date = models.DateField(blank=True, null=True)
    letter_generated_date = models.DateField(blank=True, null=True)

    # Payment Information
    PAY_TYPE_CHOICES = [
        ("cash", "Cash"),
        ("check", "Check"),
        ("credit", "Credit"),
        ("debit", "Debit"),
        ("exchange", "Exchange"),
        ("voucher", "Voucher"),
        ("multi_payment", "Multi-Payment"),
        ("tr_check", "TR Check"),
        ("web", "Web"),
        ("tsi_collection", "TSI Collection"),
        ("deducted_from_refund", "Deducted from refund"),
    ]

    payment_type = models.CharField(max_length=50, choices=PAY_TYPE_CHOICES)
    check_number = models.CharField(max_length=50, blank=True)
    date_of_payment = models.DateField(blank=True, null=True)
    is_manual_payment = models.BooleanField(default=False)

    # Conductor Input
    NON_REASON_PAYMENT_CHOICES = [("forgot_money", "Forgot Money")]

    reason_for_non_payment = models.CharField(
        max_length=100, choices=NON_REASON_PAYMENT_CHOICES
    )
    remarks = models.TextField(blank=True)
    conductor_emp_num = models.CharField(max_length=100)
    conductor_name = models.CharField(max_length=100, blank=True)
    tim_num = models.CharField(max_length=100, blank=True)
    shift_id = models.CharField(max_length=100, blank=True)

    # Clerk Input
    clerk_remarks = models.TextField(blank=True)

    def __str__(self):
        return f"CTP {self.sequence_number} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        user = None

        if not self.pk and user is not None:
            self.originally_entered_by = user
            self.date_entered = timezone.now()

        if user is not None:
            # TODO : check for the old status and new status and then update the
            # status_changed_by
            self.status_changed_by = user
            self.status_date = timezone.now()
            self.last_updated_by = user

        if not self.sequence_number:
            while True:
                new_seq = generate_sequence_number()
                if not Ctp.objects.filter(sequence_number=new_seq).exists():
                    self.sequence_number = new_seq
                    break

        super().save(*args, **kwargs)
