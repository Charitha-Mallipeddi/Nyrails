import logging

logger = logging.getLogger(__name__)


class SalesForceClient:
    """Connection manager for SalesForce API."""

    _connection = None

    @classmethod
    def get_connection(cls):
        """Return an active SalesForce connection, creating one if needed."""
        if cls._connection is not None:
            return cls._connection

        # TODO: uncomment when simple_salesforce is installed and .env configured
        # from django.conf import settings
        # from simple_salesforce import Salesforce
        #
        # try:
        #     cls._connection = Salesforce(
        #         username=settings.SF_USERNAME,
        #         password=settings.SF_PASSWORD,
        #         security_token=settings.SF_SECURITY_TOKEN,
        #         domain=settings.SF_DOMAIN,
        #     )
        #     logger.info("SalesForce connection established")
        # except Exception as e:
        #     logger.error(f"SalesForce connection failed: {e}")
        #     cls._connection = None

        return cls._connection

    @classmethod
    def reset(cls):
        """Reset the connection."""
        cls._connection = None

    @classmethod
    def is_configured(cls):
        """Check if SalesForce credentials are available in settings."""
        try:
            from django.conf import settings
            return all([
                getattr(settings, "SF_USERNAME", None),
                getattr(settings, "SF_PASSWORD", None),
                getattr(settings, "SF_SECURITY_TOKEN", None),
                getattr(settings, "SF_DOMAIN", None),
            ])
        except Exception:
            return False
