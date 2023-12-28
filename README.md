Architecture:

![Alt text](architecture.png?raw=true "Architecture")


Pre Requisites:

* minikube
* python3
* helm

Steps

1. Start docker engine

2. cd fusion

3. source build_cockroachdb.sh

4. CREATE DATABASE movies; 

5. CREATE TABLE movies.movies (id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY, title STRING NOT NULL, year INT NULL, extract STRING NULL, thumbnail STRING NULL, cast_list STRING[] NULL, genres STRING[] NULL, thumbnail_width INT NULL, thumbnail_height INT NULL); 

5. CREATE USER <db-user> WITH PASSWORD '<database-password>';

6. GRANT admin TO <db-user>;

7. Exit the Cockroachdb client server
\q

8. export DB_USER=<db-user>
9. export DB_PASSWORD=<database-password>

10. source setup_k8s.sh

visit the following url once to populate the db table with movies data
11: localhost:<randomly-assigned-minikube-port>/addall
