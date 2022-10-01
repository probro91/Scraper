from bs4 import BeautifulSoup
import requests


url = "https://www.simplyrecipes.com/dubu-jorim-korean-braised-tofu-recipe-6544036"

html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "html.parser")
    
spans = soup.find_all("span", attrs={"data-ingredient-name":"true"})
recipeTitle = soup.find("h1", {"class": "heading__title"})
print(recipeTitle.text)
for ingredient in spans:
    print(ingredient.text)
    

