from flask import Flask, render_template, request, jsonify
from recipeDAO import RecipeDAO # imports the DAO

# Create an instance of the DAO
recipe_dao = RecipeDAO()

# Flask constructor
app = Flask(__name__, static_url_path='', static_folder='static') 
# makes static files accessible at the root URL (/) instead of /static

# Bind the index() funtion to the ‘/’ URL (homepage) 
@app.route('/')
def index():
    # Render the template 'index.html' from the 'templates' folder
    return render_template('index.html')

# Endpoint: UGet all recipes by ID (PUT request)
@app.route('/recipes', methods=['GET']) # Action: Get
def getall():
    # Use get_all method from the DAO
    recipes = recipe_dao.get_all()

    # Return recipe as JSON
    return jsonify(recipes)

# Endpoint: Get recipe by ID (GET request)
@app.route('/recipes/<int:id>', methods=['GET']) # Action: Get. <int:id> is a variable, URL looks like ~/recipes/1
def get_recipe_by_id(id):    
    # Use find_by_id method in DAO to fetch recipe
    recipe = recipe_dao.find_by_id(id)
    
    if recipe:
        # Return recipe as JSON
        return jsonify(recipe)  
    else:
        # If no recipe found give 404 not found error
        return jsonify({"error": "Recipe not found"}), 404

# Endpoint: Create recipe (POST request)
@app.route('/add_recipe', methods=['POST'])  # Action: Create
def create_recipe():
    # Read JSON data from the body
    json_data = request.json

    # Ensure all necessary fields are provided
    if 'name' not in json_data or 'ingredients' not in json_data or 'instructions' not in json_data:
        return jsonify({"error": "Missing required fields: 'name', 'ingredients', and 'instructions'."}), 400

    # Create the recipe using the DAO
    new_recipe = recipe_dao.create(json_data['name'], json_data['ingredients'], json_data['instructions'])

    # Return the created recipe as JSON with a 201 status code (successfully created)
    return jsonify(new_recipe), 201

# Endpoint: Update recipe by ID (PUT request)
@app.route('/recipes/<int:id>', methods=['PUT'])  # Action: Update
def update_recipe(id):
    # Read JSON data from the request body
    json_data = request.json

    # Check if the required fields are present
    if 'name' not in json_data or 'ingredients' not in json_data or 'instructions' not in json_data:
        return jsonify({"error": "Invalid data, 'name', 'ingredients', and 'instructions' are required."}), 400

    # Extract the data
    name = json_data['name']
    ingredients = json_data['ingredients']
    instructions  = json_data['instructions']

    # Call the DAO to update the recipe
    updated_recipe = recipe_dao.update(id, name, ingredients, instructions)

    if updated_recipe:
        # Return the updated recipe with a 200 status code (successful request)
        return jsonify(updated_recipe), 200  
    else:
        # Return a 404 error if the recipe was not found
        return jsonify({"error": "Recipe not found or update failed."}), 404  

# Endpoint: Delete recipe by ID (DELETE request)
@app.route('/recipes/<int:id>', methods=['DELETE'])  # Action: Delete
def delete_recipe(id):
    # Call the DAO to delete the recipe
    success = recipe_dao.delete(id)
    
    if success:
        # Return a success message with a 200 status code (successful request)
        return jsonify({"message": "Recipe deleted successfully."}), 200
    else:
         # Return a 404 error if the recipe was not found
        return jsonify({"error": "Recipe not found."}), 404 


if __name__ == "__main__":
    # Start the application (in debug mode)
    app.run(debug=True)
