FROM public.ecr.aws/docker/library/node:24-slim AS client-builder

ARG APP_HOME=/srv
WORKDIR ${APP_HOME}

COPY ./package.json ${APP_HOME}
COPY ./package-lock.json ${APP_HOME}
RUN npm install && npm cache clean --force
COPY . ${APP_HOME}
RUN npm run build


FROM public.ecr.aws/amazonlinux/amazonlinux:latest

ARG APP_HOME=/srv
ENV APP_HOME=${APP_HOME}

ARG GIT_COMMIT=unspecified
ENV GIT_COMMIT=${GIT_COMMIT}

ENV PATH=/usr/local/bin:$PATH \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    WEB_CONCURRENCY=2 \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    DJANGO_ADMIN_URL=admin \
    # DJANGO_SECRET_KEY="0^m-))l!x+bv0drsv6klj&*85cgcfo5%ru!aj#f6h@-w!l2o#(" \
    DJANGO_SECURE_SSL_REDIRECT=False \
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=False \
    DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_EMAIL=test-dev-admin@mtahq.org \
    DATABASE_URL=sqlite:///${APP_HOME}/data/db.sqlite3
    # DJANGO_SUPERUSER_PASSWORD=test1234

EXPOSE 8000

WORKDIR ${APP_HOME}

# RUN dnf --nogpgcheck --setopt=sslverify=false update ca-certificates && update-ca-trust extract

RUN dnf --nogpgcheck --setopt=sslverify=false update -y \
    && dnf --nogpgcheck --setopt=sslverify=false install -y \
        # python3.13-devel \
        python3.13 \
        python3.13-pip \
    && python3.13 -m pip install pip --upgrade \
    && dnf -y clean all

RUN ln -s /usr/bin/python3.13 /usr/bin/python
RUN ln -s /usr/bin/pip3.13 /usr/bin/pip

# COPY . ${APP_HOME}
COPY --from=client-builder ${APP_HOME} ${APP_HOME}

RUN pip3 install --no-cache-dir -r requirements/production.txt

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

RUN mkdir -p ${APP_HOME}/core/media
RUN mkdir -p ${APP_HOME}/data
# VOLUME core_django_data:${APP_HOME}/data
# VOLUME production_django_media:/app/core/media

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ENTRYPOINT ["/entrypoint"]
CMD [ "/start" ]

# CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--chdir=/srv"]
