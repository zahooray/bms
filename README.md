# Project Boilerplate

## Required Changes

- `docker-compose.*.yml`: change `project_name` with actual project name.
- `project/`: change `project_name` with actual project name.
- `project/celery.py`: change `project_name` with actual project name.
- `config/settings/base.py`: change `project_name` with actual project name.
- `Makefile`: change `project_name` with actual project name.
- `config/settings/constance.py`: change `project_name` with actual project name.
- Search for `project_name` elsewhere in project and change with actual project name.

## Project First Time Setup

1. Ensure docker and docker compose are installed. [link](https://docs.docker.com/engine/install/)
2. Ensure `make` is installed. You can do it with
   ```shell script
    sudo apt install make
   ```
3. Copy the .env.example to .env
   ```shell
    cp .env.example .env
   ```
4. Build and pull the docker images
   ```shell
    make dev.build
   ```
5. Up the docker containers
   ```shell
   make dev.up
   ```
6. The project should be running now on localhost (127.0.0.1) on ports 8000
7. Navigate to http://localhost:8000 for backend
8. (To stop the project or remove the containers, run)
   ```shell
   make dev.down
   ```

## Commands

### To add a new package

- put your package name & version in appropriate `config/requirements/*.in` file
- run `make cr`

### To dumpdata and loaddata

- take dumpdata with this command:
  `python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission -e admin.LogEntry -e communications.Notification -e leads.ReadLead -e django_celery_beat.PeriodicTask -e sessions.Session --indent 2 > dump.json`
- in the dump.json, ensure `"user_permissions": []` in all `"users.user"` objects of json
- go to django shell and enter this command `python manage.py loaddata dump.json`

### (dev | stage | prod) ENV. Specific Commands

replace \* with appropriate ENV. name

- `make *.migrate` : run `makemigrations and migrate` command in django container
- `make *.build` : build containers
- `make *.test` : run `test` command in django container
- `make *.up` : start containers in attached mode
- `make *.down` : stop containers and remove networks
- `make *.dcshell` : open django container shell
- `make *.up.d` : start containers in detached mode
- `make *.collectstatic`: run `collectstatic` command in django container
- `make *.setup` : build and start containers
- `make *.restart` : firsts stop containers then start again
- `make *.logs` : attach to log console of containers
- `make *.dshell` : open django shell
- `make *.ipshell` : open django ipython shell
- `make *.psql` : run `psql` in postgres container
- `make *.rediscli` : run `redis cli` in redis container

### Common Commands

- `make cr` : compile requirements
- `make *.attach` : attach to specified container

## Pre Commit Hook Activation

1. Install pre-commit package `pip install pre-commit`
2. Install pre-commit hook `pre-commit install`

- To bypass "bandit" hook, use `# nosec` as comment on the line it gives error
- To bypass "Detect secrets" hook, add `# pragma: allowlist secret` as comment on the line it gives error
- Try to bypass hooks only via comments if necessary
- To commit without running pre-commit `git commit -m "message" --no-verify` (avoid as much as possible)


## Enable SSL with Certbot

### (stage|prod)

- update `DOMAINS` in .env file
- by default following command will run in test mode
  - `sudo ./init-letsencrypt.sh`
- once confirmed update `staging=0` in `init-letsencrypt.sh` and then run
  - `sudo ./init-letsencrypt.sh`
- uncomment lines in `certbot` and `nginx` services in `docker-compose.(stage|prod).py`
