#import re
import bs4 as BeautifulSoup
import requests
import time

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
        imageURLs = soupIngredient.find_all('img')
        for imgLink in imageURLs:
            image = str(imgLink.get('src'))
            if "-LEAD-" in image:
                listOfIngredients.append(image)
                break
        for ingredient in spans:
            listOfIngredients.append(ingredient.text)
        eachUrl.update({recipe:listOfIngredients})
    #print("Time after ingredients" + str(time.time_ns()))
    
eachUrl = {}
mealType = input("Do you want 'Breakfast', 'Lunch', 'Dinner', 'Dessert, or 'Snacks&Apps' recipes? ")
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
startIngredients = ['mushrooms']
listOfRecipes = []
Scraping(startUrl)

for recipe in eachUrl:
    if all(item in eachUrl[recipe] for item in startIngredients):
        print(eachUrl[recipe])
#print("Time after compairing" + str(time.time_ns()))

#print(eachUrl)

