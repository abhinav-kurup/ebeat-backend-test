## eBeat Book System for Goa Police



create database test123;

\c test123;

create user testuser with password 'password';

grant all privileges on database test to testuser;

psql -d test

create extension postgis;

pip install psycopg2-binary




## delete tables in postgres

psql -d test

DROP SCHEMA public CASCADE;

CREATE SCHEMA public;

GRANT CREATE ON SCHEMA public TO testuser;

GRANT ALL ON SCHEMA public TO public;

create extension postgis;

##