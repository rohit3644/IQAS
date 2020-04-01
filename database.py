# Database class is used to make connection to the database,
# execute insert and select query and to close the connection


class Database:
    # constructor
    def __init__(self):
        try:
            # third-party library
            import mysql.connector
            from mysql.connector import Error
            from dbcredentials import host, user, password, database
            # Making connection
            self.mydb = mysql.connector.connect(
                host=host, user=user, password=password, database=database)
            self.cursor = self.mydb.cursor()
        except Error as e:
            print("Error: ", e)

    # Function to execute insert query
    def insert_query(self, param):
        initial_result = self.select_query(param)
        if(initial_result):
            return("Question is already stored")
        else:
            query = """Insert into Answers(Value,Answer) values (%s,%s)"""
            value = (param["Value"], param["Answer"])
            self.cursor.execute(query, value)
            self.mydb.commit()
            result = self.cursor.rowcount
            return(result)

    # Function to execute select query
    def select_query(self, param):
        query = """Select Answer from Answers where Value = %s"""
        value = (param["Value"],)
        self.cursor.execute(query, value)
        result = self.cursor.fetchone()
        return(result[0])

    # function to close connection

    def close_connection(self):
        if self.mydb.is_connected():
            self.cursor.close()
            self.mydb.close()


def main():
    # database object
    database_object = Database()
    # parameter
    param = {"Value": 4, "Answer": "Narendra Modi is the current prime minister"}
    result = database_object.select_query(param)
    # closing the connection
    database_object.close_connection()
    print(result)


if __name__ == "__main__":
    main()
