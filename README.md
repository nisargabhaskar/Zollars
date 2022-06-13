# Zollars - Python project on simulation of blockchain


## Description
Project Title
Zollars - Python project on simulation of blockchain


Build Status
Created a simulation of blockchain and created an api to access the various functionalities of blockchain and connected to a postgresql container  - 13/06/2022

<!-- Screenshots
As the saying goes, a picture is equal to a thousand words. Most people will be interested if there is a visual representation of what the project is about. It helps them understand better. A visual representation can be snapshots of the project or a video of the functioning of the project. -->

Tech/Framework used
* FastAPI
* PostgreSQL

Features
Simulates a blockchain envoirnment which can later be accessed by different API functions provided.

<!-- Installation
If your project needs installation of certain software or configurations to the system. Do mention it in this section as it helps a lot for the reader to use your project. The steps mentioned should be precise and explanatory.  If possible, you can add links that can help them better understand how to configure/install the necessary files or softwares.

API reference
If your project is small, then we can add the reference docs in the readme. For larger projects, it is better to provide links to where the API reference documentation is documented.

Tests
This is the section where you mention all the different tests that can be performed with code examples  -->


How to Use?
* Create a postgres docker container to act as a server database and run it 
```
docker pull postgres:alpine
docker run --name name_of_container -e POSTGRES_PASSWORD = password -d -p 5432:5432 postgres:alpine
docker exec -it blockchain bash
```
* Create a database in postgres and connect to it
```
psql -U postgres
create database blockchain_database;
create user myuser with encrypted password 'blockchain';
grant all privileges on database blockchain_database to myuser;
\c blockchain_database
psql -h localhost -p 5432 postgres
```
* Open terminal in the folder where you have the code
```
source venv/bin/activate
uvicorn main:app --reload
```
* In your browser you can access the API's in http://localhost:8000/docs
* Commit the changes made in database
```
docker commit container_id name_of_container
```