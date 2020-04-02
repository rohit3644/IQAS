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
        # Check if the value is already present
        initial_result = self.select_query(param["Value"])
        if(initial_result == None):
            # Prepared Statement
            query = """Insert into Answers(Value,Answer) values (%s,%s)"""
            # Binding the value
            value = (param["Value"], param["Answer"])
            # Executing the query
            self.cursor.execute(query, value)
            # This is required to save changes
            self.mydb.commit()

    # Function to execute select query
    def select_query(self, value):
        # Prepared Statement
        query = """Select Answer from Answers where Value = %s"""
        # Bind value
        param = (value,)
        # Execute query
        self.cursor.execute(query, param)
        # Fetch the first result
        result = self.cursor.fetchone()
        return(result)

    # function to close connection

    def close_connection(self):
        # Check if connection is present or not
        if self.mydb.is_connected():
            self.cursor.close()
            self.mydb.close()

    def main(self, value, answer):
        # parameter
        param = {"Value": value, "Answer": answer}
        # Calling insert query
        self.insert_query(param)
        # closing the connection
        self.close_connection()
