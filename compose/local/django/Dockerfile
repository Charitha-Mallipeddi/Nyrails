FROM public.ecr.aws/amazonlinux/amazonlinux:latest

ARG APP_HOME=/srv
ENV APP_HOME=${APP_HOME}

ENV PATH=/usr/local/bin:$PATH \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    DJANGO_SETTINGS_MODULE=config.settings.local \
    DJANGO_ADMIN_URL=admin \
    DJANGO_SECURE_SSL_REDIRECT=False \
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=False \
    DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_EMAIL=test-dev-admin@mtahq.org

# EXPOSE 8001

WORKDIR ${APP_HOME}

RUN dnf --setopt=sslverify=false install -y ca-certificates && update-ca-trust force-enable && update-ca-trust extract

RUN dnf --nogpgcheck --setopt=sslverify=false update -y \
    && dnf --nogpgcheck --setopt=sslverify=false install -y \
        python3.13 \
        python3.13-pip \
        tzdata \
        lsof \
        shadow-utils \
        sudo \
        tar \
        git \
        graphviz \
        make \
    && python3.13 -m pip install pip --upgrade \
    && dnf -y clean all

RUN ln -s /usr/bin/python3.13 /usr/bin/python
RUN ln -s /usr/bin/pip3.13 /usr/bin/pip

COPY . ${APP_HOME}

RUN pip3 install --no-cache-dir -r requirements/local.txt

# Create devcontainer user and add it to sudoers
RUN /usr/sbin/groupadd --gid 1000 dev-user
RUN /usr/sbin/useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user
RUN echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user
RUN chmod 0440 /etc/sudoers.d/dev-user

ENV PATH="/${APP_HOME}/.venv/bin:/usr/local/bin:$PATH"
ENV PYTHONPATH="${APP_HOME}/.venv/lib/python3.13/site-packages:$PYTHONPATH"

# RUN GIT_SSL_NO_VERIFY=true pre-commit install-hooks -c ${APP_HOME}/.pre-commit-config.yaml

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ENTRYPOINT ["/entrypoint"]
