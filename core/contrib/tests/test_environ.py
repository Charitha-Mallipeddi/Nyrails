from core.contrib.environ import Env


class TestEnvironEnv:
    env: Env

    def setup_method(self, method):
        self.env = Env()

    def test_db_url_1(self):
        self.env.ENVIRON["DATABASE_URL"] = (
            "oracle://user:password@localhost%3A1521%2FFREEPDB1"
        )
        conf = self.env.db_url("DATABASE_URL")
        assert conf["ENGINE"] == "django.db.backends.oracle"
        assert conf["NAME"] == "localhost:1521/FREEPDB1"
        assert conf["USER"] == "user"
        assert conf["PASSWORD"] == "password"  # noqa: S105
        assert "HOST" not in conf
