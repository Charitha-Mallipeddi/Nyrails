from django.db import models


class TicketFormType(models.TextChoices):
    PAPER = "paperticket", "Ticket"
    ETIX = "eticket", "eTix"
