
CREATE TABLE "owner" (
"id" SERIAL PRIMARY KEY, 
"name" VARCHAR (250));

CREATE TABLE "pets" (
id SERIAL PRIMARY KEY, 
"owner_id" INT REFERENCES "owner", 
"pet_name" VARCHAR (250), 
"breed" VARCHAR (100), 
"color" VARCHAR (100),
"checked_in" DATE);