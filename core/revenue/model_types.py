from django.db import models


class LocationType(models.IntegerChoices):
    PHYSICAL = 0, "physical station (TvmStation)"
    ZONE = 1, "Zone"
    STATION = 2, "Station"
    CONNECTION = 3, "Connecting Service"


class ShiftChangeReasons(models.IntegerChoices):
    NONE = 0, "set before implementation"
    DAILY = 1, "auto midnight(or conf.time)daily shift"
    UPLOAD = 2, "shift change on request of upload"
    SALES = 3, "shift change by sales clerk (frontend)"
    SERVICE = 4, "shift change by service command (065)"
    CASH = 5, "shift change by cash period change"
    ONLINE = 6, "shift change by NWC - online command"
    TERMINAL = 7, "shift change by cashless terminal request"
    VERSION = 8, "shift change by version switch request"
    TRANSACTION = 9, "shift change by transaction logging"
    TEST = 10, "shift change if test mode creates shift"
    IBIS = 11, "shift change on device env. request (IBIS)"


class CashPerForceMode(models.IntegerChoices):
    NONE = 0, "no information or before implementation"
    MANUAL = 1, "change manually intitiated in service mode"
    AUTO = 2, "change automat. without manual interaction"
    FORCED = 3, "change forced by NWC command"


class CashPerTrigger(models.IntegerChoices):
    NONE = 0, "no information or before implementation"
    COMMAND = (
        1,
        "cash period triggered by command "
        "(no auto trigger conditions by cash move actions)",
    )
    COIN_VAULT = 2, "cash period triggered by coin vault removal"
    BANK_NOTE = 4, "cash period triggered by banknote vault removal"
    MAGAZINE = 8, "cash period triggered by coin magazine removal"
    COIN_VAULT2 = 16, "cash period triggered by coin vault removal"
    BANK_NOTE2 = 32, "cash period triggered by banknote vault removal"
    MAGAZINE2 = 64, "cash period triggered by coin magazine removal"
    TICKET_REM = 128, "cash period triggered by ticket stock removal"
    TICKET_INS = 256, "cash period triggered by ticket stock insert"


class CashPerCondition(models.IntegerChoices):
    NONE = 0, "no information or before implementation"
    NORMAL = 1, "trigger happened in normal service mode"
    OUTSIDE = 2, "last trigger happened outside sv mode"
    PWR_LESS = 3, "last trigger happened powerless"


class CashFlag(models.IntegerChoices):
    WITH_OUT = 0, "transaction without cash payment"
    WITH = 1, "transaction with cash payment"


class CashLessFlag(models.IntegerChoices):
    WITH_OUT = 0, "transaction without cashless payment"
    WITH = 1, "transaction with cashless payment"


class CashBookingFlag(models.IntegerChoices):
    POSITIVE = 0, "Amount is positive"
    NEGATIVE = 1, "Amount is negative"


class CancelationType(models.IntegerChoices):
    NORMAL = 0, "Normal Transaction"
    REFUND = 1, "Refund"


class CashBoxType(models.IntegerChoices):
    NORMAL = 0, "Normal booking"
    CASH = 1, "Only cash changing article, not a sale, e.g. Cash Report"


class CorrectionFlagType(models.IntegerChoices):
    VALID = 0, "record is valid, no correction record exists"
    INVALID = 1, "record is not valid, a correction record exists"


class ShiftTypes(models.IntegerChoices):
    MACHINE = 0, "a machine shift (the field VendorNo is set with the device ID)"
    EMPLOYEE = (
        1,
        "an employee shift (the field VendorNo is set with the sales clerk ID)",
    )


class AuditStatuses(models.IntegerChoices):
    NOT_NECESSARY = 1, "no audit necessary"
    TO_BE = 2, "to be audited"
    NOT_ADJUSTED = 3, "audited not adjusted"
    PASSED = 4, "passed audit"
    ADJUSTED = 5, "audited and adjusted"


class JobStates(models.IntegerChoices):
    STAND_ALONE = (
        0,
        "main shift is a complete (stand alone) shift, all related shift data "
        "belong to a single device, that means for LIRR/MNR it is a FULL-TOUR",
    )
    START_MULTI = (
        1,
        "main shift is the first main shift in a job, that means for LIRR/MNR the "
        "shift is the start of a MULTI-TOUR and contains the data for the first "
        "MINI-TOUR in the job",
    )
    MIDDLE_MULTI = (
        2,
        "main shift is a main shift in the middle of a job, that means for "
        "LIRR/MNR the shift is a middle MINI-TOUR as part of a MULTI-TOUR",
    )
    LAST_MULTI = (
        3,
        "main shift is the last main shift in a job, that means for LIRR/MNR the "
        "shift is the last MINI-TOUR of a MULTI-TOUR and contains the data for the"
        " last MINI-TOUR in the job",
    )
    START_FULL = (
        4,
        "main shift is the first main shift in a job, that means for LIRR/MNR the "
        "shift is the start of a FULL TOUR with SUSPENSION and contains the data "
        "for the first TOUR until suspended in the job",
    )
    MIDDLE_FULL = (
        5,
        "main shift is a main shift in the middle of a job, that means for "
        "LIRR/MNR the shift is a middle part of a FULL TOUR with SUSPENSION",
    )
    LAST_FULL = (
        6,
        "main shift is the last main shift in a job, that means for LIRR/MNR "
        "the shift is the last part of a FULL-TOUR with SUSPENSION",
    )


class CashLessPaymentTypes(models.IntegerChoices):
    CREDIT = 1, "Credit Card"
    DEBIT = 2, "Debit Card"
    CHECK = 4, "Check"
    VAUCHER = 8, "Voucher"
    SMARTCARD = 16, "Smart Card"
    CASH = 32, "Cash (not used in this table)"


class CashPaymentTypes(models.IntegerChoices):
    COIN = 1, "Coin"
    BILL = 2, "Bill"
    TOKEN = 3, "Token"
    CHECK = 4, "Check"
    ANY = 5, "Smart Card"


class CashPaymentChangeFlags(models.IntegerChoices):
    NONE = 0, "reserved (not used)"
    COINS_IN = 1, "coins in"
    COINS_OUT = 2, "coins out"


class SalesShiftTypes(models.IntegerChoices):
    MACHINE = 0, "a machine shift (the field VendorNo is set with the device ID)"
    EMPLOYEE = (
        1,
        "an employee shift (the field VendorNo is set with the sales clerk ID)",
    )


class BookingSelection(models.IntegerChoices):
    POSITIVE = 0, "Amount is positive"
    NEGATIVE = 1, "Amount is negative"


class ShiftIsBaseGroup(models.IntegerChoices):
    NO = 0, "Not a base group"
    YES = 1, "Base group <=> This group contains the beginning (First) shift."
