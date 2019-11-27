from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pandas as pd
import operator
from utilities import get_user_details

import csv  

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
    filterkey = []
    keywords = []
    shopping = dict()
    
    for i in range(len(data)):
        temp = data.Ingredients[i]
        res = [x.strip() for x in temp.split(',')]
        score = len(set(res) - set(ingredients))
        if(score == 0):
            #print("Best Match - ", data.Dish_Name[i])
            suggestions.append(data.Dish_Name[i])
            cv = CountVectorizer()
            attri = data.Cuisine[i] + ' , ' + data.Difficulty[i] + ' , ' + data.Meat[i]+ ' , ' + data.Spicyness[i] + ' , ' + data.Price_of_Ingredients[i]
            attri = [attri]

            filter_attri= data.Veg_Nonveg[i]+ ' , ' + data.Vegan[i] + ' , ' + data.Allergy[i]
            filter_attri=[filter_attri]
            print(filter_attri)

            cv.fit(attri)
            keywords.append(list(cv.vocabulary_.keys()))
            #print(keywords)

            cv.fit(filter_attri)
            filterkey.append(list(cv.vocabulary_.keys()))
            
            
        if(score <= 5 and score >= 1):
            #print(data.Dish_Name[i])
            grocery.append(data.Dish_Name[i])
            # print(set(res) - set(ingredients))
            shopping[data.Dish_Name[i]] = list(set(res) - set(ingredients))

    return suggestions, filterkey, keywords, shopping



def implicit_scoring(prefer,smap):
    recipe_score = {}

    for key, value in smap.items():
        tempScore=0
        for i, dish in enumerate(smap[key]):
            
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
    recipe_rank = sorted(recipe_rank.items(), key=operator.itemgetter(1), reverse=True)
    return recipe_rank
        


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
    prefer=extract_topn_from_vector(feature_names, sorted_items,10)
    
    return prefer


def user_update(recipe="Irish Stew ",username = "sujit"):
    data = pd.read_csv("./Recipe Model/Updated_Dataset.csv")
    
    attri = ""
    for i in range(len(data)):

        if recipe in list(data.Dish_Name):
            # print("inside")
            attri = str(data.Cuisine[i] + ' ' + data.Difficulty[i] + ' ' + data.Meat[i]+ ' ' + data.Spicyness[i] + ' ' + data.Price_of_Ingredients[i])
    
    add_data = ''
    for one in attri.split(" "):
        add_data = add_data+str(one)+" "
    # print("attributes to be added",add_data)
    
    try:
        with open("./User Data/" + username + ".csv","r") as file:
            data = file.readlines()

        # print("data",data,type(data))
        user_File = str(data[0]).replace("\n"," ")

    except:
        pass
        with open("./User Data/username.csv","r") as file:
            data = file.readlines()

        # print("data",data,type(data))
        user_File = str(data[0]).replace("\n"," ")


    # print("\n\n",user_File)
    user_metadata = str(user_File)+" "+str(add_data)
    user_metadata = user_metadata.replace(',',' ')
    print("user metadata",user_metadata)

    
    with open("./User Data/" + username + ".csv ", 'w') as file:
        file.write(user_metadata)
    
    # user_File.write(additional_attributes)
    # user_File.close()

    
def get_dish_name(ingredients,username):
    ## need to store user ingredients
    print("username",username)
    allergy2 =''

    try:
        users = pd.read_csv("./User Data/"+username+".csv")
    except:
        users = pd.read_csv("./User Data/username.csv")
    finally:
        # users = pd.read_csv("./User Data/username.csv")
        recipes = pd.read_csv("./Recipe Model/Updated_Dataset.csv")

        ## allergies
        user_attri = get_user_details()
        for user in user_attri:
            if username in user:
                allergy2 = user[3]
                print("allergy",allergy2)
    

    suggestions, filterkey, keywords, shopping = search(recipes,ingredients)
    
    ## mapping suggestions and its keywords
    smap = dict(zip(suggestions,keywords))

    # print("filterkey",filterkey,"keywords",keywords)
    ## making the filter map
    filtermap = dict(zip(suggestions,filterkey))
    # print("\n\nfiltermap",filtermap)
    
    ## filtering
    try:
        for fkey,fvalue in filtermap.items():
            # print("allergies shown",allergy2)
            if allergy2 in fvalue:
                print("\n\n",fkey,"is not suitable\n\n")
                del smap[fkey]
    except:
        pass
        # smap = dict(zip(suggestions,keywords))
        print("Exception")

    ## still have to check which user preference to take
    # print(users)
    prefer = convertUserData(users)
    # print("\nprefer - User preferences \n",prefer)
 
    ## sets recipe scores according to the preferences returned in the previous line
    recipe_score = implicit_scoring(prefer,smap)
    

    ## inputs the particular recipe rating given by the user (default 1)
    
    recipe_rating = {}
    for dish in recipes['Dish_Name']:
        recipe_rating[dish] = 1
     
    ## ranking wrt recipe_rating*recipe_score
    # print(recipe_rating,recipe_score)
    recipe_rank = dict(ranking(recipe_rating,recipe_score))
    # print("RecipeRank",recipe_rank)

    return recipe_rank,prefer,shopping
    # return ranking(recipe_rating,recipe_score)

    
## get_dish name is main function
if __name__ == '__main__':
    pass
    user_update()