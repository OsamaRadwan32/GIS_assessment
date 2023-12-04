# GIS_assessment

## Postgres

1- Access postgres using the following command

```
sudo -i -u postgres

psql
```

2- Copy and paste the code below and run it in the terminal to create the database tables

```
-- Create the gis_assessment database
CREATE DATABASE gis_assessment;

-- Connect to the newly created database
\ c gis_assessment;

-- Create the 'users' table
CREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY NOT NULL,
created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
email VARCHAR(100) UNIQUE NOT NULL,
username VARCHAR(100) NOT NULL,
password VARCHAR(200) NOT NULL
);

-- Create the 'tables' table with a foreign key relationship to the 'users' table
CREATE TABLE IF NOT EXISTS tables (
id SERIAL PRIMARY KEY NOT NULL,
created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
name VARCHAR(100) UNIQUE NOT NULL,
user_id INTEGER NOT NULL REFERENCES users(id),
structure JSONB
);
```

## Backend

Activate the virtual environment

```
source .venv/bin/activate
```

Change directory to access the flask application

```
cd app
```

Use the code below to install dependencies

```
pip install -r requirements.txt
```

Run the app

```
flask run --debug
```

## Frontend

When in projects main directory change directory to access the react app

```
cd frontend
```

Install dependencies using the following:

```
npm install
```

Run the react app

```
npm start
```
