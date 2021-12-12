from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    else:
        recipes = Recipe.getAllRecipes()
        return render_template('dashboard.html', recipes = recipes)    

@app.route('/recipes/new')
def newRecipePage():
    return render_template('new_recipe.html')

@app.route('/create', methods = ['POST'])
def newRecipe():
    if not 'user_id' in session:
        return redirect('/')
    else:
        
        if not Recipe.recipeValidation(request.form):
            return redirect('/recipes/new')
        else:
            data = {
                'name' : request.form['name'], 
                'description' : request.form['description'], 
                'under_thirty' : request.form['under_thirty'],
                'instructions' : request.form['instructions'],
                'date_created' : request.form['date_created'],
                'user_id' : session['user_id']
            }
            recipe = Recipe.addRecipe(data)
            return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def viewRecipe(recipe_id):
    if not 'user_id' in session:
        return redirect('/')
    else:
        data = {
            'id': recipe_id
        }
        recipe = Recipe.getRecipe(data)
    return render_template('view_recipe.html', recipe = recipe)

@app.route('/recipes/edit/<int:recipe_id>')
def editRecipe(recipe_id):
    if not 'user_id' in session:
        return redirect('/')
    else:
        data = {
            'id': recipe_id
        }
        recipe = Recipe.getRecipe(data)

    return render_template("edit_recipe.html", recipe = recipe)

@app.route('/update/<int:recipe_id>', methods = ['POST'])
def updateRecipe(recipe_id):
    if not 'user_id' in session:
        return redirect('/')
    else:
        if not Recipe.recipeValidation(request.form):
            return redirect('/recipes/edit/<int:recipe_id>')
        else:
            data = {
                'id' : recipe_id,
                'name' : request.form['name'], 
                'description' : request.form['description'], 
                'under_thirty' : request.form['under_thirty'],
                'instructions' : request.form['instructions'],
                'date_created' : request.form['date_created'],
                'user_id' : session['user_id']
            }
            recipe = Recipe.updateRecipe(data)
            return redirect('/dashboard')


@app.route('/recipes/delete/<int:recipe_id>')
def deleteRecipe(recipe_id):
    if not 'user_id' in session:
        return redirect('/')
    else:
        data = {
            'id': recipe_id
        }
        Recipe.deleteRecipe(data)
        return redirect('/dashboard')