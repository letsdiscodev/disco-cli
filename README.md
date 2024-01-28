# Disco CLI

## Usage

### Install Disco on a Ubuntu 23.10 server with first project

#### Install Disco on server

```bash
disco init \
    --ssh root@123.123.123.123
    --disco-domain disco.example.com
```

#### Add Postgres

```bash
disco projects:add --name postgres-project
disco env:set \
    --name postgres-project \
    POSTGRES_PASSWORD=Password1 \
    PGDATA=/var/lib/postgresql/data/pgdata
# temporary hack, see below for content of postgres.json file
disco deploy \
    --name postgres-project \
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
pgcli postgres://postgres:Password1@disco.example.com/postgres
```

```sql
-- in pgcli
CREATE TABLE page_views (id SERIAL, count INTEGER);
```


#### Add web project with worker

```bash
disco projects:add \
    --name first-project \
    --github-repo \
    git@github.com:exampleuser/examplerepo.git \
    --domain app.example.com
# use output from command above to set deploy key and webhook in Github
disco env:set \
    --name first-project \
    DATABASE_URL=postgresql+psycopg2://postgres:Password1@disco.example.com/postgres
# git push to repo or deploy using this command:
disco deploy \
    --name first-project \
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
