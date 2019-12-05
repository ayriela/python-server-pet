from flask import Flask, request, jsonify
import psycopg2
config_string= 'host = "127.0.0.1",port = "5432",database = "pet_hotel"'
app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/pets/")
def pets():
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
    finally:
        #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")


@app.route("/owner/", methods=["POST","DELETE"])
def owner():
    connection = psycopg2.connect(host = "127.0.0.1",
                            database = "pet_hotel")

    cursor = connection.cursor()
    data = request.get_json()
    print(data["name"])
    print(request.args.get("id")) 
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
    elif request.method == 'DELETE':
        try:
            id=request.args.get("id")
            # Execute query
            if  id:
                cursor.execute("""DELETE FROM owner WHERE id=(%s)""", ( id,))
                connection.commit()

                response = jsonify({"message":"ok"})
                response.status_code = 200
                return response
            #cursor.execute("""SELECT * FROM owner;""")
        except (Exception, psycopg2.Error) as error :
            print ("Error while deleting owner ", error)

        finally:
            if(connection):
                    cursor.close()
                    connection.close()
                    print("PostgreSQL connection is closed")

if __name__ == '__main__':
    app.run()