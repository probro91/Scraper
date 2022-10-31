import bs4 as BeautifulSoup # Parses HTMl
import requests # Gets the HTML source code
import mysql.connector # Allows Python to execute SQL commands



def Scraping(WebUrl): # Gets all the recipes for a meal type, along with their url, image url, title, and ingredients
    url = WebUrl
    code = requests.get(url)
    plain = code.text
    soup = BeautifulSoup.BeautifulSoup(plain, 'html.parser')

    #Finds all the liks to the recipes and adds them to a list
    for link in soup.findAll('a'): 
        recipe = link.get('href')
        if "-recipe-" in recipe:
            listOfRecipes.append(recipe)
    listOfRecipes.pop()
    #Parses through all the recipes and gets the ingredeints, image url, and title
    for recipe in listOfRecipes:
        code = requests.get(recipe).text
        soupIngredient = BeautifulSoup.BeautifulSoup(code, 'html.parser')
        listOfIngredients = []
        listOfIngredients.append(recipe)
        spans = soupIngredient.find_all("span", attrs={"data-ingredient-name":"true"})
        recipeTitle = soupIngredient.find("h1", {"class": "heading__title"})
        listOfIngredients.append(recipeTitle.text)
        for imgLink in soupIngredient.findAll('img'):
            image = (str)(imgLink.get('src'))
            if "-LEAD-" in image:
                listOfIngredients.append(image)
                break
        for ingredient in spans:
            listOfIngredients.append(ingredient.text)
        eachUrl.update({recipe:listOfIngredients})
    
eachUrl = {}
mealType = input("What meal type is it? ")
if mealType.lower() == 'breakfast':
    startUrl = "https://www.simplyrecipes.com/breakfast-recipes-5091541"
    mealType = "Breakfast"
elif mealType.lower() == 'lunch':
    startUrl = "https://www.simplyrecipes.com/lunch-recipes-5091263"
    mealType = "Lunch"
elif mealType.lower() == 'dinner':
    startUrl = "https://www.simplyrecipes.com/dinner-recipes-5091433"
    mealType = "Dinner"
elif mealType.lower() == 'dessert':
    startUrl = "https://www.simplyrecipes.com/dessert-recipes-5091513"
    mealType = "Dessert"
elif mealType.lower() == 'snacks and appitizers':
    startUrl = "https://www.simplyrecipes.com/snacks-and-appetizer-recipes-5090762"
    mealType = "SnacksAndApps"
else:
    startUrl = ""

startIngredients = []
startIngredients = (input("Which ingredients do you have? ")).split(", ")
listOfRecipes = []
matchingRecipes = {}
Scraping(startUrl)
#Adds only the recipes with matching ingredietns to the dictionary
for recipe in eachUrl:
    if all(item in eachUrl[recipe] for item in startIngredients):
        matchingRecipes.update({recipe:eachUrl[recipe]})

#for recipe in matchingRecipes.values():
#    print (recipe)
mealTypes = ["Breakfast", "Lunch", "Dinner", "Dessert", "SnacksAndApps"]
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="ScrapsRecipes"
    )

mycursor = mydb.cursor(buffered=True)

for mealType in mealTypes:
    for recipe in eachUrl:
        mycursor.execute("INSERT INTO " + mealType + " (url, name, imageUrl, ingredients) VALUES (%s,%s,%s,%s)", 
        (recipe,eachUrl[recipe][1],eachUrl[recipe][2],str(eachUrl[recipe][3:])))
