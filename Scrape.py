import re
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

startUrl = "https://www.simplyrecipes.com/dinner-recipes-5091433"
listOfRecipes = []
Scraping(startUrl)
print(listOfRecipes)
