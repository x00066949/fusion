# Platform Engineering Role Code Challenge
[![test-cockroachdb](https://github.com/x00066949/fusion/actions/workflows/test.yaml/badge.svg)](https://github.com/x00066949/fusion/actions/workflows/test.yaml)


## Architecture:

![Alt text](architecture.png?raw=true "Architecture")


## Pre Requisites:

* minikube
* python3
* helm

## Steps

1. ```git clone https://github.com/x00066949/fusion.git```

2. Start docker engine

3. ```cd fusion```

4. ```source build_cockroachdb.sh```

5. Within the Cockroach client server, run the following SQL queries: ```CREATE DATABASE movies;``` 

6. ```CREATE TABLE movies.movies (id INT NOT NULL DEFAULT unique_rowid() PRIMARY KEY, title STRING NOT NULL, year INT NULL, extract STRING NULL, thumbnail STRING NULL, cast_list STRING[] NULL, genres STRING[] NULL, thumbnail_width INT NULL, thumbnail_height INT NULL); ```

7. ```CREATE USER (db-user) WITH PASSWORD '(database-password)';```

8. ```GRANT admin TO (db-user);```

9. Exit the Cockroachdb client server
```\q```

10. ```export DB_USER=(db-user)```
11. ```export DB_PASSWORD=(database-password)```

12. ```source setup_k8s.sh```

13. visit the following url once to populate the db table with movies data
    * localhost:(randomly-assigned-minikube-port)/addall


## ENDPOINTS:
* /addall - GET - to populate the initial database. I made this an api just so it's easier to test upon initial setup. in a real-world scenario, this will not be implemented as we'll already have data in the database initially

* /genre/(genre) - GET - get movies in a specified genre - e.g /genre/comedy

* /cast/fullname/(first) - GET - Actors with really single and multiple names - e.g /cast/fullname/firstname_secondname_thirdname_fourthname_nname , /cast/zendaya
* /cast/firstname/(first)/lastname/(last) - GET - e.g /cast/firstname/will/lastname/smith
* /cast/firstname/(first)/middlename/(middle)/lastname/(last) - GET  - e.g /cast/firstname/Lara/middlename/Flynn/lastname/Boyle 

* /title/(title) - GET - Find movie info given a title - e.g: /title/Where_the_Day_Takes_You , /title/wind

* /year/(year) - GET - Find movies released in a given year - e.g: /year/2015

## Database Considerations:
*  Due to data structure and no obvious primary key, the obvious choicee is nosql. dynamodb and mongo db being my first choice.
* But with <5ms response time expected, dynamo db would be out as network cost of going over Amazon VPC endpoint might > 5 ms.
* Optimizations are available for running queries. Like indexing. 
* However, for this exercisem, the main reason i didn't choose Dynamo DB was my lack of access to a sandbox AWS account. 
* I didnt go w mongodb only because I'm unfamiliar with it and time constraints for this exercise means i may not have enough time to learn about the technology to confidently answer probing questions around encryption in transit and at rest.
* I chose self hosted cocroach db because: 
    * It is hosted alongside api so lower network cost/latency
    * It is scalable as it'll use the scaling policy of our eks nodes and scaling can also be set at the pod level too. We can also isolate it to it's own node pool.
    * primary key can be a composition of multiple columns or auto generated and since no other tables/foreign key relationship exists, no need for us to be aware of each row's PK

## TODO: 

* Unit testing :( and integrating it with the github actions workflow
* Swagger API Doc
* Case insensitive actor name matching. SQL Alchemy ORM query for iconatins (case insensitive contains) doesn't seem to work with array datatype. Tried to get around this by pre capitalizing the names, however, there are some edge cases where this doesn't work. i.e "Yahya Abdul-Mateen II" another approach to querying actors, would be better.
