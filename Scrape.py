#import re
from flask import Flask, render_template, request
import bs4 as BeautifulSoup
import requests
import time


app = Flask(__name__)



def Scraping(WebUrl):
    #print("Time before recipes" + str(time.time_ns()))
    url = WebUrl
    code = requests.get(url)
    plain = code.text
    soup = BeautifulSoup.BeautifulSoup(plain, 'html.parser')
    for link in soup.findAll('a'):
        recipe = link.get('href')
        if "-recipe-" in recipe:
            listOfRecipes.append(recipe)
    listOfRecipes.pop()
    #print("Time after recipes" + str(time.time_ns()))
    for recipe in listOfRecipes:
        code = requests.get(recipe).text
        soupIngredient = BeautifulSoup.BeautifulSoup(code, 'html.parser')
        listOfIngredients = []
        spans = soupIngredient.find_all("span", attrs={"data-ingredient-name":"true"})
        recipeTitle = soupIngredient.find("h1", {"class": "heading__title"})
        listOfIngredients.append(recipeTitle.text)
        for imgLink in soupIngredient.findAll('img'):
            image = imgLink.get('src')
            if "-LEAD-" in image:
                listOfIngredients.append(image)
        for ingredient in spans:
            listOfIngredients.append(ingredient.text)
        eachUrl.update({recipe:listOfIngredients})
    #print("Time after ingredients" + str(time.time_ns()))
    
eachUrl = {}
mealType = (str)(request.form["mealType"])
if mealType.lower() == 'breakfast':
    startUrl = "https://www.simplyrecipes.com/breakfast-recipes-5091541"
elif mealType.lower() == 'lunch':
    startUrl = "https://www.simplyrecipes.com/lunch-recipes-5091263"
elif mealType.lower() == 'dinner':
    startUrl = "https://www.simplyrecipes.com/dinner-recipes-5091433"
elif mealType.lower() == 'dessert':
    startUrl = "https://www.simplyrecipes.com/dessert-recipes-5091513"
elif mealType.lower() == 'snacks&apps':
    startUrl = "https://www.simplyrecipes.com/snacks-and-appetizer-recipes-5090762"
else:
    startUrl = ""
startIngredients = ((str)(request.form["Ingredients"])).split(", ")
listOfRecipes = []
Scraping(startUrl)
for recipe in eachUrl:
    if not all(item in eachUrl[recipe] for item in startIngredients):
        eachUrl.delete(recipe)

#print("Time after compairing" + str(time.time_ns()))

#print(eachUrl)
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("base.html", ingredients=eachUrl)
