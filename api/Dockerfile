FROM python:3.12-slim

ENV APP_HOME=/opt/app
ENV APP_USER=mediapoint

# Create user and app directory
RUN groupadd -r $APP_USER && \
    useradd -r -g $APP_USER -d $APP_HOME -s /sbin/nologin -c "Docker image user" $APP_USER && \
    mkdir -p $APP_HOME /opt/alembic/versions && \
    chown -R $APP_USER:$APP_USER /opt

RUN apt update && \
    apt install -y nano build-essential cargo

USER $APP_USER
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VENV_PATH=$APP_HOME

COPY --chown=$APP_USER:$APP_USER requirements.txt requirements.txt

RUN python3 -m venv env && \
    ./env/bin/pip install --upgrade pip && \
    ./env/bin/pip install -r requirements.txt --no-cache-dir

COPY --chown=$APP_USER:$APP_USER ./docker_init /docker_init
COPY --chown=$APP_USER:$APP_USER ./alembic /opt/alembic
COPY --chown=$APP_USER:$APP_USER ./src $APP_HOME
COPY --chown=$APP_USER:$APP_USER ./alembic.docker.ini /opt/alembic.ini

RUN chmod +x /docker_init/docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker_init/docker-entrypoint.sh"]
CMD ["$0", "$@"]
