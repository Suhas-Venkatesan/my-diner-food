from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re

filename  = "the-diner-dinner.csv"
f = open(filename, "w")
headers = "Food name, Calories, Serving size, Serving size with units(each/oz), Total fats(g), Saturated fat(g), Trans fat(g),"
headers += "Cholesterol(mg), Sodium(mg), Total carbs(g), Dietary fiber(g), Total Sugar(g), Added Sugar(g), Protein(g), Ingredients, Allergen List,"
headers += "hasEgg, hasSoy, hasDairy, hasGluten, hasFish_or_shellfish, hasTreeNuts, hasPeanuts, isVegan\n"
f.write(headers) 

#For loop to iterate through 29 days of menus in February
for i in range(1,29):
    base_url = "http://nutrition.umd.edu/longmenu.aspx?sName=%3cfont+style%3d%22color%3aRed%22%3eDining+%40+Maryland%3c%2ffont%3e&locationNum=04&locationName=%3cfont+style%3d%22color%3aRed%22%3eThe+Diner%3c%2ffont%3e&naFlag=1&WeeksMenus=This+Week%27s+Menus&dtdate=2%2f" + str(i) + "%2f2020&mealName=Dinner"
    #opening up connection, grabbing the page
    uClient = uReq(base_url)
    page_html = uClient.read()
    uClient.close()

    #parsing html file
    page_soup = soup(page_html, "html.parser")

    food_link_container = page_soup.findAll("div",{"class":"longmenucoldispname"})

    #Loops through all food items on the menu
    for food_link in food_link_container:

        my_url =  "http://nutrition.umd.edu/" + food_link.a.get('href')

        #opening up connection, grabbing the page
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()

        #html parsing
        page_soup = soup(page_html, "html.parser")

        if page_soup.find("div",{"class":"nutfactsservsize"}) is not None:
            #stores food name
            food_name = page_soup.find("div",{"class":"labelrecipe"}).text
            print(food_name)

            #grabs the serving size and stores it 
            serving_container = page_soup.findAll("div",{"class":"nutfactsservsize"})
            serving_size = serving_container[1].text

            if "oz" in serving_size:
                serving_size_numeric = re.sub("oz","", serving_size)  
                
                if "1/2" in serving_size_numeric:
                    serving_size_numeric = re.sub("1/2 oz","0.5", serving_size)

                if "1/4" in serving_size_numeric:
                    serving_size_numeric = re.sub("1/4 oz","0.25", serving_size)

            elif "each" in serving_size:
                serving_size_numeric = re.sub("each","", serving_size)

                if "1/2" in serving_size_numeric:
                    serving_size_numeric = re.sub("1/2","0.5", serving_size)

                if "1/4" in serving_size_numeric:
                    serving_size_numeric = re.sub("1/4","0.25", serving_size)

            #grabs the calories and stores it 
            calorie_container = page_soup.find("td",{"class":"nutfactscaloriesval"})
            calories = calorie_container.text

            #grabs all the nutrient containers 
            nutrients_container = page_soup.findAll("span",{"class":"nutfactstopnutrient"})

            #stores total fat data 
            total_fats = re.sub("Total Fat\xa0","", nutrients_container[0].text)
            total_fats_numeric = re.sub("g","", total_fats)

            #stores total carbohydrates data 
            total_carbs = re.sub("Total Carbohydrate.\xa0","", nutrients_container[2].text)
            total_carbs_numeric = re.sub("g","", total_carbs)

            #stores saturated fat data
            saturated_fat = re.sub("\xa0\xa0\xa0\xa0Saturated Fat\xa0","", nutrients_container[4].text)
            saturated_fat_numeric = re.sub("g","", saturated_fat)

            #stores dietary fiber data
            dietary_fiber = re.sub("\xa0\xa0\xa0\xa0Dietary Fiber\xa0","", nutrients_container[6].text)
            dietary_fiber_numeric = re.sub("g","", dietary_fiber)

            #stores trans fat data 
            trans_fat = re.sub("\xa0\xa0\xa0\xa0Trans Fat\xa0","", nutrients_container[8].text)
            trans_fat_numeric = re.sub("g","", trans_fat)

            #stores total sugars data
            total_sugars = re.sub("\xa0\xa0\xa0\xa0Total Sugars\xa0","", nutrients_container[10].text)
            total_sugars_numeric = re.sub("g","", total_sugars)

            #stores cholesterol data 
            cholesterol = re.sub("Cholesterol\xa0","", nutrients_container[12].text)
            cholesterol_numeric = re.sub("mg","", cholesterol)

            #stores added sugar data 
            added_sugar = re.sub("\xa0\xa0\xa0\xa0\xa0\xa0Includes","", nutrients_container[14].text)
            added_sugar_numeric = re.sub("g Added Sugars","", added_sugar)

            #stores sodium data
            sodium = re.sub("Sodium\xa0","", nutrients_container[16].text)
            sodium_numeric = re.sub("mg","", sodium)

            #stores protein data
            protein = re.sub("Protein\xa0","", nutrients_container[18].text)
            protein_numeric = re.sub("g","", protein)

            #stores ingredient data
            ingredients = page_soup.find("span", {"class":"labelingredientsvalue"}).text

            #stores allergen data
            allergens = page_soup.find("span", {"class":"labelallergensvalue"}).text

            #allergens are set to false by default
            hasEgg = False
            hasSoy = False
            hasDairy = False
            hasGluten = False
            hasFish_or_shellfish = False
            hasTreeNuts = False
            hasPeanuts = False
            isVegan = False

            #checks if food has certain allergens 
            if "Eggs" in allergens:
                hasEgg = True
            elif "Soybeans" in allergens:
                hasSoy = True
            elif "Milk" in allergens:
                hasDairy = True
            elif "Wheat" in allergens:
                hasGluten = True
            elif "Fish" in allergens:
                hasFish_or_shellfish = True
            elif "Tree Nuts" in allergens:
                hasTreeNuts = True
            elif "Peanuts" in allergens:  
                hasPeanuts = True  
            elif "Vegan" in allergens:
                isVegan = True

            #writes data to CSV file
            f.write(food_name + "," + calories + "," + serving_size_numeric + "," + serving_size + "," +  total_fats_numeric + "," +
                            saturated_fat_numeric + "," + trans_fat_numeric + "," + cholesterol_numeric + ","  + sodium_numeric + "," +  total_carbs_numeric + "," + dietary_fiber_numeric + "," + 
                            total_sugars_numeric + "," + added_sugar_numeric + "," + protein_numeric + "," + ingredients.replace(",", "|") + "," + allergens.replace(",", "|") + "," + str(hasEgg) + "," + str(hasSoy) + "," + str(hasDairy) + "," +
                            str(hasGluten) + "," + str(hasFish_or_shellfish) + "," + str(hasTreeNuts) + "," + str(hasPeanuts) + "," + str(isVegan) + "\n")


































