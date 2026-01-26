

## Star Schema 
- is a schema design style in data warehouse
- Include:
  - Fact Table, (info): in the middle
  - Dimension Tables (dim/description): in around
- roles:
  - speed up query
  - optimize join
  - reduce data model complexity

## Catalog
- Where to save metadata of entire data
- catalog in dwh include:
    - table info: schema, description, name
    - column info: type, business sense, constraint, default value ( like declare of colum in SQL ->DDL)
    - lineage: source of table, flow: raw-> staging -> dim/fact
    - owner & steward: who responsible?, which team for maintenance?
    - version/ scheme evolution: what have columns recently added/drop/change-scheme? 
- Catalog in DWH vs Catalog in Data-Lake -> Diff:
  - In Warehouse(Snowflake/Redshift/BigQuery): internal metadata of the system. organizing:>> +schema, +table, +view, +procedures
  - In Data-Lake/Lake-house (Iceberg/Delta/Hudi): Catalog is not a built-in thing — it is a required component to manage files in object storage (S3, MinIO, HDFS).
- Benefit:
  - Standard Schema
  - Ease to access, query
  - Ease control lifecycle of data: data lineage, versioning, retention, audit logs
## 3NF Normalization
- 1-NF:
  - Atomic Column
  - No duplicate rows
  - has unique key
  - order of store data does not matter
- 2-NF:
  - 1-NF
  - No partial dependency exists, meaning every non-primary attribute must depend on the entire primary key

- 3-NF:
    - 2-NF
    - No transitive dependencies
## Apache Spark

### Artchitechture
???
#### Apache Spark with Hadoop
- include:
  - Resource Management: Yarn or Standalone or ???
  - Name Node
  - Work Node
  - Executor
  - Spark Driver
### Auto Compact vs Optimize Writing 
???

### Executor in Spark 
???
### Partition By vs Bucket By 
???

## Lazy Transformation in Spark 
???
## Transformation: Map-Shuffle-Reduce 
- two kind of transformation in spark:
  - wide
  - narrow
## Infer Schema
???

## Join Mechanism in Spark
- Broadcast Hash-Join
- Shuffle Hash-Join
- Shuffle Sort-Merge-Join
## Introduction metadata and metadata management 

- Metadata is data that provides information about other data
- types: 
  - Technical metadata
  - Process metadata 
  - Business metadata
### Technical Metadata 
- define the data structure in data repo or platform, primarily from a technical perspective 
- technical metadata in a data warehouse includes assets such as:
  - Tables:
    - each's table name
    - number of cols and rows each table has 
  - Data Catalog: is an inventory of tables, contain infos:
    - name of each database in the enterprise dwh
    - name of each column present in each db
    - names of every table 
    - type of data that each column contains 
### Process Metadata 
- describes the processes that operate behind business systems such as dwh, accounting-sys, cust-relationship management tools
- explain: many important enterprise systems are responsible for collecting and processing data from various sources... Process metadata for such sys include
tracking things like:
  - process start and end times
  - disk usages
  - where data was moved from and to, and
  - how many users access the systems at any given time
### Business metadata
- data has a descriptive one that express business data within or out of their business
- includes:
  - how the data is acquired 
  - what the data is measuring or describing 
  - the connection of link between the data and other data sources
- Business metadata also serves as documentation for the entire data warehouse system

### Managing metadata 
- Managing metadata includes:
  - developing and administering policies and process to ensure information can be accessed and integrated from various sources 
and appropriately shared across the entire enterprise
  - Creation of a reliable, user-friendly data catalog is a primary objective of a metadata management model. The data catalog
is a core component of a modern metadata management system, serving as the main asset around which metadata management is administered.

## Data-Lake

## ACID in Delta-Lake 

## Data-Exchange 

- Data Exchange platform is a platform for organizations share, buy, sell and exchange data in a controlled, safe, and standard way
- 
