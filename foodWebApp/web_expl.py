from flask import Flask, request
from flask_restful import Resource, Api

import re
import csv
import sys
import json
import random
from datetime import datetime
import numpy as np
import pandas as pd
from random import choice



app = Flask(__name__)
api = Api(app)

app.debug = True

class Explain(Resource):
    def get(self):

        #---
        # Explanation functions definitions
        #---

        """
        The Explanation function Popularity returns a static string
        saying that the recipe is very popular in the community.
        """
        def popularity_one(recipeName):
            explanation = ""
            explanation = "I suggest you " + recipeName + \
                " since it is very popular in the community."
            return explanation

        """
        The Explanation function Popularity compares the rating count of the
        two recipes and returns a string saying that a recipe is more
        popular than the other.
        """
        def popularity_two(recipeA_name, recipeB_name, recipeA_rc, recipeB_rc):
            explanation = ""

            if(recipeA_rc > recipeB_rc):
                explanation = recipeA_name + " is more popular than " + recipeB_name + " in the community."
            if(recipeB_rc > recipeA_rc):
                explanation = recipeB_name + " is more popular than " + recipeA_name + " in the community."
            if(recipeA_rc == recipeB_rc):
                explanation = recipeA_name + " is as popular as " + recipeB_name + " in the community."
                
            return explanation

        """
        The explanation function foodGoals_one take in input the name of the recipe,
        the user goal (lose -> lose weight, gain -> gain weight, no -> no goals)
        and the recipe calories. It returns a string saying that the recipe is
        good related to the goal of the user.
                    
        """
        def foodGoals_one(recipeName, user_goal, recipe_calories):
            explanation = ""
            explanation = recipeName + " has " + recipe_calories + " calories. "
            
            if(user_goal == "lose"):
                explanation += "It is a good choice, since you want to lose weight."
            elif(user_goal == "gain"):
                explanation += "It is a good choice, since you want to gain weight."
            elif(user_goal == "no"):
                explanation += "The average calorie intake for a person like you is 1900 calories."
            return explanation

        """
        The explanation function foodGoals_two compares the amount of calories of recipe A
        and Recipe B, and based on the user goal
        (lose -> lose weight, gain -> gain weight, no -> no goals)
        suggests the better recipe in terms of calories. If the user has no goals, then
        the output will be only the comparison of the amount of calories.
        """
        def foodGoals_two(user_goal, recipeA_name, recipeB_name, recipeA_calories, recipeB_calories):
            explanation = ""

            if(recipeA_calories > recipeB_calories):
                if(user_goal == "lose"):
                    explanation = recipeB_name + " has less calories (" + str(recipeB_calories) + " Kcal) than " + recipeA_name + " (" + str(recipeA_calories) + " Kcal). "
                    explanation += "It can help you reaching your goal of losing weight."

                elif(user_goal == "gain"):
                    explanation = recipeA_name + " has more calories (" + str(recipeA_calories) + " Kcal) than " + recipeB_name + " (" + str(recipeB_calories) + " Kcal). "
                    explanation += "It can help you reaching your goal of gaining weight."

                elif(user_goal == "no"):
                    explanation = recipeA_name + " has more calories (" + str(recipeA_calories) + " Kcal) than " + recipeB_name + " (" + str(recipeB_calories) + " Kcal). "
                    explanation += "The average calorie intake for a person like you is 1900 calories."

            elif(recipeA_calories < recipeB_calories):

                if(user_goal == "lose"):
                    explanation = recipeA_name + " has less calories (" + str(recipeA_calories) + " Kcal) than " + recipeB_name + " (" + str(recipeB_calories) + " Kcal). "
                    explanation += "It can help you reaching your goal of losing weight."

                elif(user_goal == "gain"):
                    explanation = recipeB_name + " has more calories (" + str(recipeB_calories) + " Kcal) than " + recipeA_name + " (" + str(recipeA_calories) + " Kcal). "
                    explanation += "It can help you reaching your goal of gaining weight."

                elif(user_goal == "no"):
                    explanation = recipeB_name + " has more calories (" + str(recipeB_calories) + " Kcal) than " + recipeA_name + " (" + str(recipeA_calories) + " Kcal). "
                    explanation += "The average calorie intake for a person like you is 1900 calories."

            else:
                explanation = recipeA_name + " is as caloric as " + recipeB_name + ". Both recipes have " + str(recipeA_calories) + " calories (Kcal)."
                explanation += "The average calorie intake for a person like you is 1900 calories."
                
            
            return explanation
        """
        The explanation function foodPreferences_one connects the recipe A with the user
        restriction (vegetarian, lactosefree, glutenfree, lownickel, light).
        The output will be a static string saying that the recipe is suggested because
        of a random restriction chosen among the user preferences.
        """ 
        def foodPreferences_one(name_restriction, description, recipeName):
            explanation = "I suggest you " + recipeName

            explanation += " because you want " + \
                           name_restriction + " recipes and " + description

            return explanation

        """
        The explanation function foodPreferences_two connects Recipe A and Recipe B
        with the user restrictions. The output will be a static string saying
        that the recipes are suggested because
        of a random restriction chosen among the user preferences.
        """
        def foodPreferences_two(name_restriction, description):

            explanation = "I suggest you these recipes " + \
                          "because you want " + \
                          name_restriction + " recipes and " + description

            return explanation

        """
        The explanation function foodFeatures_one outputs the amount of macronutrients
        with labels "low", "medium", and "high". We used the FSA table to set the ranges
        of each macronutrient.
        """

        def foodFeatures_one(recipe_values, nutrients):
            explanation = ""
            small = ""
            great = ""
           
            
            smallList = []
            greatList = []
            
            listNutrients = list(nutrients.keys())
            random.shuffle(listNutrients)

            recipeName = recipe_values["title"]

            for item in listNutrients:
                if(not(np.isnan(recipe_values[item]))):
                    if(recipe_values[item] <= nutrients[item]["RI"]):
                        smallList.append(item)
                    else:
                        greatList.append(item)
        
            
            if (smallList != []):
                small = smallList[0]
                strSmall = small
                
                if(small == "saturatedFat"):
                    strSmall = "saturated fats"
                explanation = recipeName + " has a small amount of " + strSmall + " (" + str(recipe_values[small]) + " gr)" + \
                              " than reference daily intake (" + str(nutrients[small]["RI"]) + " gr)"
                if(greatList != []):
                    great = greatList[0]
                    strGreat = great

                    if(great == "saturatedFat"):
                        strGreat = "saturated fats"
                    explanation += " and an excess of " + strGreat + " (" + str(recipe_values[great]) + " gr)" + \
                                    " than reference daily intake (" + str(nutrients[great]["RI"]) + " gr). "
                else:
                    explanation += " and there isn't higher amount of nutrients than reference daily intake. "
                        
            if (greatList != []):
                great = greatList[0]
                strGreat = great
                
                if(great == "saturatedFat"):
                    strGreat = "saturated fats"
                explanation = recipeName + " has an excess amount of " + strGreat + " (" + str(recipe_values[great]) + " gr)" + \
                              " than reference daily intake (" + str(nutrients[great]["RI"]) + " gr)"
                if(smallList != []):
                    small = smallList[0]
                    strSmall = small

                    if(small == "saturatedFat"):
                        strSmall = "saturated fats"
                    explanation += " and a small amount of " + strSmall + " (" + str(recipe_values[small]) + " gr)" + \
                                    " than reference daily intake (" + str(nutrients[small]["RI"]) + " gr). "
                else:
                    explanation += " and there isn't lower amount of nutrients than reference daily intake. "

            
            return explanation, small, great
           

        """
        The explanation function foodFeatures_two compares nutrients (calories
        and sugars) of the two recipes. 

        """
        def foodFeatures_two(recipeA, recipeB, nutrients):
            recipeA_name = recipeA["title"]
            recipeB_name = recipeB["title"]

            #initialize output values
            explanation = ""
            small = ""
            great = ""
            strSmall = ""
            strGreat = ""

            #collecting the list of nutrients
            """
            calories               
            carbohydrates          
            sugars                 
            proteins               
            fat                    
            saturatedFat           
            fibers                 
            cholesterol            
            sodium
            """

            listNutrients = list(nutrients.keys())

            #randomize the nutrients list
            random.shuffle(listNutrients)
            
            smallList = []
            greatList = []

            for item in listNutrients:
                if(not(np.isnan(recipeA[item])) and not(np.isnan(recipeB[item]))):
                    if(recipeA[item] < recipeB[item]):
                        smallList.append(item)
                    if(recipeA[item] > recipeB[item]):
                        greatList.append(item)

            if(smallList != []):
                small = smallList[0]
                strSmall = small

                if(small == "saturatedFat"):
                    strSmall = "saturated fats"
                explanation = recipeA_name + " has a lower amount of " + \
                                strSmall + " (" + str(recipeA[small]) + \
                                " gr)"  
                if(greatList != []):
                    great = greatList[0]
                    strGreat = great

                    if(great == "saturatedFat"):
                        strGreat = "saturated fats"
                        
                    explanation += " and a higher amount of " + strGreat + \
                                   " (" + str(recipeA[great]) + " gr) than " + \
                                   recipeB_name + \
                                   "(" + strSmall + ": " + str(recipeB[small]) + \
                                   " gr, " + strGreat + ": " + str(recipeB[great]) + \
                                   " gr). "
                else:
                    explanation += " than " + recipeB_name + " (" + strSmall + ": " + str(recipeB[small]) + " gr), and there isn't higher amount of nutrients than " + recipeB_name + ". "

            if(greatList != []):
                great = greatList[0]
                strGreat = great

                if(great == "saturatedFat"):
                    strGreat = "saturated fats"
                explanation = recipeA_name + " has a higher amount of " + \
                                strGreat + " (" + str(recipeA[great]) + \
                                " gr)"  
                if(smallList != []):
                    small = smallList[0]
                    strSmall = small

                    if(small == "saturatedFat"):
                        strSmall = "saturated fats"
                        
                    explanation += " and a lower amount of " + \
                                  strSmall + " (" + str(recipeA[small]) + \
                                  " gr) than " + recipeB_name + " (" + strGreat + ": "  + \
                                  str(recipeB[great]) + " gr" + ", " + strSmall + ": " + \
                                  str(recipeB[small]) + " gr). "
                else:
                    explanation += " than " + recipeB_name + "(" + strGreat + ": " + \
                                   str(recipeB[great]) + " gr), and there isn't lower amount of nutrients than " + recipeB_name + ". "

            
            return explanation,small,great

        """
        The explanation function userSkills_one take as input the user cooking experience
        and returns a string saying that the recipe is rated by the user in a certain
        difficulty, and it is adequate with the specific user cooking experience.
        """
        def userSkills_one(user_exp, recipe_name):
            explanation = ""
            if(user_exp == 1):
                explanation = recipe_name + " is rated by the users as very simple to prepare, " + \
                              "and it is adequate to your cooking skills, which are very low."
            elif(user_exp == 2):
                explanation = recipe_name + " is rated by the users as simple to prepare, " + \
                              "and it is adequate to your cooking skills, which are low"
            elif(user_exp == 3):
                explanation = recipe_name + " is rated by the users as quite simple to prepare, " + \
                              "and it is adequate to your cooking skills, which are medium"
            elif(user_exp == 4):
                explanation = recipe_name + " is rated by the users as difficult to prepare, " + \
                              "and it is adequate to your cooking skills, which are high"
            elif(user_exp == 5):
                explanation = recipe_name + " is rated by the users as very difficult to prepare, " + \
                              "and it is adequate to your cooking skills, which are very high."
            return explanation


        """
        The explanation function userSkills_two takes as input the user cooking skills and
        the difficulty of the two recommended recipes. These difficulties are converted
        in a numeric format in order to make a comparison and suggest the better recipe in
        terms of user skills and recipe difficulty.
        """
        def userSkills_two(user_skills, recipeA, recipeB, diffA, diffB):
            # molto facile, facile, media, difficile, molto difficile

            explanation = ""

            if(diffA == "molto facile"):
                diffA = 1
            elif(diffA == "facile"):
                diffA = 2
            elif(diffA == "media"):
                diffA = 3
            elif(diffA == "difficile"):
                diffA = 4
            elif(diffA == "molto difficile"):
                diffA = 5

            if(diffB == "molto facile"):
                diffB = 1
            elif(diffB == "facile"):
                diffB = 2
            elif(diffB == "media"):
                diffB = 3
            elif(diffB == "difficile"):
                diffB = 4
            elif(diffB == "molto difficile"):
                diffB = 5

            if(user_skills == 1):
                if(diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are very low."
                elif(diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are very low."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."

            if(user_skills == 2):
                if(diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are low."
                elif(diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are low."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."
            
            if(user_skills == 3):
                if(diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are medium."
                elif(diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are medium."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."

            if(user_skills == 4):
                if(diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are high."
                elif(diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are high."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."

            if(user_skills == 5):
                if(diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are very high."
                elif(diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are very high."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."

            return explanation

        """
        The explanation function foodFeatureHealthRisk_one compares recipe nutrients
        with the medical knowledge about the reference intake (RI). It outputs the
        small and great amount of nutrients and risks associated to a higher assumption
        of the specific nutrient.
        If the "great" nutrient is empty, there will be a risk associated to a higher
        assumption of the "small" nutrient.
        """
        def foodFeatureHealthRisk_one(recipe_values, nutrients):
            explanation = ""
            small = ""
            great = ""
            risk = ""

            explanation,small,great = foodFeatures_one(recipe_values, nutrients)

            if(great != ""):
                risk = random.choice(nutrients[great]["risks"])
                explanation += " Intake too much " + great + \
                               " can increase the risk of " + risk + "."
            else:
                risk = random.choice(nutrients[small]["risks"])
                explanation += " Intake too much " + small + \
                               " can increase the risk of " + risk + "."

            return explanation

        """
        The explanation function foodFeatureHealthRisk_two recall the function
        foodFeatures_two to make a comparison between the nutrients of the two recipes.
        The output is a string telling the risk associated to a higher assumption
        of the great/small nutrient.
        Then, there is a comparison of the amount of calories of the two recipes.
        """

        def foodFeatureHealthRisk_two(recipeA_calories, recipeB_calories, recipeA, recipeB, nutrients):

            explanation = ""
            small = ""
            great = ""
            risk = ""

            recipeA_name = recipeA["title"]
            recipeB_name = recipeB["title"]

            #small and great related to recipeA
            explanation,small,great = foodFeatures_two(recipeA, recipeB, nutrients)

            if(great != ""):
                risk = random.choice(nutrients[great]["risks"])
                explanation += "Intake too much " + great + \
                               " can increase the risk of " + risk + ". "
            if(small != ""):
                risk = random.choice(nutrients[small]["risks"])
                explanation += "Intake too much " + small + \
                               " can increase the risk of " + risk + ". "
                
            if(np.isnan(recipeA_calories) or np.isnan(recipeB_calories)):
                explanation += ""
            
            elif(recipeA_calories > recipeB_calories):
                explanation += "Moreover, " + recipeA_name + " has more calories (" + str(recipeA_calories) + " gr) than " + recipeB_name + " (" + str(recipeB_calories) + " gr). "
                    
            elif(recipeB_calories > recipeA_calories):
                explanation += "Moreover, " + recipeB_name + " has more calories (" + str(recipeB_calories) + " gr) than " + recipeA_name + " (" + str(recipeA_calories) + " gr). "
                    
            else:
                explanation += "Moreover, both recipes have got the same amount of calories (" + str(recipeA_calories) + " gr). "
                explanation += "Reference daily intake of calories is 1900 Kcal." 
                    

            return explanation

        """
        The explanation function foodFeatureHealthBenefits_one recall the foodFeatures_one
        and returns a string with the benefit of the small/great nutrient returned in the
        foodFeatures_one function.
        """

        def foodFeatureHealthBenefits_one(recipe_values, nutrients):

            explanation = ""
            small = ""
            great = ""
            risk = ""

            explanation,small,great = foodFeatures_one(recipe_values, nutrients)

            if(small != ""):
                benefit = random.choice(nutrients[small]["benefits"])
                explanation += " A correct daily intake of " + small + \
                               " can " + benefit + "."
            else:
                benefit = random.choice(nutrients[great]["benefits"])
                explanation += " A correct daily intake of " + great + \
                               " can " + benefit + "."

            return explanation

        """
        The explanation function foodFeatureHealthBenefits_two recall the
        foodFeatures_two function, and return a string with the benefit
        related to the small/great nutrient returned by the foodFeatures_two
        function.
        There is also a comparison between the calories of the two
        recommended recipes.
        """

        def foodFeatureHealthBenefits_two(recipeA,recipeB,nutrients):

            explanation = ""
            small = ""
            great = ""
            risk = ""

            recipeA_name = recipeA["title"]
            recipeB_name = recipeB["title"]
            
            explanation,small,great = foodFeatures_two(recipeA, recipeB, nutrients)

            if(small != ""):
                benefit = random.choice(nutrients[small]["benefits"])
                if(small == 'saturatedFat'):
                    small = 'saturated fats'
                explanation += "A correct daily intake of " + small + \
                               " can " + benefit + ". "
            if(great != ""):
                benefit = random.choice(nutrients[great]["benefits"])
                if(great == 'saturatedFat'):
                    great = 'saturated fats'
                explanation += "A correct daily intake of " + great + \
                               " can " + benefit + ". "

            if(np.isnan(recipeA['calories']) or np.isnan(recipeB['calories'])):
                explanation += ""
            elif(recipeA["calories"]) > recipeB["calories"]:
                explanation += "Furthermore, " + recipeA_name + " has more calories (" + str(recipeA["calories"]) + " gr) than " + recipeB_name + " (" + str(recipeB["calories"]) + " gr). "
                    
            elif(recipeB["calories"]) > recipeA["calories"]:
                explanation += "Furthermore, " + recipeB_name + " has more calories (" + str(recipeB["calories"]) + " gr) than " + recipeA_name + " (" + str(recipeA["calories"]) + " gr). "
                    
            else:
                explanation += "Furthermore, both recipes have got the same amount of calories (" + str(recipeA["calories"]) + " gr). "
                explanation += "Reference daily intake of calories is 1900 Kcal."        

            return explanation

        """
        The explanation function foodFeatureHealthRisks_one recall the foodFeatures_one
        and returns a string with the risk of the small/great nutrient returned in the
        foodFeatures_one function.
        """

        def userFeatureHealthRisk_one(user, recipe_values, nutrients):
                    
            explanation, small, great = foodFeatures_one(recipe_values, nutrients)

            if(user["Mood"] == 'bad' or user["Mood"] == 'neutral' or user["Depressed"] == 'yes' or user["Stressed"] == 'yes'):
                listMood = ["sugars","carbohydrates","proteins"]
                if(great in listMood):
                    explanation += "An excess of " + great + " can swing your mood. "
                    
            if(user["BMI"] == "lower"):
                explanation += "It may not be able to help you to gain weight. "
            elif(user["BMI"] == "over"):
                explanation += "It may not be able to help you to lose weight. "
            
            return explanation

        """
        The explanation function foodFeatureHealthRisks_two recall the
        foodFeatures_two function, and return a string with the risk
        related to the small/great nutrient returned by the foodFeatures_two
        function.
        There is also a comparison between the calories of the two
        recommended recipes.
        """
        def userFeatureHealthRisk_two(user, recipeA, recipeB, nutrients):
            smallA = ""
            greatA = ""
            explanation = ""
            
            recipeA_name = recipeA["title"]
            recipeB_name = recipeB["title"]
            explanation, smallA, greatA = foodFeatures_two(recipeA, recipeB, nutrients)


            if(user["Mood"] == 'bad' or user["Mood"] == 'neutral' or user["Depressed"] == 'yes' or user["Stressed"] == 'yes'):
                listMood = ["sugars","carbohydrates","proteins"]
                if(greatA in listMood):
                    explanation += "An excess of " + greatA + " can swing your mood. "
             
            if(user["BMI"] == "lower" and greatA != ""):
                explanation += "It may not be able to help you to gain weight. "
            elif(user["BMI"] == "over" and smallA != ""):
                explanation += "It may not be able to help you to lose weight. "
            

            if(np.isnan(recipeA['calories']) or np.isnan(recipeB['calories'])):
                explanation += ""
            elif(recipeA["calories"]) > recipeB["calories"]:
                explanation += "Also, " +recipeA_name + " has more calories (" + str(recipeA["calories"]) + " gr) than " + recipeB_name + " (" + str(recipeB["calories"]) + " gr)."
                    
            elif(recipeB["calories"]) > recipeA["calories"]:
                explanation += "Also, " +recipeB_name + " has more calories (" + str(recipeB["calories"]) + " gr) than " + recipeA_name + " (" + str(recipeA["calories"]) + " gr)."
                    
            else:
                explanation += "Also, both recipes have got the same amount of calories (" + str(recipeA["calories"]) + " gr). "
                explanation += "Reference daily intake of calories is 1900 Kcal." 		
            
            return explanation

        """
        The explanation function userFeatureHealthBenefits_one connects the recipe A with the user characteristics
        (BMI, mood, if he or she is depressed/stressed). It returns a string with a benefit related to a nutrient
        that is the output of the foodFeatures_one function.
        """
        def userFeatureHealthBenefits_one(user, recipe_values, nutrients):
            
            explanation, small, great = foodFeatures_one(recipe_values, nutrients)
            
            if(user["Mood"] == 'bad' or user["Mood"] == 'neutral' or user["Depressed"] == 'yes' or user["Stressed"] == 'yes'):
                listMood = ["sugars","carbohydrates","proteins"]
                if(small in listMood):
                    explanation += "A correct intake of " + small + " can improve your mood. "

            if(user["BMI"] == "lower"):
                if(great != ""):
                    explanation += "A correct intake of " + great + " can help you to gain weight. "
                if(small != ""):
                    explanation += "A correct intake of " + small + " can help you to gain weight. "

            elif(user["BMI"] == "over"):
                explanation += "A correct intake of " + small + " can help you to lose weight. "


            return explanation


        """
        The explanation function userFeatureHealthBenefits_two recall the foodFeatures_two
        function, returns a string with a benefit related to the nutrient and the mood / BMI
        of the user.
        There is a comparison of the amount of calories of the two recommeded recipes.
        """
        def userFeatureHealthBenefits_two(user, recipeA, recipeB, nutrients):

            explanation = ""
            smallA = ""
            greatA = ""

            recipeA_name = recipeA["title"]
            recipeB_name = recipeB["title"]
            
            explanation, smallA, greatA = foodFeatures_two(recipeA, recipeB, nutrients)
            
            if(user["Mood"] == 'bad' or user["Mood"] == 'neutral' or user["Depressed"] == 'yes' or user["Stressed"] == 'yes'):
                listMood = ["sugar","carbohydrates","proteins"]
                if(smallA in listMood):
                    explanation += "A correct intake of " + smallA + " can improve your mood. "

            if(user["BMI"] == "lower" and greatA != ""):
                explanation += "A correct intake of " + greatA + " can help you to gain weight. "
            elif(user["BMI"] == "over" and smallA != ""):
                explanation += "A correct intake of " + smallA + " can help you to lose weight. "
            

            if(np.isnan(recipeA['calories']) or np.isnan(recipeB['calories'])):
                explanation += ""
            
            elif(recipeA["calories"]) > recipeB["calories"]:
                explanation += "Moreover, " + recipeA_name + " has more calories (" + str(recipeA["calories"]) + " gr) than " + recipeB_name + " (" + str(recipeB["calories"]) + " gr). "
                    
            elif(recipeB["calories"]) > recipeA["calories"]:
                explanation += "Moreover, " +recipeB_name + " has more calories (" + str(recipeB["calories"]) + " gr) than " + recipeA_name + " (" + str(recipeA["calories"]) + " gr). "
                    
            else:
                explanation += "Moreover, both recipes have got the same amount of calories (" + str(recipeA["calories"]) + " gr). "
                explanation += "Reference daily intake of calories is 1900 Kcal." 

            return explanation

       
        #-----
        # Function get_string_exp returns the explanation of a specific type
        # (popularity, food features, user features, ecc...)
        #---
        def get_str_exp_one(user,
                            recipe_values,
                            type_explanation,
                            listRestrictions,
                            nutrients):
            expl = ''
            recipeName = recipe_values['title']
            
            if type_explanation == 'popularity_one':
                expl = popularity_one(recipeName)
            elif type_explanation == 'foodGoals_one':
                user_goal = user['Goal']
                recipe_calories = str(recipe_values['calories'])
                expl = foodGoals_one(recipeName, user_goal, recipe_calories)
            elif type_explanation == 'foodPreferences_one':
                restriction = ""
                userRestrictions = user["User_restriction"]
                if(userRestrictions is None):
                    expl = ""
                else:
                    flag = 0
                    random.shuffle(listRestrictions)
                    i = 0
                    #encoded(vegetarian,lactosefree,glutenfree,lownichel,light)
                    while(flag == 0 and i < len(listRestrictions)):
                        if(listRestrictions[i] in userRestrictions):
                            restriction = listRestrictions[i]
                            description = restrictions["one"][restriction]
                            if(listRestrictions[i] == "lactosefree"):
                                restriction = "lactose-free"
                            if(listRestrictions[i] == "glutenfree"):
                                restriction = "gluten-free"
                            if(listRestrictions[i] == "lownichel"):
                                restriction = "low-nichel"
                            flag = 1
                            
                        i += 1
                   
                    expl = foodPreferences_one(restriction, description, recipeName)
            elif type_explanation == 'foodFeatures_one':
                expl,_,_ = foodFeatures_one(recipe_values,
                                            nutrients)
            elif type_explanation == 'userSkills_one':
                user_skills = int(user['Cooking_exp'])
                # molto facile, facile, media, difficile, molto difficile
                expl = userSkills_one(user_skills,
                                      recipeName)
            elif type_explanation == 'foodFeatureHealthRisk_one':
                expl = foodFeatureHealthRisk_one(recipe_values, nutrients)
            elif type_explanation == 'foodFeatureHealthBenefits_one':
                        expl = foodFeatureHealthBenefits_one(recipe_values, nutrients)
            elif type_explanation == 'userFeatureHealthRisk_one':
                        expl = userFeatureHealthRisk_one(user, recipe_values, nutrients)
            elif type_explanation == 'userFeatureHealthBenefits_one':
                expl = userFeatureHealthBenefits_one(user, recipe_values, nutrients)
            return expl
        
        def get_str_exp_two(user,
                           recipeA_values,
                           recipeB_values,
                           type_explanation,
                           listRestrictions,
                           nutrients):
            
            expl = ''
            recipeA_name = recipeA_values['title']
            recipeB_name = recipeB_values['title']

                
            if type_explanation == 'popularity_two':
                recipeA_rc = recipeA_values['ratingCount']
                recipeB_rc = recipeB_values['ratingCount']

                expl = popularity_two(recipeA_name, recipeB_name, recipeA_rc, recipeB_rc)
         
            elif type_explanation == 'foodGoals_two':
                user_goal = user['Goal']
                recipeA_calories = recipeA_values['calories']
                recipeB_calories = recipeB_values['calories']
                            
                expl = foodGoals_two(user_goal,
                          recipeA_name,
                          recipeB_name,
                          recipeA_calories,
                          recipeB_calories)
           
            elif type_explanation == 'foodPreferences_two':
                restriction = ""
                userRestrictions = user["User_restriction"]
                if(userRestrictions is None):
                    expl = ""
                else:
                    flag = 0
                    random.shuffle(listRestrictions)
                    i = 0
                    
                    while(flag == 0 and i < len(listRestrictions)):
                        if(listRestrictions[i] in userRestrictions):
                            restriction = listRestrictions[i]
                            description = restrictions["two"][restriction]
                            if(listRestrictions[i] == "lactosefree"):
                                restriction = "lactose-free"
                            if(listRestrictions[i] == "glutenfree"):
                                restriction = "gluten-free"
                            if(listRestrictions[i] == "lownichel"):
                                restriction = "low-nichel"
                            flag = 1
                            
                        i += 1
                   
                    expl = foodPreferences_two(restriction, description)
     
            elif type_explanation == 'foodFeatures_two':
                expl,_,_ = foodFeatures_two(recipeA_values,
                                            recipeB_values,
                                            nutrients)
                
            elif type_explanation == 'userSkills_two':
                user_skills = int(user['Cooking_exp'])
                diffA = recipeA_values['difficulty']
                diffB = recipeB_values['difficulty']
                expl = userSkills_two(user_skills,
                                      recipeA_name,
                                      recipeB_name,
                                      diffA,
                                      diffB)

            elif type_explanation == 'foodFeatureHealthRisk_two':
                recipeA_calories = recipeA_values['calories']
                recipeB_calories = recipeB_values['calories']
                expl = foodFeatureHealthRisk_two(recipeA_calories, recipeB_calories, recipeA_values, recipeB_values, nutrients)
            elif type_explanation == 'foodFeatureHealthBenefits_two':
                        expl = foodFeatureHealthBenefits_two(recipeA_values, recipeB_values, nutrients)       
            elif type_explanation == 'userFeatureHealthRisk_two':
                expl = userFeatureHealthRisk_two(user, recipeA_values, recipeB_values, nutrients)
            elif type_explanation == 'userFeatureHealthBenefits_two':
                expl = userFeatureHealthBenefits_two(user, recipeA_values, recipeB_values, nutrients)
            
            return expl

        #---

        PATH = 'Nutrient.json'
        restrictionsPath = 'Restrictions.json'
        print(request.args.get('imgurl1'))
    
        recipeA_url = request.args.get('imgurl1')
        recipeB_url = request.args.get('imgurl2')
        url_dataset_en = 'dataset_en.csv'


        #df = pd.read_csv(url_dataset_en)
		
        # read file
        with open(PATH, 'r') as myfile:
            data = myfile.read()

        with open(restrictionsPath, 'r') as myfile:
            dataRestrictions = myfile.read()
            
        nutrients = json.loads(data)
        restrictions = json.loads(dataRestrictions)
        listRestrictions = list(restrictions["one"].keys())
      
        df = pd.read_csv(url_dataset_en)

        recipeA_values = {}
        recipeB_values = {}

        for index, row in df.iterrows():
            if(row["imageURL"] == recipeA_url):
                recipeA_values = row
            if(row["imageURL"] == recipeB_url):
                recipeB_values = row

        recipeA_values["sodium"] = recipeB_values["sodium"]/1000
        recipeB_values["sodium"] = recipeB_values["sodium"]/1000

        recipeA_values["cholesterol"] = recipeB_values["cholesterol"]/1000
        recipeB_values["cholesterol"] = recipeB_values["cholesterol"]/1000
                    

        user = {
            'Mood'              : request.args.get('mood'), # bad/good/neutral
            'Stressed'          : request.args.get('stress'), # yes/no
            'Depressed'         : request.args.get('depression'),  # yes/no
            'BMI'               : request.args.get('bmi'), # over/lower/normal
            'Activity'          : request.args.get('activity'), #low/high/normal
            'Goal'              : request.args.get('goal'), #lose/gain/no
            'Sleep'             : request.args.get('sleep'), # low/good
            'User_restriction'  : request.args.get('restr'),
            #encoded(vegetarian,lactosefree,glutenfree,lownichel,light)
            'Prob'              : request.args.get('prob'),
            #encoded(heart,diabete,joint,pressure,chol)
            'Cooking_exp'       : request.args.get('difficulty'), # 1/2/3/4/5
            }

        two_recipes = [  
                "popularity_two",
                "foodGoals_two", 
                "foodPreferences_two",
                "foodFeatures_two",
                "userSkills_two", 
                "foodFeatureHealthRisk_two",  
                "foodFeatureHealthBenefits_two", 
                "userFeatureHealthRisk_two", 
                "userFeatureHealthBenefits_two"
                ]
        
        one_recipe = [
                "popularity_one",
                "foodGoals_one",
                "foodPreferences_one",
                "foodFeatures_one",
                "userSkills_one",
                "foodFeatureHealthRisk_one",
                "foodFeatureHealthBenefits_one",
                "userFeatureHealthRisk_one",
                "userFeatureHealthBenefits_one"

            ]

        random.seed(datetime.now())

        expl = ""
        expls_a = []
        expls_b = []
        expls_ab = []
        list_exp = []

        i = 0
        random.shuffle(one_recipe)
        for type_exp in one_recipe:
            expl = get_str_exp_one(user,
                           recipeA_values,
                           one_recipe[i],
                           listRestrictions,
                           nutrients)
            if (expl != ""):
                expls_a.append(expl)
            i += 1

        expl = ""
        i = 0
        random.shuffle(one_recipe)
        for type_exp in one_recipe:
            expl = get_str_exp_one(user,
                           recipeB_values,
                           one_recipe[i],
                           listRestrictions,
                           nutrients)
            if (expl != ""):
                expls_b.append(expl)
            i += 1

        expl = ""
        i = 0
        random.shuffle(two_recipes)
        for type_exp in two_recipes:
            expl = get_str_exp_two(user,
                           recipeA_values,
                           recipeB_values,
                           two_recipes[i],
                           listRestrictions,
                           nutrients)
            if (expl != ""):
                expls_ab.append(expl)
            i += 1

        
        list_exp.append(expls_a[0])
        list_exp.append(expls_b[0])
        list_exp.append(expls_ab[0])
        
        #list_exp.append(expl)
        	
	#conversion Array to JSON
        json_exp = json.dumps({'explanation':list_exp})
		
		
        return json_exp
        
api.add_resource(Explain, '/exp/')

if __name__ == '__main__':
     app.run(port=5003)
