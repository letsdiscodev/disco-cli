# Disco CLI

## Usage

### Install Disco on a Ubuntu 23.10 server with first project

#### Install Disco on server

```bash
disco init root@123.123.123.123
```

#### Add Postgres

This is a temporary way of adding postgres until we polish it a bit.

```bash
disco projects:add --name postgres-project
disco env:set \
    --project postgres-project \
    POSTGRES_PASSWORD=Password1 \
    PGDATA=/var/lib/postgresql/data/pgdata
# see below for content of postgres.json file
disco deploy \
    --project postgres-project \
    --file postgres.json
```

Here's the content of `postgres.json`:
```json
{
    "version": "1.0",
    "services": {
        "postgres": {
            "image": {
                "pull": "postgres:16.1"
            },
            "publishedPorts": [
                {
                    "publishedAs": "5432",
                    "fromContainerPort": "5432",
                    "protocol": "tcp"
                }
            ],
            "volumes": [{
                "name": "postgres-data",
                "destinationPath": "/var/lib/postgresql/data"
            }]
        }
    }
}
```

```bash
# use SQL client to run some SQL
pgcli postgres://postgres:Password1@123.123.123.123/postgres
```

```sql
-- in pgcli
CREATE TABLE page_views (id SERIAL, count INTEGER);
```

#### Add project

```bash
disco projects:add \
    --name first-project \
    --github-repo git@github.com:exampleuser/examplerepo.git \
    --domain app.example.com
# use output from command above to set deploy key and webhook in Github
disco env:set \
    --project first-project \
    DATABASE_URL=postgresql+psycopg2://postgres:Password1@123.123.123.123/postgres
# git push to repo or deploy using this command:
disco deploy \
    --project first-project \
    --commit 999ae33ccdf2cf849f3fc9af5fe9443699265be4
```

#### See logs from the app we just deployed

```bash
disco logs --project first-project
```

#### Setup logging on a third party service

```bash
disco syslog:add syslog+tls://logsN.papertrailapp.com:12345
```

## Local development

Install package locally in a virtualenv.

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
