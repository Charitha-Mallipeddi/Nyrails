from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest
from import_export.admin import ImportExportActionModelAdmin
from import_export.resources import ModelResource

from .models import (
    Company,
    ConnectingService,
    Country,
    Department,
    DeviceClass,
    Routes,
    Status,
    TariffVersions,
    TVMStation,
)


class AuditBaseModelAdmin(admin.ModelAdmin):
    def save_model(
        self, request: HttpRequest, obj: Any, form: Any, change: Any
    ) -> None:
        if change:
            obj.user_change = request.user
        else:
            obj.user_new = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Status)
class AdminStatusModel(AuditBaseModelAdmin):
    fields = ("description", "valid", "user_change", "user_new")
    readonly_fields = ("user_change", "user_new")
    list_display = ("description", "user_new", "time_new", "user_change", "time_change")


@admin.register(Department)
class AdminDepartmentModel(AuditBaseModelAdmin):
    fields = ("description", "valid", "user_change", "user_new")
    readonly_fields = ("user_change", "user_new")
    list_display = ("description", "user_new", "time_new", "user_change", "time_change")


@admin.register(Country)
class AdminCountryModel(AuditBaseModelAdmin):
    fields = ("description", "code", "valid", "user_change", "user_new")
    readonly_fields = ("user_change", "user_new")
    list_display = ("description", "user_new", "time_new", "user_change", "time_change")


@admin.register(ConnectingService)
class AdminConnectionServiceModel(AuditBaseModelAdmin):
    fields = ("description", "user_change", "user_new")
    readonly_fields = ("user_change", "user_new")
    list_display = ("description", "user_new", "time_new", "user_change", "time_change")


class AdminCompanyModelResource(ModelResource):
    class Meta:
        model = Company
        import_id_fields = ("code",)
        fields = ("code", "name", "short_name")


@admin.register(Company)
class AdminCompany(ImportExportActionModelAdmin):
    list_display = ("company_id", "name", "short_name", "time_change", "time_new")
    resource_class = AdminCompanyModelResource
    search_fields = ["pk", "name", "short_name"]
    ordering = ["name"]
    readonly_fields = ("time_change", "time_new")


@admin.register(Routes)
class AdminRoutes(admin.ModelAdmin):
    list_display = ("route_id", "description", "time_change", "time_new")
    search_fields = ["pk", "description"]
    ordering = ["description"]
    readonly_fields = ("time_change", "time_new")


@admin.register(TariffVersions)
class AdminTariffVersions(admin.ModelAdmin):
    list_display = (
        "version_id",
        "description",
        "rail_road",
        "validity_start_time",
        "validity_end_time",
    )
    search_fields = ["version_id", "description"]
    ordering = ["description"]

    readonly_fields = ("time_change", "time_new")
    autocomplete_fields = ["rail_road"]


@admin.register(DeviceClass)
class AdminDeviceClass(admin.ModelAdmin):
    list_display = (
        "device_class_id",
        "description",
        "device_class_type",
        "user_new",
        "time_new",
        "user_change",
        "time_change",
    )
    search_fields = ["device_class_id", "description"]
    ordering = ["description"]
    readonly_fields = ("time_change", "time_new", "user_change", "user_new")


@admin.register(TVMStation)
class AdminTVMStation(admin.ModelAdmin):
    list_display = (
        "station_id",
        "company",
        "name",
        "name_long",
        "name_short",
        "town",
    )
    search_fields = ["station_id", "name"]
    ordering = ["name"]
    readonly_fields = ("time_change", "time_new", "user_change", "user_new")
    autocomplete_fields = ["company"]
