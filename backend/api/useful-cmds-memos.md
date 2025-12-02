# Useful commands 

## Docker

- check networks 

```shell
docker network inspect <network_name>
```

- check info of a container 

```shell
docker inspect <container_name_or_id>
```

- view containers

```shell
docker ps 
```

- run cli of a container

```shell
docker exec -it <container_name_or_id> bash
```

- view port of container 
- template result: internal-ip -> expose/external ip addr

```shell
docker port <container_name>
```

- view logs of a container

```shell
docker logs <container_name>
```

## Postgres CLI

- enter cli for s specified db 

```shell
psql -U <user-name> -d <database-name>
```

- list all db 

```shell
\l or \list
```

- connect to db 
```shell
\c dbname
```

- list all table: `\dt`
- view structure of a table: `\d tablename`
- list user/role: `\du`
- list scheme: `\dn`
- list function(sql): `\df`
- out/exit psql cli: `\q`
- change password: `\password`
- view size of all db: `\l+`
- view index: `\d <table_name>`
- view sequence: `\ds`
- view size for each table: `\dt+`
- pretty db size: `SELECT pg_size_pretty(pg_database_size('<db-name>'))`
- pretty tb size: `SELECT pg_size_pretty(pg_total_relation_size('<table-name>'))`

#### debug/troubleshoot
...



### Alembic 

- list template 
```shell
alembic list_templates
```

- init 
```shell
alembic init --template pyproject_async <migration_name(ex: migrations)> 
```
- Notes:
    * pyproject is an example, view all templates in cmd `alembic list_templates` for know more details

- create migrations 
```shell
alembic revision --autogenerate -m <migration-status(ex: initial db, create table customer,...)>
```

- upgrade 
```shell
alembic upgrade head
```

```shell
alembic upgrade <revision_id>
```

- list history of migrations 
```shell
alembic history
```

- downgrade 

```shell
alembic downgrade base
```

- details of current migration:

```shell
alembic current
```



