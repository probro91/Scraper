from bs4 import BeautifulSoup
import requests


url = "https://www.simplyrecipes.com/dubu-jorim-korean-braised-tofu-recipe-6544036"

html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "html.parser")
 
# Find the specifc div tag
datas = soup.find("div", id="structured-ingredients_1-0").find("span")
 


# Iterate through all li tags
#for data in datas:
    # Get text from each tag
    #print(data.text)
 

