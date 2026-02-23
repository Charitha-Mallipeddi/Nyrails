from django.conf import settings


def base_settings(request):
    """Expose some settings from base settings in templates."""
    return {
        "GIT_COMMIT": settings.GIT_COMMIT,
    }
