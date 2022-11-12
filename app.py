from flask import Flask, render_template, request
import json

application = Flask(__name__)
mealTypes = ["Breakfast", "Lunch", "Dinner", "Dessert", "SnacksAndApps"]

@application.route('/', methods=["GET","POST"])
def home():
  if request.method == "POST":
    startIngredients = []
    startIngredients = ((str)(request.form["Ingredients"])).split(", ")
    mealTypeInput = (str)(request.form["mealType"])
    if mealTypeInput == "Any":
      for mealType in mealTypes:
        f = open(""+mealType+".json")
        recipeList = json.load(f)
        data = []
        for recipe in recipeList:
          for item in recipeList[recipe]:
            for ingredient in startIngredients:
              if ingredient in item and recipeList[recipe] not in data:
                data.append(recipeList[recipe])
    elif mealTypeInput == "Selection":
      return render_template("base.html", output_data = [])
    else:
      f = open(""+mealTypeInput+".json")
      recipeList = json.load(f)
      data = []
      for recipe in recipeList:
        for item in recipeList[recipe]:
          for ingredient in startIngredients:
            if ingredient in item and recipeList[recipe] not in data:
              data.append(recipeList[recipe])
    return render_template("base.html", output_data = data)
  if request.method == "GET":
    return render_template("base.html", output_data = [])

if __name__=="__main__":
  application.run(debug=True)