---

## Usage

### Install Disco on a Ubuntu 23.10 server with first project

#### Install Disco on your server

```bash
disco init root@123.123.123.123
```

#### Add Postgres addon

```bash
disco projects:add \
    --name postgres \
    --github-repo https://github.com/letsdiscodev/disco-addon-postgres \
    --deploy
```

#### Add project, with a database

```bash
disco projects:add \
    --name first-project \
    --github-repo git@github.com:exampleuser/examplerepo.git \
    --domain app.example.com
```
Follow the instructions from the output above for the deployment key and webhook.

#### Add a database to the project
```bash
disco command postgres db:add --project first-project
```
This should have set the env variable `DATABASE_URL` for `first-project`.

Also notice that there's the `postgres` addon and the Postgres database with a generated name like `postgres-db-clean-passenger`:
```bash
disco projects:list
```

The addon deployed Postgres and added a database for `first-project`.
Adding more databases for other projects should use the same Postgres instance.

##### Use an SQL client to run some SQL

```bash
pgcli $(disco env:get DATABASE_URL --project first-project)
```

```sql
-- in pgcli
CREATE TABLE page_views (id SERIAL, count INTEGER);
```

#### Deploy the project
Either push a commit to the project to let the webhook trigger a build,
or use the CLI:
```bash
disco deploy --project first-project
```

#### Run a command in your project
```bash
disco run --project first-project "python migrate.py"
```

#### See logs from the app we just deployed

```bash
disco logs --project first-project
```

#### Setup logging on a third party service

```bash
disco syslog:add syslog+tls://logsN.papertrailapp.com:12345
```

#### List deployments for a project

```bash
disco deploy:list --project first-project
```

#### Get output of a specific deployment
```bash
disco deploy:output --project first-project --deployment 123
```

## Local development of the CLI

Install the package locally in a virtualenv.

```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install --editable .
```

Test that it works
```bash
$ disco --version
disco-cli 0.1.0
```
