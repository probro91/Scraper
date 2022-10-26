from flask import Blueprint, render_template, request # Python integration with making websites
import mysql.connector # Allows Python to execute SQL commands

# Connects to mySQL database and server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="ScrapsRecipes"
    )

mycursor = mydb.cursor(buffered=True)

result = ""
data = ""

htmlCode = []

tbl = "<tr><td>URL</td><td>Title</td><td>Image</td><td>Ingredients</td></tr>"
htmlCode.append(tbl)
"""
Creates the database:
mycursor.execute("CREATE DATABASE ScrapsRecipes") 

Creates the tables for each meal type:
mealTypes = ["Breakfast", "Lunch", "Dinner", "Dessert", "SnacksAndApps"]
for mealType in mealTypes:
    mycursor.execute("CREATE TABLE " + mealType + " (url VARCHAR(200), 
    name VARCHAR(150), 
    imageUrl VARCHAR(300), 
    ingredients VARCHAR(500), 
    recipeID int PRIMARY KEY AUTO_INCREMENT)")

Adds all the recipes and their ingredients into their corresponding tables:
for mealType in mealTypes:
    for recipe in eachUrl:
        mycursor.execute("INSERT INTO " + mealType + " (url, name, imageUrl, ingredients) 
        VALUES (%s,%s,%s,%s)", (recipe,eachUrl[recipe][1],eachUrl[recipe][2],str(eachUrl[recipe][3:])))
"""

views = Blueprint('views', __name__)


@views.route('/', methods=["GET","POST"])
def home():
    if request.method == "POST":
        mealType = (str)(request.form["mealType"])
        startIngredients = []
        startIngredients = ((str)(request.form["Ingredients"])).split(", ")
        sql = "SELECT * FROM " + mealType + " WHERE ingredients LIKE '%" + startIngredients[0] + "%'"
        for x in range(1,len(startIngredients)):
            sql += " AND ingredients LIKE '%" + startIngredients[x] + "%'"
        mycursor.execute(sql)
        return render_template("base.html", output_data = mycursor)
    if request.method == "GET":
        mycursor.execute("SELECT * FROM Breakfast")
        return render_template("base.html", output_data = [])
