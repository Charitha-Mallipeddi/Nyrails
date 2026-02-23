# ruff: noqa: S311,T201

import datetime
import email
from random import randrange, choice

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os
User = get_user_model()

class Command(BaseCommand):
    help = "General App Hygene functions"

    def add_arguments(self, parser):
        parser.add_argument('--stations', action="store_true", default=False)

    def handle(self, *args, **options):
        if options.get("stations"):
            from core.general.models import Station
            for station in Station.objects.iterator():
                if station.line:
                    continue
                lines = station.lines.all()
                line_cnt = lines.count()
                if line_cnt == 1:
                    station.line = lines.first()
                    station.save()
                print(line_cnt)
