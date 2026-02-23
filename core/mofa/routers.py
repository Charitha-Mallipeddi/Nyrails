# ruff: noqa: SLF001


class MofaRouter:
    def db_for_read(self, model, **hints):
        if hasattr(model, "_meta") and model._meta.app_label == "mofa":
            return "mofa"
        return None

    def db_for_write(self, model, **hints):
        if hasattr(model, "_meta") and model._meta.app_label == "mofa":
            return "mofa"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both objects are in the 'mofa' app.
        if (
            hasattr(obj1, "_meta")
            and hasattr(obj2, "_meta")
            and obj1._meta.app_label == "mofa"
            and obj2._meta.app_label == "mofa"
        ):
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Make sure the 'myapp app only appears in the 'other_db' database.
        if app_label == "mofa":
            return db == "mofa"

        return None
