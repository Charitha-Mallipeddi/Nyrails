from django.urls import path

from . import views

app_name = "refunds"

urlpatterns = [
    path("", views.refund_list, name="list"),
    path("analytics", views.analytics, name="analytics"),
    path("create/", views.refund_create, name="create"),
    path("<int:pk>/edit/", views.refund_edit, name="edit"),
    path("<int:pk>/denial-letter/pdf/", views.generate_denial_letter_pdf, name="denial_letter_pdf"),
    path("denial-email", views.denial_mail, name="denial_mail"),
    path("justification-autocomplete/", views.denial_justification_autocomplete_view, name="justification-autocomplete"),
    path("refund-reason-autocomplete/", views.refund_reason_autocomplete_view, name="refund-reason-autocomplete"),
    path("notified-by-autocomplete/", views.notified_by_autocomplete_view, name="notified-by-autocomplete"),
    path("customer-notified-by-autocomplete/", views.customer_notified_by_autocomplete_view, name="customer-notified-by-autocomplete"),
    path("routing-status-autocomplete/", views.routing_status_autocomplete_view, name="routing-status-autocomplete"),
    path("purchase-type-autocomplete/", views.purchase_type_autocomplete_view, name="purchase-type-autocomplete"),
    path("sent-for-processing-autocomplete/", views.sent_for_processing_autocomplete_view, name="sent-for-processing-autocomplete"),
    path("refund-pay-type-autocomplete/", views.refund_pay_type_autocomplete_view, name="refund-pay-type-autocomplete"),
]
