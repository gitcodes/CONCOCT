from recipe_scrapers import scrape_me
import pandas as pd

def get_link(dishname):
    link = None
    recipes = pd.read_csv("./Recipe Model/Dataset.csv")
    row =  recipes.loc[recipes['Dish_Name'] == dishname].values
    if row.size > 2:
        link = row[0][row.size - 1 ]          
    else:
        link = None    
    return link

def get_recipe(dishname):
    instructions = []
    link = get_link(dishname)
    if (link != None):
        try:
            scraper = scrape_me(link)  
            instructions = scraper.instructions()
        except:
            instructions = []
    return instructions

