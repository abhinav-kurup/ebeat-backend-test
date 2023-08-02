## eBeat Book System for Goa Police



create database test123;

\c test123;

create user testuser with password 'password';

grant all privileges on database test to testuser;

psql -d test

create extension postgis;

pip install psycopg2-binary




## connect to remote postgres

psql -h dpg-cj4f6e2ip7vuasiultj0-a -p 5432 -U ebeat_db_user -d ebeat_db

postgres://ebeat_db_user:6H5aDRXbGUKzafCWNYhtjgcKK8vavJrf@dpg-cj4f6e2ip7vuasiultj0-a/ebeat_d