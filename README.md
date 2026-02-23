<img src="core/static/images/top_logo_bw.svg" width="500px"/>

# RFC-C.O.R.E

Centralized Office Revenue Engine, written in django to aggregate and centralize all legacy applications for the MTA

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [RFC-C.O.R.E](#rfc-core)
  - [Download and Installation](#download-and-installation)
  - [Docker Compose Setup](#docker-compose-setup)
    - [Install Docker](#install-docker)
    - [Docker Container Default Settings](#docker-container-default-settings)
    - [Tips & Tricks](#tips--tricks)
  - [NPM Tasks](#npm-tasks)
  - [Basic commands / Manual Setup](#basic-commands--manual-setup)
    - [Setup python Virtual Environment](#setup-python-virtual-environment)
    - [Setting Up Your Users](#setting-up-your-users)
    - [Type checks](#type-checks)
    - [Test coverage](#test-coverage)
      - [Running tests with pytest](#running-tests-with-pytest)
    - [Live reloading and Sass CSS compilation](#live-reloading-and-sass-css-compilation)
      - [Live reloading and Sass CSS compilation](#live-reloading-and-sass-css-compilation-1)

<!-- /code_chunk_output -->

## Download and Installation

First clone the latest version of the repository, and switch branch to develop

```bash
git clone https://github.com/MTA-RFC/RFC-CORE.git
git switch origin/develop
```

Extra Git configurations

```bash
git config --global http.github.com.sslVerify false
git config —global user.name “Last, First”
git config --global user.email “user@mtahq.org”
```

Make sure you have [Docker/Compose Installed](#install-docker)

```bash
cd core
touch .env
docker compose up django -d
```

This will initialize all the required components to develop using docker, if you want to execute some manual command. Go into the respective docker container using ***Docker Desktop > Containers > Select Container > Exec***

Open vsCode then install the [Dev Container](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.

After the extension is installed, try to open the ***CORE** folder.

Once opened vsCode will ask you to Reopen in Container, if not asked then go to***Ctrl+Command+P > Dev Container: Reopen in Container**

The vsCode window will reopen within the container, and start running initial setup scripts. It will prompt to install recommended extensions.

After a few seconds go to the ***Run and Debug** screen and start ***Python Debugger: Django***

This wills start django and open port 8001

Open your browser to [http://127.0.0.1:8001/](http://127.0.0.1:8001/)

## Docker Compose Setup

The docker compose setup has a few tools integrated for future development

- ***Django*** (Python)
- ***Node (ViteJS / TypeScript / Sass)*** - Helps to listen for .ts, .scss, .css files to get compiled and minified.
- ***MailTrap*** - Fake SMTP server to capture any emails sent from the application.
- ***OracleDB*** - Single local instance of Oracle Database Server
- ***DynamoDB*** - AWS DynamoDB server

### Install Docker

Please follow the official instruction to [Install Docker on Mac](https://docs.docker.com/desktop/setup/install/mac-install/)

### Docker Container Default Settings

Most of this variables and definitions are in ***docker-compose.yaml***, if you require to make some modifications please discuss it with all the other developers before committing any changes to the docker compose file.

| service | name | value | description |
|---|---|---|---|
|django|ports|"8001:8001"<br/> "5678:5678"|8001 is the default django http port, 5678 is the debugPy listening port to attach vsCode for debug|
|django|env_file|./.envs/.local/.django<br/>./.envs/.local/.oracle<br/>./.env| All default environment variables for development, the last .env file was introduced to overwrite all default values per developer if necessary. |
|mailpit|ports|"8025:8025"<br/>"1025:1025"|8025 Web UI, 1025 SMTP|
|dynamodb|ports|"8000:8000"|Gateway|
|node|ports|"5173:5173"|Asset gateway|

### Tips & Tricks

If you want to start all services but want to have some local control of django while developing, do the following:

1. This will spin all the containers in DAEMON mode, then we will stop django manually

```bash
docker compose up -d
docker compose stop django
```

1. After django is stopped, we can start it again in local mode.

```bash
docker compose up django
```

this lets you see what is getting printed by the django development console in your local terminal, instead of logging everything into docker container logs.

## NPM Tasks

These are the task and explanation of what they do to simplify execution of common jobs.
e.g. how to execute a task

```bash
npm run <task_name>
```

|name|description|
|---|---|
|build|Generates the final static production ready .js and .css files|
|docker:build|Creates a docker image with label rfc/core ready to deploy into App Runner|
|docker:tag|Tags the previously created image to be pushed to ECR|
|docker:push|Pushes the tagged imaged to ECR|
|docker:deploy|Executes the previous three tasks (build,tag,push) in one command|
|font|Build the icont font using all .svg files found in ***./core/static/icons***|
|graph_models|Executes a django function to generate docs/core_models.png using **/models.py definitions|

## Basic commands / Manual Setup

Here are some of the basic commands if there is a need to customize or execute some manual changes.

### Setup python Virtual Environment

This configures your project to install a local version of python and make sure all the required libraries are installed locally.

- Initialize the virtual environment

```bash
python -m venv .venv
```

- Enable the virtual environment (Mac/Linux)

```shell
source .venv/bin/activate
```

Once enabled you will see in your terminal cursor `(.venv)` before your username.

- Install all dependencies

```shell
pip install -r requirements/local.txt
```

### Setting Up Your Users

To access the application locally you can create a local user using the commandline.

```shell
./manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    mypy core

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

```bash
coverage run -m pytest
coverage html
open htmlcov/index.html
```

You can execute both initial command and also add some attributes to debug

```bash
coverage run -m pytest -s -vv && coverage html
```

#### Running tests with pytest

```bash
pytest
```

### Live reloading and Sass CSS compilation

In here we need to configure NodeJs NVM for local virtual environment of Node.

```shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

after installing nvm, execute the following commands in your project directory

```shell
nvm install
nvm use
```

This will read the .nvmrc file and install the required version of nodejs for this project, then we can install all NPM required libraries

```shell
npm install
```

#### Live reloading and Sass CSS compilation

While developing and having live scss changes execute this

```shell
npm run dev
```

But for deployment execute

```shell
npm run build
```
