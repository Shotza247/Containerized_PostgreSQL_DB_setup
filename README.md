To run PostgreSQL inside a Docker container instead of installing it directly onto your operating system, follow these steps.

## 1. Run the PostgreSQL Container
Open your terminal and run the following command. This will automatically pull the official image and start the database:

docker run --name my-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres

## 2. Breakdown of the Command

* --name my-postgres: Names your container my-postgres so it is easy to reference later.
* -e POSTGRES_PASSWORD=mysecretpassword: Sets your mandatory database password. Change mysecretpassword to whatever you prefer.
* -p 5432:5432: Maps port 5432 from inside the container to port 5432 on your local machine.
* -d: Runs the container in the background (detached mode).
* postgres: Uses the latest official PostgreSQL image from Docker Hub.

## 3. Connect to Your Database
To connect to the database command line (psql) inside your running container, run:

```
docker exec -it my-postgres psql -U postgres
```

Learn more at https://docs.docker.com/go/debug-cli/ then:

```
docker debug my-postgres
```
postgresdb container logs:

```
docker logs my-postgresdb 
```

check container is up on docker.
```
docker ps   
```

output:
CONTAINER ID   IMAGE      COMMAND                 CREATED       STATUS            PORTS                        NAMES
aa0ac00822ce   postgres   "docker-entrypoint.s…"   5 hours ago   Up About an hour   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp my-postgresdb

To exit the database command line, type \q and hit Enter.
## 4. Manage the Container

* Stop the database: docker stop my-postgres
* Start it again: docker start my-postgres
* Check if it is running: docker ps [7, 8] 

Would you like help setting up a persistent storage folder so your data isn't lost if the container is deleted, or would you like a Docker Compose file to manage it alongside a management tool like pgAdmin?

# set up a local environment for our dependencies and liabraries:
py -m venv .venv  

## Option 1: Temporarily allow scripts (recommended):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

.\.venv\Scripts\Activate.ps1

## Option 2: Bypass the policy for just this PowerShell session
If you don't want to change your execution policy permanently:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

- Then:

```
.\.venv\Scripts\Activate.ps1
```

## Then install the PostgreSQL driver:
- Your requirements.txt will look something like:

```
psycopg2-binary==2.9.x
```

or, if using psycopg 3:

```
-> psycopg[binary]==3.x.x
```

or run:

```
pip freeze > requirements.txt
```

or

```
pip install -r requirements.txt 
```

Verify the installed version:

```
py -c "import psycopg2; print(psycopg2.__version__)"as
```

If you wnat to Step out of the local environment
(optional not necessary if not intalling anything outside your env):

```
deactivate
```

Run these:

```
1. py config.py   
2. py logging_config.py 
3. py DB_SetUp.py  
4. py Postgres_SetUp.py 
```

Run the select statement

```
5. select * from test_users;
```

Drop the test_users table:

```
drop table if exists test_users;
```

After that i added a new file called DBOps:
This will run our DB operations like getting the version creating tables, insert, updates, deletes, and many more.

Rerun this:
- py DB_SetUp.py
- py DBOps.py
- py Postgres_SetUp.py 