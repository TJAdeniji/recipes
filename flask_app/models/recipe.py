from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    db = 'recipes_db'
    def __init__ (self, data):
        self.id =  data['id']
        self.name = data['name']
        self.description = data['description']
        self.under_thirty = data['under_thirty']
        self.instructions = data['instructions']
        self.date_created = data['date_created']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = []

    @classmethod
    def addRecipe(cls, data):
        query = "INSERT INTO recipes (name, description, under_thirty, instructions, date_created, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(under_thirty)s, %(instructions)s, %(date_created)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def getAllRecipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        if len(results) == 0:
            return recipes
        else:
            for recipe in results:
                recipes.append(cls(recipe))
            return recipes

    @classmethod
    def getRecipe(cls, data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        if not results:
            return False
        this_recipe = cls(results[0])
        return this_recipe

    @classmethod
    def updateRecipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under_thirty = %(under_thirty)s, instructions = %(instructions)s, updated_at = NOW(), user_id = %(user_id)s WHERE recipes.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def deleteRecipe(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getRecipeWithUser(cls):
        query = "SELECT *FROM recipes LEFT JOIN users ON recipes.id = users.id WHERE recipes.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query)
        recipeData = cls(results[0])
        for row in results:
            user = {
                'id' : row['user.id'], 
                'first_name' : row['first_name'], 
                'last_name' : row['last_name'],
                'email' : row['email'], 
                'password' : row['password'], 
                'created_at' : row['ninjas.created_at'],
                'updated_at' : row['ninjas.updated_at']
            }
        recipeData.users.append(User(user))

    @staticmethod
    def recipeValidation(recipeData):
        is_valid = True
        if not recipeData['name'].isalpha():
            flash("Invalid recipe name", 'recipe')
            is_valid = False
        if not len(recipeData['name']) > 3:
            flash("Name is too short, must be at least 3 characters.", 'recipe')
            is_valid = False
        if not len(recipeData['description']) > 3:
            flash("Description is too short, must be at least 3 characters.", 'recipe')
            is_valid = False
        if not len(recipeData['instructions']) > 3:
            flash("Instructions too short, must be at least 3 characters.", 'recipe')
            is_valid = False
        return is_valid