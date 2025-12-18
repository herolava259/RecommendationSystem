# How to set up postgresql 

## 1. Running Docker compose 

```bash
docker compose -f docker-compose-postgresql.yaml up -d 
```

## Useful CMD

- check logs 

```bash
docker logs applicationdb
```

## Postgresql with terminal 

- Step 1: access cmd of the database 

```bash
docker exec -it 7f6b5155e545 bash
```

- Step 2: activate posgres cli with current user name:

```bash
psql -U ghostofrace
```

- activate postgresql cli 

```bash
docker compose exec -it postgresappdb psql -U ghostofrace -d recappdb
```