from django.db import models


class TicketTypeSummary(models.IntegerChoices):
    NO = 0, "is not"
    YES = 1, "is (Sales summary relevant)"


class TicketTypeGenerInput(models.IntegerChoices):
    NO = 0, "Application will not ask for customer gender"
    YES = 1, "Application will ask"


class SalesPacketsSendOnlEvt(models.IntegerChoices):
    NO = 0, "no event is send"
    YES = 1, "an online event is send by selling this packet"
