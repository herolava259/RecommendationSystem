## Tags

- Hadoop
- Hive
- Yarn
- Spark
- Delta-Lake
- Data-Lake
- Bronze-> Silver -> Gold
- CLick House
- Duck Db
- Standalone 
- HBase
- S3 / Minio 


## Classification

### 1. Data warehouse
- DuckDB: local small project
- Click-House: big project, has multiple nodes, so strong for dwh
- Big-Query: in GCP

### 2. Ingest 
- Kafka: streaming
- Flink Ingest
- API / Crawler (Fire Crawl)
- Debezium: ????

### 3. Store
- S3/ MinIO / ADLS???: object storage
- HDFS: distributed file system
- Local file system

### 4. Data Lake/ Lake-House
- Iceberg (delta-lake)
- Delta Lake (as name)
- Hudi ???

### 5. Transforming/ Processing Data
- Spark: batch/stream
- Flink: (streaming)

### 6. Orchestration
- Airflow
- Dagster ??? 

### 7. Govern ??? 
- Hive Metastore
- Glue Catalog
- Iceberg Catalog 
- DataHub

## What is Apache Iceberg?
- = table-format + metadata layer
- What?:
  - table management in data lake
  - bring ACID for data lake 
  - connector between data-lake and compute-engine like: spark, flink, trino???, hive???, presto???, snowflake???, duck-db
  - unlock large processing problem: 
  - versioning and time travel
- How?:
  - Schema Evolution
  - Hidden Partitioning
  - ACID Transaction
  - Time Travel: Explain: supporting to save metadata snapshots. eg: `SELECT * FROM table VERSION AS OF 1577836800;`
  - Incremental Reads / CDC
  - Powerful Metadata pruning: save metadata following by: + manifest file. + manifest list. + snapshot
  - Automatically organize file: + merge small files. + split a large file. + rewrite data to optimization
  - Multi-engine concurrency
  - Table-level governance: retention policy. + snapshot expiration. + metadata cleaning. + row-level delete

## Airflow

- components:
  - airflow-postgres: db, store metadata about DAGs, task, ...
  - redis: CeleryExecutor need it, it facilitates communication between the airflow-scheduler and celery workers
  - airflow-webserver:  airflow-ui, interact intuitively with users
  - airflow-scheduler: schedules tasks and manage execution of workflows
  - airflow-worker: execute tasks defined in the DAGs
  - airflow-trigger: for handling event-driven triggers in airflow
  - airflow-init: initializes airflow envs
  - airflow-cli: cli that is used to interact with airflow-env

## Hadoop-Hive 

### Hadoop:
- is an open-source framework to store and process big-data in distributed system.
- include 2 components: 1.Map-Reduce, 2.HDFS (Hadoop Distributed File System)
- Map-Reduce: parallel programming model for distributed system. include 2 stage:
  - map: split tasks, groups and schedule for them on distributed computation nodes to processing tasks
  - reduce: merging results from workers
- HDFS: 
  - Distributed File System
- It contains other tools 
  - Sqoop: i/o for data from HDFS to RDBMS
  - Pig: procedure programming framework for MapReduce 
  - Hive: a framework provide SQL syntax for users write sql scripts
### Hive:
- is a data warehouse infra engine for processing structured data in Hadoop
- is **not** a:
  - database
  - tool/engine for OTLP(Online Transaction Processing)
  - real-time query engine
- features:
  - erd, processing data for HDFS
  - be made for OLAP (OnLine Analytic Processing)
  - familiar, quickly, scalable
- architecture:
  - High layer:
    - User-interface. Include:
      - Web UI
      - Hive CLI
      - HD Insight ???
      - library for programming
  - Middle layer:
    - Meta store
    - For Map-Reduce:
      - Hive QL Process Engine
      - Execution Engine
  - Low Layer:
    - HDFS or HBASE Data Storage
