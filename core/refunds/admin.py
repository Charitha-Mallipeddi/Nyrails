from django.contrib import admin

from core.refunds.models import (
    Refund,
    NotifiedBy,
    CustomerNotifiedBy,
    RefundJustification,
    RefundReason,
)

admin.site.register(Refund)
admin.site.register(CustomerNotifiedBy)
admin.site.register(NotifiedBy)
admin.site.register(RefundJustification)
admin.site.register(RefundReason)
