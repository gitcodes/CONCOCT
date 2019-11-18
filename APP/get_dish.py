from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import operator

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results


def search(data,ingredients):
    #user_ingredients = input("Enter ingredients followed comma\n")
    ## need to make two cols for user ingrds one for standard and one for dynamic ingrds
    # user_ingredients = "Potatoes, Garlic, Cream, Black Pepper, Nutmeg, Cheese, Eggs, Milk, Butter, pasta,milk,Salad Dressing,eggs,cheese,crumbs,butter,"
    # user_ingredients = [x.strip() for x in user_ingredients.split(',')]
    suggestions = []
    grocery = []
    keywords = []
    for i in range(len(data)):
        temp = data.Ingredients[i]
        res = [x.strip() for x in temp.split(',')]
        score = len(set(res) - set(ingredients))
        if(score == 0):
            #print("Best Match - ", data.Dish_Name[i])
            suggestions.append(data.Dish_Name[i])
            cv = CountVectorizer()
            attri = data.Cuisine[i] + ' , ' + data.Difficulty[i] + ' , ' + data.Meat[i] 
            attri = [attri]
            cv.fit(attri)
            keywords.append(list(cv.vocabulary_.keys()))
            #print(keywords)
            
        if(score <= 5 and score >= 1):
            #print(data.Dish_Name[i])
            grocery.append(data.Dish_Name[i])

    return suggestions, grocery, keywords


def implicit_filtering(prefer,smap):
    recipe_score = {}
    
    for key,value in smap.items():
        tempScore=0
        for i,dish in enumerate(smap[key]):
            
            try:
                #print(dish)
                tempScore += prefer[dish]
            except:
                tempScore += 0
        recipe_score[key] = tempScore
        
    return recipe_score


def ranking(recipe_rating,recipe_score):
    recipe_rank={}
    
    for key,value in recipe_score.items():
        recipe_rank[key] = value * recipe_rating[key]
    
    ## sorting it OUT
    recipe_rank = sorted(recipe_rank.items(), key=operator.itemgetter(1),reverse=True)
    dishes = []
    for dish in recipe_rank:
        dishes.append(dish[0])
    return dishes
        

def convertUserData(user):
    cv=CountVectorizer()
    word_count_vector = cv.fit_transform(user)
     
    tfidf_transformer = TfidfTransformer()
    tfidf_transformer.fit(word_count_vector)
    
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform(user))
    
    # you only needs to do this once, this is a mapping of index to 
    feature_names=cv.get_feature_names()
    
    #sort the tf-idf vectors set.csv")
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    
    #extract only the top n; n here is 10
    prefer=extract_topn_from_vector(feature_names,sorted_items,10)
    
    return prefer


def get_dish_name(ingredients):
    ## need to store user ingredients
    users = pd.read_csv("./User Data/User - John.csv")
    recipes = pd.read_csv("./Recipe Model/Dataset.csv")
    
    suggestions, grocery, keywords = search(recipes,ingredients)
    
    ## mapping suggestions and its keywords
    smap = dict(zip(suggestions,keywords))
    
    ## still have to check which user preference to take
    prefer = convertUserData(users)
    
    ## sets recipe scores according to the preferences returned in the previous line
    recipe_score = implicit_filtering(prefer,smap)
    
    ## inputs the particular recipe rating given by the user (default 1)
    recipe_rating = {}
    for dish in recipes['Dish_Name']:
        recipe_rating[dish] = 1
        
    ## ranking wrt recipe_rating*recipe_score
    return ranking(recipe_rating,recipe_score)
    
    