from flask import Flask, request, jsonify
import psycopg2
config_string= 'host = "127.0.0.1",port = "5432",database = "pet_hotel"'
app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/pets/", methods=["GET","POST","DELETE","PUT"])
def pets():
    connection = psycopg2.connect(host = "127.0.0.1",
                            database = "pet_hotel")

    cursor = connection.cursor()
    data = request.get_json()
    # POST PETS
    if request.method == "POST":
        try:
            # Open a connection to db
            print(request.json)

            if data:
                print(data)
                # Execute query to post new pet
                querytext="""INSERT INTO pets ("owner_id","pet_name","breed", "color") VALUES (%s, %s,%s,%s);"""
                cursor.execute(querytext, ( data["owner_id"],data["pet_name"],data["breed"],data["color"],))
                connection.commit()
                # status message
                response = jsonify({"message":"ok"})
                response.status_code = 200
                return response
        except (Exception, psycopg2.Error) as error :
            print("Error while connecting to PostgreSQL in post Pets", error)
        finally:
                if(connection):
                      cursor.close()
                      connection.close()
                      print("PostgreSQL connection is closed")
    # END OF POST PETS

    # GET PETS
    elif request.method =='GET':
        try:
            # Open a connection to db
            connection = psycopg2.connect(host = "127.0.0.1",
                            database = "pet_hotel")
            # create a cursor to "a vessel between server and db"
            cursor = connection.cursor()        
            # Execute query
            cursor.execute("""SELECT * FROM pets;""")
            # Fetch all results from cursor as "rows"
            rows = cursor.fetchall()
            # create an empty list called results to make with our loop
            results = []
            # Create object to jsonify and append to results LIST
            for row in rows:
                obj = {
                    "id":row[0],
                    "owner_id":row[1],
                    "pet_name":row[2],
                    "breed":row[3],
                    "color":row[4],
                    "check_in":row[5]
                }  
                results.append(obj)
            # create a response out of jsonifying our list of objects, add a status code to end.
            response = jsonify(results)
            response.status_code = 200
        
            # close cursor
            cursor.close()
            print('Connection closed')
        
            # return response
            return response
    
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
  # END OF GET PETS

  # DELETE PETS
    elif request.method== "DELETE":
        try:
            #get the named id parameter from 
            id=request.args.get("id")
            print(id)
            # Execute query
            if  id:
                cursor.execute("""DELETE FROM pets WHERE id=(%s)""", ( id,))
                connection.commit()

                response = jsonify({"message":"ok"})
                response.status_code = 201
                return response
            
        except (Exception, psycopg2.Error) as error :
            print ("Error while deleting pet ", error)

        finally:
            if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
    # END OF DELETE PETS

    #DELETE PETS

@app.route("/owner/", methods=["POST","DELETE","GET"])
def owner():
    connection = psycopg2.connect(host = "127.0.0.1",
                            database = "pet_hotel")

    cursor = connection.cursor()
    data = request.get_json()
    print(request.args.get("id")) 
    # GET OWNER
    if request.method == "POST":
        try:        
            print(request.json)
            
            if data:
                cursor.execute("""INSERT INTO owner(name) VALUES(%s)""", ( data["name"],))
                connection.commit()

                response = jsonify({"message":"ok"})
                response.status_code = 200
                return response

        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            #closing database connection.
                if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
    # END OF GET OWNER

    # GET DELETE
    elif request.method == 'DELETE':
        try:
            id=request.args.get("id")
            print(id)
            # Execute query
            if  id:
                cursor.execute("""DELETE FROM owner WHERE id=(%s)""", ( id,))
                connection.commit()

                response = jsonify({"message":"ok"})
                response.status_code = 201
                return response
            #cursor.execute("""SELECT * FROM owner;""")
        except (Exception, psycopg2.Error) as error :
            print ("Error while deleting owner ", error)

        finally:
            if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")
    # END OF GET DELETE

    # GET OWNER
    elif request.method =='GET':
        try:
            # Open a connection to db
            connection = psycopg2.connect(host = "127.0.0.1",
                            database = "pet_hotel")
            # create a cursor to "a vessel between server and db"
            cursor = connection.cursor()        
            # Execute query
            cursor.execute("""SELECT * FROM owner;""")
            # Fetch all results from cursor as "rows"
            rows = cursor.fetchall()
            # create an empty list called results to make with our loop
            results = []
            # Create object to jsonify and append to results LIST
            for row in rows:
                obj = {
                    "id":row[0],
                    "name":row[1]
                }  
                results.append(obj)
            # create a response out of jsonifying our list of objects, add a status code to end.
            response = jsonify(results)
            response.status_code = 200
        
            # close cursor
            cursor.close()
            print('Connection closed')
        
            # return response
            return response
    
        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)
        # END OF GET OWNER
        finally:
            #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


if __name__ == '__main__':
    app.run()