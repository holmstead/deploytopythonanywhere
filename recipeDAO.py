import mysql.connector # for connecting python to the mysql database
from dbconfig import db_config  # import config from dbconfig.py

# create recipeDAO class
class RecipeDAO:
    # constructor
    def __init__(self):
        # connect to the database
        # **db_config unpacks the dictionary into keyword arguments
        self.db = mysql.connector.connect(**db_config) # use the config from dbconfig.py
        # creata a cursor (for executing SQL commands)
        self.cursor = self.db.cursor(dictionary=True) # return as a dictionary

    # Return all recipes
    def get_all(self):
        # Open the file containg the query
        with open('sql/get_all_recipes.sql', 'r') as file:
            sql = file.read()
        
        # Execute sql query - return all rows from the recipe table
        self.cursor.execute(sql)
        
        # Fetch results
        results = self.cursor.fetchall()
        return results

    # Return one recipe by ID
    def find_by_id(self, id):
        # Open the file containg the query
        with open('sql/get_recipe_by_id.sql', 'r') as file:
            sql = file.read()
                
        # Exectue the query
        self.cursor.execute(sql, (id,))

        # Fetch one row from the database query
        result = self.cursor.fetchone() 
        return result

    # Insert a recipe into the database
    def create(self, name, ingredients, instructions):
        # Open the file containg the query
        with open('sql/add_new_recipe.sql', 'r') as file:
            sql = file.read()
        
        # Exectue the query
        self.cursor.execute(sql, (name, ingredients, instructions))
        
        # Commit the transaction
        self.db.commit()  
        return self.find_by_id(self.cursor.lastrowid)  # Return the created recipe (the last row inserted into the database)

    # Update a recipe
    def update(self, id, name, ingredients, instructions):
        # Open the file containg the query
        with open('sql/update_recipe.sql', 'r') as file:
            sql = file.read()
                
        # Exectue the query
        self.cursor.execute(sql, (name, ingredients, instructions, id))

        # Commit the transaction
        self.db.commit()
        return self.find_by_id(id)  # Return the updated recipe

    # Deletes a recipe
    def delete(self, id):
        # Open the file containg the query
        with open('sql/delete_recipe.sql', 'r') as file:
            sql = file.read()
        
        # Exectue the query
        self.cursor.execute(sql, (id,))

        # Commit the transaction
        self.db.commit()  
        return True  # Return True if deletion was successful

    # Close the database connection
    def close(self):
        self.cursor.close()
        self.db.close()