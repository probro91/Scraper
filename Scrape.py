#import re
import bs4 as BeautifulSoup
import requests

def Scraping(WebUrl):
    url = WebUrl
    code = requests.get(url)
    plain = code.text
    soup = BeautifulSoup.BeautifulSoup(plain, 'html.parser')
    for link in soup.findAll('a'):
        recipe = link.get('href')
        if "-recipe-" in recipe:
            listOfRecipes.append(recipe)
    listOfRecipes.pop()
    for recipe in listOfRecipes:
        code = requests.get(recipe).text
        soupIngredient = BeautifulSoup.BeautifulSoup(code, 'html.parser')
        listOfIngredients = []
        spans = soupIngredient.find_all("span", attrs={"data-ingredient-name":"true"})
        recipeTitle = soupIngredient.find("h1", {"class": "heading__title"})
        listOfIngredients.append(recipeTitle.text)
        for ingredient in spans:
            listOfIngredients.append(ingredient.text)
        eachUrl.update({recipe:listOfIngredients})
    
eachUrl = {}
startUrl = "https://www.simplyrecipes.com/dinner-recipes-5091433"
startIngredients = ['mushrooms','Italian sausage','lemon juice']
listOfRecipes = []
Scraping(startUrl)

for recipe in eachUrl:
    if all(item in eachUrl[recipe] for item in startIngredients):
        print(eachUrl[recipe])

#print(eachUrl)

