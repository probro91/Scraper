import re
import bs4 as BeautifulSoup
import requests

def Scraping(WebUrl, function):
    url = WebUrl
    code = requests.get(url)
    plain = code.text
    soup = BeautifulSoup.BeautifulSoup(plain, 'html.parser')
    if function == "Getting recipes":
        for link in soup.findAll('a'):
            recipe = link.get('href')
            if "-recipe-" in recipe:
                listOfRecipes.append(recipe)
        listOfRecipes.pop()
        print(listOfRecipes)
    if function == "Getting ingredients and title":
        spans = soup.find_all("span", attrs={"data-ingredient-name":"true"})
        recipeTitle = soup.find("h1", {"class": "heading__title"})
        print(recipeTitle.text)
        for ingredient in spans:
            print(ingredient.text)
    

startUrl = "https://www.simplyrecipes.com/dinner-recipes-5091433"
listOfRecipes = []
Scraping(startUrl, "Getting recipes")
for recipe in listOfRecipes:
    Scraping(recipe, "Getting ingredients and title")

