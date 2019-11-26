from get_dish import get_dish_name
from get_recepie import get_recipe
from utilities import save_user_details
from flask import (Flask,Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify)

app = Flask(__name__)   

@app.route('/',methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register',methods=('GET', 'POST'))
def register():
    recipies_for_dishes = {}
    if request.method == 'POST':
        details = []
        metadata = []
        details.append(request.form['username'])
        details.append(request.form['name'])
        details.append(request.form['password'])
        metadata.append(request.form['cusine'])
        metadata.append(request.form['allergy'])
        userdetails = [details,metadata]
        save_user_details(userdetails)
        return  render_template('home.html',recepies = recipies_for_dishes)
    return render_template('register.html')

@app.route('/home',methods=('GET', 'POST'))
def home():
    recipies_for_dishes = {}
    list_general_ingredients = "oil,olive oil,salt,pepper,flour,butter,cumin,chili flakes,black pepper,thyme,garlic,ginger,mint,chillies,sage,cinnamon"
    if request.method == 'POST' :
        user_ingredients = request.form['ingredients']
        user_ingredients = user_ingredients +','+list_general_ingredients
        user_ingredient_list = [x.strip() for x in user_ingredients.split(',')]
        dishes =  get_dish_name(user_ingredient_list)        
        recipies_for_dishes =  get_all_dish_recipes(dishes)
    return render_template('home.html',recepies = recipies_for_dishes,ing = list_general_ingredients)


def get_all_dish_recipes(dishes):
    recipies_dishes = {}
    for dish in dishes:
       recipies_dishes[dish] =  get_recipe(dish)
    print(recipies_dishes)
    return recipies_dishes

if __name__ == '__main__':
    app.run(debug=True)
    
