from django.db.models import IntegerChoices, TextChoices


class RefundPayTypes(IntegerChoices):
    CASH = 0, "Cash"
    CHECK = 1, "Check"
    CREDIT = 2, "Credit"
    DEBIT = 3, "Debit"
    EXCHANGE = 4, "Exchange"
    VOUCHER = 5, "Voucher"
    MULTI_PAYMENT = 6, "Multi-Payment"
    TR_CHECK = 7, "TR Check"
    WEB = 8, "Web"
    TSI_COLLECTION = 9, "TSI Collection"
    DEDUCTED_FROM_REFUND = 10, "Deducted from refund"


class CreditCardTypes(IntegerChoices):
    DISCOVER = 0, "Discover"
    MASTERCARD = 1, "MasterCard"
    VISA = 2, "Visa"
    AMERICAN = 3, "American Express"


class RoutingStatusChoices(TextChoices):
    NONE = "", "---"
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"
    RE_OPEN = "re-open", "Re-Open"
    RE_CLOSED = "re-closed", "Re-Closed"


class PurchaseTypeChoices(TextChoices):
    NONE = "", "---"
    TSS_REFUND = "tss_refund", "TSS Refund"
    ETIX_REFUND = "etix_refund", "eTix Refund"
    GROUP_SALES_REFUND = "group_sales_refund", "Group Sales Refund"
    OBTIMS = "obtims", "OBTIMS"
    STIMS_MANUAL = "stims_manual", "STIMS,Manual"
    HAMPTON_HOLIDAY = "hampton_holiday", "Hampton/Holiday"
    MAIL_RIDE_REFUNDS = "mail_ride_refunds", "MailRide Refunds"


class SentForProcessingChoices(TextChoices):
    NONE = "", "---"
    ACCOUNTING = "accounting", "Accounting"
    REVENUE = "revenue", "Revenue"


class CaseType(TextChoices):
    REFUND = "refund", "Refund"
    CTP = "ctp", "CTP"


class CaseTicketStatus(TextChoices):
    CREATED = "created", "Created"
    DETAIL_CHECKED = "detail_checked", "Detail Checked"
    DETAIL_FAIL = "detail_fail", "Detail Failed"
    SCAN_CHECKED = "scan_checked", "Scan Checked"
    SCAN_FAIL = "scan_fail", "Scan Failed"
    RESEARCH_PASS = "research_pass", "Research Passed"
    RESEARCH_FAIL = "research_fail", "Research Failed"


class PaymentType(TextChoices):
    CASH = "cash", "Cash"
    CASHLESS = "cashless", "Cashless"


class InvoiceStatus(TextChoices):
    OPEN = "open", "Open"
    PAID = "paid", "Paid"
    VOIDED = "voided", "Voided"


class CaseStatus(TextChoices):
    CLOSED = "closed", "Closed"
    IN_PROGRESS = "in_progress", "In Progress"
    RECEIVED = "received", "Received"
    RE_OPENED = "re_opened", "Re-Opened"
    WAITING = "waiting", "Waiting on Requester"


class CaseStatusDetail(TextChoices):
    AUTO_CLOSED = "auto_closed", "Auto-closed per policy"
    CLOSED_NO_RESPONSE = "closed_no_response", "Closed without Response"
    DUPLICATE = "duplicate", "Duplicate Case"
    FOLLOW_UP = "follow_up", "Follow-up Required"
    REPETITIVE = "repetitive", "Repetitive Inquiry"
    RESOLVED = "resolved", "Resolved"
    RESPONDED_CHAT = "responded_chat", "Responded via Chat"
    RESPONDED_EMAIL = "responded_email", "Responded via Email"
    RESPONDED_LETTER = "responded_letter", "Responded via Letter"
    RESPONDED_PARENT = "responded_parent", "Responded via Parent Case"
    RESPONDED_PHONE = "responded_phone", "Responded via Phone"
    RESPONDED_SOCIAL = "responded_social", "Responded via Social Media"
    RUDE_ABUSIVE = "rude_abusive", "Rude/Abusive"
    SPAM = "spam", "Spam"
    TEST = "test", "Test"
    RESEARCH_REQUIRED = "research_required", "Research Required"
    INVESTIGATION_UPDATED = "investigation_updated", "Investigation Updated"
    ON_HOLD = "on_hold", "On Hold"
    PREPARE_RESPONSE = "prepare_response", "Prepare Response"
    TO_BE_MAILED = "to_be_mailed", "To Be Mailed"
