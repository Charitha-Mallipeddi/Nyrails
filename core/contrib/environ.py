from urllib.parse import unquote_plus

from environ import Env as EnvBase


class Env(EnvBase):
    def db_url(
        self,
        var=EnvBase.DEFAULT_DATABASE_ENV,
        default=EnvBase.NOTSET,
        engine=None,
    ):
        config = super().db_url(var, default, engine)
        if config["ENGINE"] == "django.db.backends.oracle":
            if "HOST" in config and config["HOST"] == "":
                del config["HOST"]
                config["NAME"] = unquote_plus(unquote_plus(config["NAME"]))
        return config

    db = db_url
