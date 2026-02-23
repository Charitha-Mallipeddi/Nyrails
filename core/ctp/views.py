from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CtpForm
from .models import Ctp


@login_required
def ctp_list(req: HttpRequest):
    ctps = Ctp.objects.all().order_by("-date_entered")
    return render(req, "ctp/list.html", {"ctps": ctps})

@login_required
def ctp_create(req: HttpRequest):
    if req.method == "POST":
        form = CtpForm(req.POST)

        if not form.is_valid():
            return render(req, "ctp/add.html", {"form": form})

        form.save()
        messages.success(req, "Ctp created successfully")
        return redirect("ctp:list")

    form = CtpForm()

    return render(req, "ctp/add.html", {"form": form})

@login_required
def ctp_edit(req: HttpRequest, pk: int):
    ctp = get_object_or_404(Ctp, pk=pk)

    if req.method == "POST":
        form = CtpForm(req.POST, instance=ctp)

        if not form.is_valid():
            return render(req, "ctp/edit.html", {"form": form})

        form.save()
        messages.success(req, "Ctp updated successfully")
        return redirect("ctp:list")

    form = CtpForm(instance=ctp)

    return render(req, "ctp/edit.html", {"form": form})
