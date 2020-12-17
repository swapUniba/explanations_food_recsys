from functools import reduce

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

        # ---
        # Explanation functions definitions
        # ---

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

            if (recipeA_rc > recipeB_rc):
                explanation = recipeA_name + " is more popular than " + recipeB_name + " in the community."
            if (recipeB_rc > recipeA_rc):
                explanation = recipeB_name + " is more popular than " + recipeA_name + " in the community."
            if (recipeA_rc == recipeB_rc):
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
            explanation = recipeName + " has " + recipe_calories + " Kcal. "

            if (user_goal == "lose"):
                explanation += "It is a good choice, since you want to lose weight."
            elif (user_goal == "gain"):
                explanation += "It is a good choice, since you want to gain weight."
            elif (user_goal == "no"):
                explanation += "The average calorie intake for a person like you is 1900 Kcal."
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

            if (recipeA_calories > recipeB_calories):
                if (user_goal == "lose"):
                    explanation = recipeB_name + " has less calories (" + str(
                        recipeB_calories) + " Kcal) than " + recipeA_name + " (" + str(recipeA_calories) + " Kcal). "
                    explanation += "It can help you reaching your goal of losing weight."

                elif (user_goal == "gain"):
                    explanation = recipeA_name + " has more calories (" + str(
                        recipeA_calories) + " Kcal) than " + recipeB_name + " (" + str(recipeB_calories) + " Kcal). "
                    explanation += "It can help you reaching your goal of gaining weight."

                elif (user_goal == "no"):
                    explanation = recipeA_name + " has more calories (" + str(
                        recipeA_calories) + " Kcal) than " + recipeB_name + " (" + str(recipeB_calories) + " Kcal). "
                    explanation += "The average calorie intake for a person like you is 1900 Kcal."

            elif (recipeA_calories < recipeB_calories):

                if (user_goal == "lose"):
                    explanation = recipeA_name + " has less calories (" + str(
                        recipeA_calories) + " Kcal) than " + recipeB_name + " (" + str(recipeB_calories) + " Kcal). "
                    explanation += "It can help you reaching your goal of losing weight."

                elif (user_goal == "gain"):
                    explanation = recipeB_name + " has more calories (" + str(
                        recipeB_calories) + " Kcal) than " + recipeA_name + " (" + str(recipeA_calories) + " Kcal). "
                    explanation += "It can help you reaching your goal of gaining weight."

                elif (user_goal == "no"):
                    explanation = recipeB_name + " has more calories (" + str(
                        recipeB_calories) + " Kcal) than " + recipeA_name + " (" + str(recipeA_calories) + " Kcal). "
                    explanation += "The average calorie intake for a person like you is 1900 Kcal."

            else:
                explanation = recipeA_name + " is as caloric as " + recipeB_name + ". Both recipes have " + str(
                    recipeA_calories) + " Kcal."
                explanation += "The average calorie intake for a person like you is 1900 Kcal."

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
                if (not (np.isnan(recipe_values[item]))):
                    if (recipe_values[item] <= nutrients[item]["RI"]):
                        smallList.append(item)
                    else:
                        greatList.append(item)

            if (smallList != []):
                small = smallList[0]
                strSmall = small

                if (small == "saturatedFat"):
                    strSmall = "saturated fats"
                explanation = recipeName + " has a smaller amount of " + strSmall + " (" + str(
                    recipe_values[small]) + " gr)" + \
                              " than reference daily intake (" + str(nutrients[small]["RI"]) + " gr)"
                if (greatList != []):
                    great = greatList[0]
                    strGreat = great

                    if (great == "saturatedFat"):
                        strGreat = "saturated fats"
                    explanation += " and an excess of " + strGreat + " (" + str(recipe_values[great]) + " gr)" + \
                                   " than reference daily intake (" + str(nutrients[great]["RI"]) + " gr). "
                else:
                    explanation += " and there isn't higher amount of nutrients than reference daily intake. "

            if (greatList != []):
                great = greatList[0]
                strGreat = great

                if (great == "saturatedFat"):
                    strGreat = "saturated fats"
                explanation = recipeName + " has an excess amount of " + strGreat + " (" + str(
                    recipe_values[great]) + " gr)" + \
                              " than reference daily intake (" + str(nutrients[great]["RI"]) + " gr)"
                if (smallList != []):
                    small = smallList[0]
                    strSmall = small

                    if (small == "saturatedFat"):
                        strSmall = "saturated fats"
                    explanation += " and a smaller amount of " + strSmall + " (" + str(recipe_values[small]) + " gr)" + \
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

            # initialize output values
            explanation = ""
            small = ""
            great = ""
            strSmall = ""
            strGreat = ""

            # collecting the list of nutrients
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

            # randomize the nutrients list
            random.shuffle(listNutrients)

            smallList = []
            greatList = []

            for item in listNutrients:
                if (not (np.isnan(recipeA[item])) and not (np.isnan(recipeB[item]))):
                    if (recipeA[item] < recipeB[item]):
                        smallList.append(item)
                    if (recipeA[item] > recipeB[item]):
                        greatList.append(item)

            if (smallList != []):
                small = smallList[0]
                strSmall = small

                if (small == "saturatedFat"):
                    strSmall = "saturated fats"
                explanation = recipeA_name + " has a lower amount of " + \
                              strSmall + " (" + str(recipeA[small]) + \
                              " gr)"
                if (greatList != []):
                    great = greatList[0]
                    strGreat = great

                    if (great == "saturatedFat"):
                        strGreat = "saturated fats"

                    explanation += " and a higher amount of " + strGreat + \
                                   " (" + str(recipeA[great]) + " gr) than " + \
                                   recipeB_name + \
                                   "(" + strSmall + ": " + str(recipeB[small]) + \
                                   " gr, " + strGreat + ": " + str(recipeB[great]) + \
                                   " gr). "
                else:
                    explanation += " than " + recipeB_name + " (" + strSmall + ": " + str(
                        recipeB[small]) + " gr), and there isn't higher amount of nutrients than " + recipeB_name + ". "

            if (greatList != []):
                great = greatList[0]
                strGreat = great

                if (great == "saturatedFat"):
                    strGreat = "saturated fats"
                explanation = recipeA_name + " has a higher amount of " + \
                              strGreat + " (" + str(recipeA[great]) + \
                              " gr)"
                if (smallList != []):
                    small = smallList[0]
                    strSmall = small

                    if (small == "saturatedFat"):
                        strSmall = "saturated fats"

                    explanation += " and a lower amount of " + \
                                   strSmall + " (" + str(recipeA[small]) + \
                                   " gr) than " + recipeB_name + " (" + strGreat + ": " + \
                                   str(recipeB[great]) + " gr" + ", " + strSmall + ": " + \
                                   str(recipeB[small]) + " gr). "
                else:
                    explanation += " than " + recipeB_name + "(" + strGreat + ": " + \
                                   str(recipeB[
                                           great]) + " gr), and there isn't lower amount of nutrients than " + recipeB_name + ". "

            return explanation, small, great

        """
        The explanation function userSkills_one take as input the user cooking experience
        and returns a string saying that the recipe is rated by the user in a certain
        difficulty, and it is adequate with the specific user cooking experience.
        """

        def userSkills_one(user_exp, recipe_name):
            explanation = ""
            if (user_exp == 1):
                explanation = recipe_name + " is rated by the users as very simple to prepare, " + \
                              "and it is adequate to your cooking skills, which are very low."
            elif (user_exp == 2):
                explanation = recipe_name + " is rated by the users as simple to prepare, " + \
                              "and it is adequate to your cooking skills, which are low"
            elif (user_exp == 3):
                explanation = recipe_name + " is rated by the users as quite simple to prepare, " + \
                              "and it is adequate to your cooking skills, which are medium"
            elif (user_exp == 4):
                explanation = recipe_name + " is rated by the users as difficult to prepare, " + \
                              "and it is adequate to your cooking skills, which are high"
            elif (user_exp == 5):
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

            if (diffA == "molto facile"):
                diffA = 1
            elif (diffA == "facile"):
                diffA = 2
            elif (diffA == "media"):
                diffA = 3
            elif (diffA == "difficile"):
                diffA = 4
            elif (diffA == "molto difficile"):
                diffA = 5

            if (diffB == "molto facile"):
                diffB = 1
            elif (diffB == "facile"):
                diffB = 2
            elif (diffB == "media"):
                diffB = 3
            elif (diffB == "difficile"):
                diffB = 4
            elif (diffB == "molto difficile"):
                diffB = 5

            if (user_skills == 1):
                if (diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are very low."
                elif (diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are very low."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."

            if (user_skills == 2):
                if (diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are low."
                elif (diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are low."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."

            if (user_skills == 3):
                if (diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are medium."
                elif (diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are medium."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."

            if (user_skills == 4):
                if (diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are high."
                elif (diffB < diffA):
                    explanation = recipeB + " is rated by the users as easier to prepare than " + recipeA + \
                                  ", and this is adequate with your cooking skills, which are high."
                else:
                    explanation = recipeA + " is as easy to prepare as " + recipeB + "."

            if (user_skills == 5):
                if (diffA < diffB):
                    explanation = recipeA + " is rated by the users as easier to prepare than " + recipeB + \
                                  ", and this is adequate with your cooking skills, which are very high."
                elif (diffB < diffA):
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

            explanation, small, great = foodFeatures_one(recipe_values, nutrients)

            if (great != ""):
                risk = random.choice(nutrients[great]["risks"])
                if (great == "saturatedFat"):
                    great = "saturated fats"
                explanation += " Intake too much " + great + \
                               " can increase the risk of " + risk + "."
            elif small != "":
                risk = random.choice(nutrients[small]["risks"])
                if (small == "saturatedFat"):
                    small = "saturated fats"
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

        def foodFeatureHealthRisk_two(recipeA, recipeB, nutrients):

            explanation = ""
            small = ""
            great = ""
            risk = ""

            recipeA_name = recipeA["title"]
            recipeB_name = recipeB["title"]

            explanation, small, great = foodFeatures_two(recipeA, recipeB, nutrients)

            if (small != ""):
                risk = random.choice(nutrients[small]["risks"])
                if (small == 'saturatedFat'):
                    small = 'saturated fats'
                explanation += "Intake too much " + small + \
                               " can increase the risk of " + risk + ". "
            if (great != ""):
                risk = random.choice(nutrients[great]["risks"])
                if (great == 'saturatedFat'):
                    great = 'saturated fats'
                explanation += " Intake too much " + great + \
                               " can increase the risk of " + risk + ". "

            if (np.isnan(recipeA['calories']) or np.isnan(recipeB['calories'])):
                explanation += ""
            elif (recipeA["calories"]) > recipeB["calories"]:
                explanation += "Furthermore, " + recipeA_name + " has more calories (" + str(
                    recipeA["calories"]) + " Kcal) than " + recipeB_name + " (" + str(recipeB["calories"]) + " Kcal). "

            elif (recipeB["calories"]) > recipeA["calories"]:
                explanation += "Furthermore, " + recipeB_name + " has more calories (" + str(
                    recipeB["calories"]) + " Kcal) than " + recipeA_name + " (" + str(recipeA["calories"]) + " Kcal). "

            else:
                explanation += "Furthermore, both recipes have got the same amount of calories (" + str(
                    recipeA["calories"]) + " Kcal). "
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

            explanation, small, great = foodFeatures_one(recipe_values, nutrients)

            if (small != ""):
                benefit = random.choice(nutrients[small]["benefits"])
                if (small == "saturatedFat"):
                    small = "saturated fats"
                explanation += " A correct daily intake of " + small + \
                               " can " + benefit + "."
            elif great != "":
                benefit = random.choice(nutrients[great]["benefits"])
                if (great == "saturatedFat"):
                    great = "saturated fats"
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

        def foodFeatureHealthBenefits_two(recipeA, recipeB, nutrients):

            explanation = ""
            small = ""
            great = ""
            risk = ""

            recipeA_name = recipeA["title"]
            recipeB_name = recipeB["title"]

            explanation, small, great = foodFeatures_two(recipeA, recipeB, nutrients)

            if (small != ""):
                benefit = random.choice(nutrients[small]["benefits"])
                if (small == 'saturatedFat'):
                    small = 'saturated fats'
                explanation += "A correct daily intake of " + small + \
                               " can " + benefit + ". "
            if (great != ""):
                benefit = random.choice(nutrients[great]["benefits"])
                if (great == 'saturatedFat'):
                    great = 'saturated fats'
                explanation += "A correct daily intake of " + great + \
                               " can " + benefit + ". "

            if (np.isnan(recipeA['calories']) or np.isnan(recipeB['calories'])):
                explanation += ""
            elif (recipeA["calories"]) > recipeB["calories"]:
                explanation += "Furthermore, " + recipeA_name + " has more calories (" + str(
                    recipeA["calories"]) + " Kcal) than " + recipeB_name + " (" + str(recipeB["calories"]) + " Kcal). "

            elif (recipeB["calories"]) > recipeA["calories"]:
                explanation += "Furthermore, " + recipeB_name + " has more calories (" + str(
                    recipeB["calories"]) + " Kcal) than " + recipeA_name + " (" + str(recipeA["calories"]) + " Kcal). "

            else:
                explanation += "Furthermore, both recipes have got the same amount of calories (" + str(
                    recipeA["calories"]) + " Kcal). "
                explanation += "Reference daily intake of calories is 1900 Kcal."

            return explanation

        """
        The explanation function foodFeatureHealthRisks_one recall the foodFeatures_one
        and returns a string with the risk of the small/great nutrient returned in the
        foodFeatures_one function.
        """

        def userFeatureHealthRisk_one(user, recipe_values, nutrients):

            explanation, small, great = foodFeatures_one(recipe_values, nutrients)

            if (explanation != ""):
                if (user["Mood"] == 'bad' or user["Mood"] == 'neutral' or user["Depressed"] == 'yes' or user[
                    "Stressed"] == 'yes'):
                    listMood = ["sugars", "carbohydrates", "proteins"]
                    if (great in listMood):
                        explanation += "An excess of " + great + " can swing your mood. "

                if (user["BMI"] == "under"):
                    explanation += "It may not be able to help you to gain weight. "
                elif (user["BMI"] == "over"):
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

            if (explanation != ""):
                if (user["Mood"] == 'bad' or user["Mood"] == 'neutral' or user["Depressed"] == 'yes' or user[
                    "Stressed"] == 'yes'):
                    listMood = ["sugars", "carbohydrates", "proteins"]
                    if (greatA in listMood):
                        explanation += "An excess of " + greatA + " can swing your mood. "

                if (user["BMI"] == "under" and greatA != ""):
                    explanation += "It may not be able to help you to gain weight. "
                elif (user["BMI"] == "over" and smallA != ""):
                    explanation += "It may not be able to help you to lose weight. "

                if (np.isnan(recipeA['calories']) or np.isnan(recipeB['calories'])):
                    explanation += ""
                elif (recipeA["calories"]) > recipeB["calories"]:
                    explanation += "Also, " + recipeA_name + " has more calories (" + str(
                        recipeA["calories"]) + " Kcal) than " + recipeB_name + " (" + str(
                        recipeB["calories"]) + " Kcal)."

                elif (recipeB["calories"]) > recipeA["calories"]:
                    explanation += "Also, " + recipeB_name + " has more calories (" + str(
                        recipeB["calories"]) + " Kcal) than " + recipeA_name + " (" + str(
                        recipeA["calories"]) + " Kcal)."

                else:
                    explanation += "Also, both recipes have got the same amount of calories (" + str(
                        recipeA["calories"]) + " Kcal). "
                    explanation += "Reference daily intake of calories is 1900 Kcal."

            return explanation

        """
        The explanation function userFeatureHealthBenefits_one connects the recipe A with the user characteristics
        (BMI, mood, if he or she is depressed/stressed). It returns a string with a benefit related to a nutrient
        that is the output of the foodFeatures_one function.
        """

        def userFeatureHealthBenefits_one(user, recipe_values, nutrients):

            explanation, small, great = foodFeatures_one(recipe_values, nutrients)

            if (user["Mood"] == 'bad' or user["Mood"] == 'neutral' or user["Depressed"] == 'yes' or user[
                "Stressed"] == 'yes'):
                listMood = ["sugars", "carbohydrates", "proteins"]
                if (small in listMood):
                    explanation += "A correct intake of " + small + " can improve your mood. "

            if (user["BMI"] == "under"):
                if (great != ""):
                    explanation += "A correct intake of " + great + " can help you to gain weight. "
                if (small != ""):
                    explanation += "A correct intake of " + small + " can help you to gain weight. "

            elif (user["BMI"] == "over"):
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

            if (explanation != ""):
                if (user["Mood"] == 'bad' or user["Mood"] == 'neutral' or user["Depressed"] == 'yes' or user[
                    "Stressed"] == 'yes'):
                    listMood = ["sugar", "carbohydrates", "proteins"]
                    if (smallA in listMood):
                        explanation += "A correct intake of " + smallA + " can improve your mood. "

                if (user["BMI"] == "under" and greatA != ""):
                    explanation += "A correct intake of " + greatA + " can help you to gain weight. "
                elif (user["BMI"] == "over" and smallA != ""):
                    explanation += "A correct intake of " + smallA + " can help you to lose weight. "

                if (np.isnan(recipeA['calories']) or np.isnan(recipeB['calories'])):
                    explanation += ""

                elif (recipeA["calories"]) > recipeB["calories"]:
                    explanation += "Moreover, " + recipeA_name + " has more calories (" + str(
                        recipeA["calories"]) + " Kcal) than " + recipeB_name + " (" + str(
                        recipeB["calories"]) + " Kcal). "

                elif (recipeB["calories"]) > recipeA["calories"]:
                    explanation += "Moreover, " + recipeB_name + " has more calories (" + str(
                        recipeB["calories"]) + " Kcal) than " + recipeA_name + " (" + str(
                        recipeA["calories"]) + " Kcal). "

                else:
                    explanation += "Moreover, both recipes have got the same amount of calories (" + str(
                        recipeA["calories"]) + " Kcal). "
                    explanation += "Reference daily intake of calories is 1900 Kcal."

            return explanation

        """
        The explanation function userTime_one take as input the user preparation time
        and returns a string saying that the recipe has a certain
        preparation time, and if it is adequate with the specific user preference.
        """

        def userTime_one(user_time, recipe_values):
            explanation = ""
            # time calculation from string ( PM123...4 into the dataset)
            i = len(recipe_values['totalTime']) - 2
            potenzaDieci = 1
            recipe_prepTime = 0
            while i >= 2:
                recipe_prepTime = recipe_prepTime + int(recipe_values['totalTime'][i]) * potenzaDieci
                potenzaDieci = potenzaDieci * 10
                i -= 1

            # value 0 stands for 'no constraints'
            if user_time != 0:
                explanation = recipe_values['title'] + " takes " + str(recipe_prepTime) \
                              + " minutes as preparation time, and you've requested recipes that require at most " \
                              + str(user_time) + " minutes as preparation time. "
            else:
                explanation = recipe_values['title'] + " takes " + str(recipe_prepTime) \
                              + " minutes as preparation time."
            return explanation

        """
        The explanation function userTime_two take as input the user preparation time
        and returns a string which contains the comparison between the preparation time 
        of the two recipes recommended by the recsys
        """

        def userTime_two(user_time, recipeA_values, recipeB_values):
            explanation = ""
            # time calculation from string  for first recipe( PM123...4 into the dataset)
            i = len(recipeA_values['totalTime']) - 2
            potenzaDieci = 1
            recipeA_prepTime = 0
            while i >= 2:
                recipeA_prepTime = recipeA_prepTime + int(recipeA_values['totalTime'][i]) * potenzaDieci
                potenzaDieci = potenzaDieci * 10
                i -= 1

            # time calculation from string  for first recipe( PM123...4 into the dataset)
            i = len(recipeB_values['totalTime']) - 2
            potenzaDieci = 1
            recipeB_prepTime = 0
            while i >= 2:
                recipeB_prepTime = recipeB_prepTime + int(recipeB_values['totalTime'][i]) * potenzaDieci
                potenzaDieci = potenzaDieci * 10
                i -= 1

            if recipeA_prepTime < recipeB_prepTime:
                explanation = recipeA_values['title'] + " can be prepared in less time (" \
                              + str(recipeA_prepTime) + " minutes) than " + recipeB_values['title'] + " (" \
                              + str(recipeB_prepTime)
                if user_time != 0:
                    explanation += " minutes), and you prefer recipes that require a maximum of " \
                                   + str(user_time) + " minutes of preparation time."
                else:
                    explanation += " minutes)."
            elif recipeA_prepTime > recipeB_prepTime:
                explanation = recipeA_values['title'] + " can be prepared in more time (" \
                              + str(recipeA_prepTime) + " minutes) than " + recipeB_values['title'] + " (" \
                              + str(recipeB_prepTime)
                if user_time != 0:
                    explanation += " minutes), and you prefer recipes that require a maximum of " \
                                   + str(user_time) + " minutes of preparation time."
                else:
                    explanation += " minutes)."
            else:  # same preparation time
                explanation = recipeA_values['title'] + " takes the same preparation time (" \
                              + str(recipeA_prepTime) + " minutes) as " \
                              + recipeB_values['title']
                if user_time != 0:
                    explanation += ", and you prefer recipes that require a maximum of " \
                                   + str(user_time) + " minutes of preparation time."
                else:
                    explanation += " ."

            return explanation

        """
        The explanation function userCosts_one take as input the user preference about cost level
        and returns a string saying that the recipe has a certain cost level, and if 
        it is adequate with the specific user preference.
        """

        def userCosts_one(user_cost, recipe_values):
            explanation = ""
            costs = ["very low", "low", "medium", "high"]
            # into the dataset the level is in italian
            costs_translate_stringDict = {"Molto basso": "very low", "Basso": "low",
                                          "Medio": "medium", "Elevato": "high"}

            if costs_translate_stringDict.get(recipe_values['cost']) is None:
                return explanation
            else:
                recipe_cost = costs_translate_stringDict[recipe_values['cost']]

            # if the user cost is 5, it means that for the user the cost is not important, so we show only the cost
            # level of the recommended recipe
            if recipe_values['cost'] != "":
                if user_cost != 5:
                    explanation = recipe_values['title'] + " has a " \
                                  + recipe_cost + " cost level , in line with how much you intend to " \
                                                  "spend (cost level " + costs[user_cost - 1] + ")."
                else:
                    explanation = recipe_values['title'] + " has a " \
                                  + recipe_cost + " cost level."
            return explanation

        """
        The explanation function userCosts_two take as input the user preference about 
        the cost level and returns a string which contains the comparison of the costs of two 
        recipes
        """

        def userCosts_two(user_cost, recipeA_values, recipeB_values):
            explanation = ""
            costs_dict = {1: "very low", 2: "low", 3: "medium", 4: "high"}
            costs_dictRev = {"very low": 1, "low": 2, "medium": 3, "high": 4}
            # into the dataset the level is in italian
            costs_translate_stringDict = {"Molto basso": "very low", "Basso": "low",
                                          "Medio": "medium", "Elevato": "high"}
            if (costs_translate_stringDict.get(recipeA_values['cost']) is None) or (
                    costs_translate_stringDict.get(recipeB_values['cost']) is None):
                return explanation
            else:
                recipeA_cost = costs_translate_stringDict[recipeA_values['cost']]
                recipeB_cost = costs_translate_stringDict[recipeB_values['cost']]
            if user_cost != 5:
                user_cost_str = costs_dict[user_cost]

            if ((recipeA_values["cost"] != "") and (recipeB_values["cost"] != "")):
                # if the user cost is 5, it means that for the user the cost is not important, so we show only the cost
                # level of the recommended recipe
                if recipeA_cost == recipeB_cost:
                    explanation = recipeA_values['title'] + " has the same cost level of " \
                                  + recipeB_values['title']
                    if user_cost != 5:
                        explanation += ", and " + user_cost_str + " is your preference on the level cost."
                    else:
                        explanation += "."
                elif costs_dictRev[recipeA_cost] > costs_dictRev[recipeB_cost]:
                    explanation = recipeA_values['title'] + " has an higher cost level (" + recipeA_cost + ") than " \
                                  + recipeB_values['title'] + " (" + recipeB_cost
                    if user_cost != 5:
                        explanation += "), and " + user_cost_str + " is your preference on the level cost."
                    else:
                        explanation += ")."
                else:
                    explanation = recipeA_values['title'] + " has a lower cost level (" + recipeA_cost + ") than " \
                                  + recipeB_values['title'] + " (" + recipeB_cost
                    if user_cost != 5:
                        explanation += "), and " + user_cost_str + " is your preference on the level cost."
                    else:
                        explanation += ")."
            return explanation

        """
        The function userLifestyle_one connects the user lifestyle to the recipe.
        This function also call rsa_score to estabilish how healthy is a food in according to 
        the FSA guideline 
        """

        def userLifestyle_one(user_health_lifestyle, user_health_condition, recipe_values):
            explanation = ""
            score_level_cmp, score_level_str = getScores(rsa_score(recipe_values))

            if user_health_lifestyle > user_health_condition:
                # user wants to improve the lifestyle
                explanation = "You want to improve your lifestyle, "
                if score_level_cmp > user_health_condition:
                    explanation += recipe_values['title'] + " allows you to have a better diet, because" \
                                   + " it's a " + score_level_str + " recipe (In according to FSA guidelines)."
                elif score_level_cmp == user_health_condition:
                    explanation += recipe_values['title'] + " allows you to maintain your lifestyle, because" \
                                   + " it's a " + score_level_str + " recipe (In according to FSA guidelines). "
                else:
                    explanation += "but " + recipe_values['title'] \
                                   + " doesn't allow to maintain your lifestyle, because" \
                                   + " it's a " + score_level_str + " recipe (In according to FSA guidelines). You " \
                                                                    "probably have a very " \
                                                       "healthy lifestyle and therefore these recipes are slightly " \
                                                       "less healthy than the ones you usually choose."
            elif user_health_lifestyle == user_health_condition:
                # user wants to maintain the lifestyle
                explanation = "You want to maintain your lifestyle, "
                if score_level_cmp > user_health_condition:
                    explanation += recipe_values['title'] + " allows you to have a better diet, because" \
                                   + " it's a " + score_level_str + " recipe (In according to FSA guidelines)."
                elif score_level_cmp == user_health_condition:
                    explanation += recipe_values['title'] + " allows you to maintain your lifestyle, because" \
                                   + " it's a " + score_level_str + " recipe (In according to FSA guidelines)."
                else:
                    explanation += recipe_values['title'] \
                                   + " doesn't allow to maintain your lifestyle, because" \
                                   + " it's a " + score_level_str + " recipe (In according to FSA guidelines). " \
                                                                    "You probably have a very " \
                                                       "healthy lifestyle and therefore these recipes are slightly " \
                                                       "less healthy than the ones you usually choose."
            else:
                # user wants a worst lifestyle. since this can be an error, we don't show this in the string
                if score_level_cmp > user_health_condition:
                    explanation = recipe_values['title'] + " allows you to have a better lifestyle, because" \
                                  + " it's a " + score_level_str + " recipe."
                elif score_level_cmp == user_health_condition:
                    explanation = recipe_values['title'] + " allows you to maintain your lifestyle, because" \
                                  + " it's a " + score_level_str + " recipe."
                else:
                    explanation = recipe_values['title'] + " doesn't allow to maintain your lifestyle, because" \
                                  + " it's a " + score_level_str + " recipe. You probably have a very " \
                                                       "healthy lifestyle and therefore these recipes are slightly " \
                                                       "less healthy than the ones you usually choose."

            return explanation

        """
        The function userLifestyle_two connects the user lifestyle to the recommended recipes.
        This function also call rsa_score to estabilish how healthy is a food in according to the FSA guideline 
        """

        def userLifestyle_two(user_health_lifestyle, user_health_condition, recipeA_values, recipeB_values):
            explanation = ""
            scoreA_level_cmp, scoreA_level_str = getScores(rsa_score(recipeA_values))
            scoreB_level_cmp, scoreB_level_str = getScores(rsa_score(recipeB_values))

            if (scoreA_level_cmp > user_health_condition) or (scoreB_level_cmp > user_health_condition):
                if scoreA_level_cmp > scoreB_level_cmp:
                    # recipeA is better
                    explanation = recipeA_values['title'] + " is healthier than " + recipeB_values['title'] \
                                  + " (in according to FSA guidelines) and can help you to improve your lifestyle."
                elif scoreA_level_cmp < scoreB_level_cmp:
                    # recipeB is better
                    explanation = recipeB_values['title'] + " is healthier than " + recipeA_values['title'] \
                                  + " (in according to FSA guidelines) and can help you to improve your lifestyle."
                else:
                    explanation = "Both recipes allow you to improve your lifestyle, since they are " \
                                  + scoreA_level_str + " (in according to FSA guidelines)."
            elif (scoreA_level_cmp == user_health_condition) or (scoreB_level_cmp == user_health_condition):
                if scoreA_level_cmp > scoreB_level_cmp:
                    # recipeA is better
                    explanation = recipeA_values['title'] + " is healthier than " + recipeB_values['title'] \
                                  + " (in according to FSA guidelines) and can help you to maintain your lifestyle."
                elif scoreA_level_cmp < scoreB_level_cmp:
                    # recipeB is better
                    explanation = recipeB_values['title'] + " is healthier than " + recipeA_values['title'] \
                                  + " (in according to FSA guidelines) and can help you to maintain your lifestyle."
                else:
                    explanation = "Both recipes allow you to maintain your lifestyle, since they are " \
                                  + scoreA_level_str + " (in according to FSA guidelines)."
            else:
                if scoreA_level_cmp > scoreB_level_cmp:
                    # recipeA is better
                    explanation = "Both recipes make your lifestyle worse, but " + \
                                  recipeA_values['title'] + " is quite healthier than " + recipeB_values['title'] \
                                  + " (in according to FSA guidelines). You probably have a very " \
                                                       "healthy lifestyle and therefore these recipes are slightly " \
                                                       "less healthy than the ones you usually choose."
                elif scoreA_level_cmp < scoreB_level_cmp:
                    # recipeB is better
                    explanation = "Both recipes make your lifestyle worse, but " + \
                                  recipeB_values['title'] + " is quite healthier than " + recipeA_values['title'] \
                                  + " (in according to FSA guidelines). You probably have a very " \
                                                       "healthy lifestyle and therefore these recipes are slightly " \
                                                       "less healthy than the ones you usually choose."
                else:
                    explanation = "Both recipes make your lifestyle worse, since they are " \
                                  + scoreA_level_str + " (in according to FSA guidelines). You probably have a very " \
                                                       "healthy lifestyle and therefore these recipes are slightly " \
                                                       "less healthy than the ones you usually choose."
            return explanation

        """
        This function calculates the score that estabilish how healthy is a recipe in according to the FSA guide lines
        """

        def rsa_score(recipe_values):
            # have to divide each value by 1.2 because in the dataset we have
            # the values per portion but the score is calculated per 100g
            score = 0.0
            # get all the recipe's nutrients
            fat = float(recipe_values['fat']) / 1.2
            saturated_fat = float(recipe_values['saturatedFat']) / 1.2
            sugar = float(recipe_values['sugars']) / 1.2
            # http://www.istitutodanone.it/novita-etichetta/sale-sodio-limportante-conoscere-differenza/ si moltiplica per 2.5 il sodio
            sodium = float(recipe_values['sodium']) / 1000
            sodium = sodium / 1.2
            salt = sodium * 2.5
            # FAT SCORE
            if fat <= 3.0:
                score += 1
            elif (fat > 3.0) and (fat <= 17.5):
                score += 2
            else:
                score += 3
            # SATURATED FAT SCORE
            if saturated_fat <= 1.5:
                score += 1
            elif (saturated_fat > 1.5) and (saturated_fat <= 5.0):
                score += 2
            else:
                score += 3
            # SUGAR SCORE
            if sugar <= 5.0:
                score += 1
            elif (sugar > 5.0) and (sugar <= 22.5):
                score += 2
            else:
                score += 3
            # SALT SCORE
            if salt <= 0.3:
                score += 1
            elif (salt > 0.3) and (salt <= 1.5):
                score += 2
            else:
                score += 3
            # TOTAL SCORE is a number between 4 (very healthy) to 12 (very unhealthy)
            return score

        """
        This function converts the FSA score int string and in a  comparable number for the user lifestyle
        """

        def getScores(score):
            if score <= 5.6:
                score_level_str = "very healthy"
                score_level_cmp = 5
            elif (score > 5.6) and (score <= 7.2):
                score_level_str = "healthy"
                score_level_cmp = 4
            elif (score > 7.2) and (score <= 8.6):
                score_level_str = "average healthy"
                score_level_cmp = 3
            elif (score > 8.6) and (score <= 10.2):
                score_level_str = "unhealthy"
                score_level_cmp = 2
            else:
                score_level_str = "very unhealthy"
                score_level_cmp = 1
            return score_level_cmp, score_level_str

        """
        The function userIngredients_one verifies if the recommended recipe contains the user's favourite 
        ingredients, if any of these are present it provides an explanation in which it lists which of these are present
        in the recipe
        """

        def userIngredients_one(user_ingredients, recipe_values):
            explanation = ""
            recipe_ingredients_str = recipe_values['ingredients']
            # clean string
            recipe_ingredients_str.translate({ord('['): None})
            recipe_ingredients_str.translate({ord(']'): None})
            recipe_ingredients_str.translate({ord('"'): None})
            recipe_ingredients = recipe_ingredients_str.split(',')
            favIngredientsInRecipe = []
            for ingredient in user_ingredients:
                for recipeIngredient in recipe_ingredients:
                    if recipeIngredient.casefold().find(ingredient.casefold()) != -1:
                        favIngredientsInRecipe.append(ingredient.casefold())

            # remove duplicates
            favIngredientsInRecipe = list(dict.fromkeys(favIngredientsInRecipe))
            # remove empty strings
            if "" in favIngredientsInRecipe:
                favIngredientsInRecipe.remove("");
            if " " in favIngredientsInRecipe:
                favIngredientsInRecipe.remove(" ");

            if len(favIngredientsInRecipe) > 0:
                if len(favIngredientsInRecipe) == 1:
                    explanation = recipe_values['title'] + " is prepared with " + favIngredientsInRecipe[0] \
                                  + ", which is one of your favourite ingredients."
                else:
                    explanation = recipe_values['title'] + " is prepared with "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, favIngredientsInRecipe))
                    explanation += " which are some of your favourite ingredients."

            return explanation

        """
        The function userIngredients_two  verifies that the recommended recipes contain the user's favourite 
        ingredients, if any of these are present it provides an explanation in which it lists which of these are present
        in the recipes and compare them
        """

        def userIngredients_two(user_ingredients, recipeA_values, recipeB_values):
            explanation = ""
            recipeA_ingredients_str = recipeA_values['ingredients']
            # clean string
            recipeA_ingredients_str.translate({ord('['): None})
            recipeA_ingredients_str.translate({ord(']'): None})
            recipeA_ingredients_str.translate({ord('"'): None})
            recipeA_ingredients = recipeA_ingredients_str.split(',')
            # create list of fav ingredients in recipe A
            favIngredientsInRecipeA = []
            for ingredient in user_ingredients:
                for recipeIngredient in recipeA_ingredients:
                    if recipeIngredient.casefold().find(ingredient.casefold()) != -1:
                        favIngredientsInRecipeA.append(ingredient.casefold())

            # remove duplicates
            favIngredientsInRecipeA = list(dict.fromkeys(favIngredientsInRecipeA))
            # remove empty strings
            if "" in favIngredientsInRecipeA:
                favIngredientsInRecipeA.remove("");
            if " " in favIngredientsInRecipeA:
                favIngredientsInRecipeA.remove(" ");

            recipeB_ingredients_str = recipeB_values['ingredients']
            # clean string
            recipeB_ingredients_str.translate({ord('['): None})
            recipeB_ingredients_str.translate({ord(']'): None})
            recipeB_ingredients_str.translate({ord('"'): None})
            recipeB_ingredients = recipeB_ingredients_str.split(',')
            # create list of fav ingredients in recipe B
            favIngredientsInRecipeB = []
            for ingredient in user_ingredients:
                for recipeIngredient in recipeB_ingredients:
                    if recipeIngredient.casefold().find(ingredient.casefold()) != -1:
                        favIngredientsInRecipeB.append(ingredient.casefold())

            # remove duplicates
            favIngredientsInRecipeB = list(dict.fromkeys(favIngredientsInRecipeB))
            # remove empty strings
            if "" in favIngredientsInRecipeB:
                favIngredientsInRecipeB.remove("");
            if " " in favIngredientsInRecipeA:
                favIngredientsInRecipeB.remove(" ");

            if (len(favIngredientsInRecipeA) > 0) or (len(favIngredientsInRecipeB) > 0):

                if len(favIngredientsInRecipeB) == 0:
                    # recipe B doesn't "contain" any fav ingredient
                    explanation = recipeA_values['title'] + " contains "
                    if len(favIngredientsInRecipeA) == 1:
                        # recipe A contains just 1 of fav ingredients
                        explanation += favIngredientsInRecipeA[0] + ", one of your favourite ingredients, compared to " \
                                       + recipeB_values['title'] + " which doesn't contain any favourite ingredients."
                    elif len(favIngredientsInRecipeA) > 1:
                        # recipe A contains more then 1 of fav ingredients
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, favIngredientsInRecipeA))
                        explanation += " which are some of your favourite ingredients, compared to " \
                                       + recipeB_values['title'] + "which doesn't contain any favourite ingredients."

                elif (len(favIngredientsInRecipeA) == 0):
                    # recipe A doesn't "contain" any fav ingredient
                    explanation = recipeB_values['title'] + " contains "
                    if len(favIngredientsInRecipeB) == 1:
                        # recipe B contains just 1 of fav ingredients
                        explanation += favIngredientsInRecipeB[0] + ", one of your favourite ingredients, compared to " \
                                       + recipeA_values['title'] + " which doesn't contain any favourite ingredients."
                    elif len(favIngredientsInRecipeB) > 1:
                        # recipe B contains more then 1 of fav ingredients
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, favIngredientsInRecipeB))
                        explanation += " which are some of your favourite ingredients, compared to " \
                                       + recipeA_values['title'] + " which doesn't contain any favourite ingredients."

                else:
                    # both recipes contain some fav ingredients
                    explanation = recipeA_values['title'] + " contains "
                    if len(favIngredientsInRecipeA) == 1:
                        # recipe A contains just 1 of fav ingredients
                        explanation += favIngredientsInRecipeA[0] + ", one of your favourite ingredients, compared to "
                    elif len(favIngredientsInRecipeA) > 1:
                        # recipe A contains more then 1 of fav ingredients
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, favIngredientsInRecipeA))
                        explanation += " which are some of your favourite ingredients, compared to "

                    explanation += recipeB_values['title'] + " which contains "
                    if len(favIngredientsInRecipeB) == 1:
                        # recipe B contains just 1 of fav ingredients
                        explanation += favIngredientsInRecipeB[0]
                        explanation += "."
                    elif len(favIngredientsInRecipeB) > 1:
                        # recipe B contains more then 1 of fav ingredients
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, favIngredientsInRecipeB))
                        explanation += "."

            return explanation

        """
        The function userAge_one evaluate if certain ingredients are present in the recommended recipe to evaluate 
        if they are rich in the recommended nutrient for a certain age group
        """

        def userAge_one(user_age, recipe_values):
            explanation = ""
            # we build sets of ingredients with certain characteristics (for example rich in calcium) to evaluate
            # if the recipes contain them
            # from https://www.myfooddata.com/articles/foods-high-in-calcium.php
            richCalciumList = ["tofu", "milk", "yogurt", "parmesan", "spinach",
                               "black-eyed peas", "okra", "trout", "squash", "clams"]
            # from https://www.myfooddata.com/articles/food-sources-of-iron.php
            richIronList = ["cereals", "beef", "shellfish", "apricots", "white beans",
                            "spinach", "dark chocolate", "quinoa", "mushrooms", "pumpkin seeds"]
            # from https://www.myfooddata.com/articles/foods-high-in-magnesium.php#magnesium-rich-foods-list
            richMagnesiumList = ["spinach", "pumpkin seeds", "beans", "tuna", "brown rice",
                                 "almonds", "dark chocolate", "avocado", "yogurt", "banana"]
            # to evaluate whether an ingredient is antioxidant, it is necessary to evaluate whether it contains
            # elements that are. The main antioxidants in foods are lycopene and beta carotene.
            # from https://www.myfooddata.com/articles/high-lycopene-foods.php
            richLycopeneList = ["guavas", "tomato", "watermelon", "grapefruit", "papaya",
                                "red peppers", "persimmon", "asparagus", "red cabbage", "mangos"]
            # from https://www.myfooddata.com/articles/natural-food-sources-of-beta-carotene.php
            richBetaCaroteneList = ["sweet potato", "carrots", "spinach", "butternut squash", "cantaloupe",
                                    "romaine lettuce", "red peppers", "apricots", "broccoli", "peas"]
            richAntioxidantList = richLycopeneList + richBetaCaroteneList
            # from https://www.myfooddata.com/articles/vitamin-c-foods.php
            richVitaminCList = ["guavas", "kiwi", "red peppers", "strawberries", "oranges",
                                "papaya", "broccoli", "tomato", "peas", "kale"]
            # from https://www.myfooddata.com/articles/vitamin-e-foods.php
            richVitaminEList = ["sunflower seeds", "almonds", "avocado", "spinach", "butternut squash",
                                "kiwi", "broccoli", "trout", "olive oil", "shrimp"]
            # from https://www.myfooddata.com/articles/high-vitamin-D-foods.php
            richVitaminDList = ["salmon", "chestnut", "milk", "soy milk", "tofu",
                                "yogurt", "breakfast cereal", "orange juice", "pork chops", "eggs"]
            under_30_motivation = " In your age group, calcium intake is important to help the bones reach their " \
                                  "maximum development. In addition, it is important to take iron to support " \
                                  "metabolism, improve concentration, improve oxygen transfer to the muscles " \
                                  "and produce hormones."
            under_40_motivation = " In your age group, the intake of magnesium is important, a mineral that helps " \
                                  "generate energy for the body, regulate blood pressure and blood sugar, and keep " \
                                  "bones strong."
            under_50_motivation = " In your age group, taking antioxidants, vitamin C and E is important to fend " \
                                  "off harmful free radicals. Harmful free radical damage contributes to aging and " \
                                  "many chronic diseases."
            over_50_motivation = " In your age group, calcium intake is important to counteract bone loss. It is " \
                                 "also important to take vitamin D."

            if user_age == "U30":
                # in this age group we want recipes that contain ingredients rich in calcium and iron
                calciumIngredientsInRecipe = isRichIn(richCalciumList, recipe_values)
                ironIngredientsInRecipe = isRichIn(richIronList, recipe_values)
                # define explanation
                if (len(calciumIngredientsInRecipe) > 0) and (len(ironIngredientsInRecipe) > 0):
                    explanation = recipe_values['title'] + " contains "
                    if len(calciumIngredientsInRecipe) == 1:
                        explanation += calciumIngredientsInRecipe[0] + " which is an ingredient rich in calcium, "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, calciumIngredientsInRecipe))
                        explanation += " which are ingredients rich in calcium, "
                    explanation = " and "
                    if len(ironIngredientsInRecipe) == 1:
                        explanation += ironIngredientsInRecipe[0] + " which is an ingredient rich in iron. "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, ironIngredientsInRecipe))
                        explanation += " which are ingredients rich in iron. "
                    explanation += under_30_motivation
                elif len(calciumIngredientsInRecipe) > 0:
                    explanation = recipe_values['title'] + " contains "
                    if len(calciumIngredientsInRecipe) == 1:
                        explanation += calciumIngredientsInRecipe[0] + " which is an ingredient rich in calcium. "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, calciumIngredientsInRecipe))
                        explanation += " which are ingredients rich in calcium. "
                    explanation += under_30_motivation
                elif len(ironIngredientsInRecipe) > 0:
                    explanation = recipe_values['title'] + " contains "
                    if len(ironIngredientsInRecipe) == 1:
                        explanation += ironIngredientsInRecipe[0] + " which is an ingredient rich in iron. "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, ironIngredientsInRecipe))
                        explanation += "which are ingredients rich in iron. "
                    explanation += under_30_motivation

            if user_age == "U40":
                # in this age group we want recipes that contain ingredients rich in magnesium
                magnesiumIngredientsInRecipe = isRichIn(richMagnesiumList, recipe_values)
                if len(magnesiumIngredientsInRecipe) > 0:
                    explanation = recipe_values['title'] + " contains "
                    if len(magnesiumIngredientsInRecipe) == 1:
                        explanation += magnesiumIngredientsInRecipe[0] + " which is an ingredient rich in magnesium. "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, magnesiumIngredientsInRecipe))
                        explanation += "which are ingredients rich in magnesium. "
                    explanation += under_40_motivation

            if user_age == "U50":
                # in this age group we want recipes that contain ingredients rich in vitamin C and E, and antioxidants
                antioxidantIngredientsInRecipe = isRichIn(richAntioxidantList, recipe_values)
                vitaminCIngredientsInRecipe = isRichIn(richVitaminCList, recipe_values)
                vitaminEIngredientsInRecipe = isRichIn(richVitaminEList, recipe_values)
                # u50 explanation
                if (len(antioxidantIngredientsInRecipe) > 0) or (len(vitaminCIngredientsInRecipe) > 0) or (
                        len(vitaminEIngredientsInRecipe) > 0):
                    explanation = recipe_values['title'] + " contains "
                    if len(antioxidantIngredientsInRecipe) > 0:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, antioxidantIngredientsInRecipe))
                        explanation += "(antioxidant) "
                    if len(vitaminCIngredientsInRecipe) > 0:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, vitaminCIngredientsInRecipe))
                        explanation += "(rich in vitamin C) "
                    if len(vitaminEIngredientsInRecipe) > 0:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, vitaminEIngredientsInRecipe))
                        explanation += "(rich in vitamin E). "
                    explanation += under_50_motivation

            if (user_age == "U60") or (user_age == "060"):
                # in this age group we want recipes that contain ingredients rich in calcium and vitamin D
                vitaminDIngredientsInRecipe = isRichIn(richVitaminDList, recipe_values)
                calciumIngredientsInRecipe = isRichIn(richCalciumList, recipe_values)

                # define explanation
                if (len(calciumIngredientsInRecipe) > 0) and (len(vitaminDIngredientsInRecipe) > 0):
                    explanation = recipe_values['title'] + " contains "
                    if len(calciumIngredientsInRecipe) == 1:
                        explanation += calciumIngredientsInRecipe[0] + " which is an ingredient rich in calcium, "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, calciumIngredientsInRecipe))
                        explanation += " which are ingredients rich in calcium, "
                    explanation = " and "
                    if len(vitaminDIngredientsInRecipe) == 1:
                        explanation += vitaminDIngredientsInRecipe[0] + " which is an ingredient rich in vitamin D. "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, vitaminDIngredientsInRecipe))
                        explanation += " which are ingredients rich in vitamin D. "
                    explanation += over_50_motivation
                elif len(calciumIngredientsInRecipe) > 0:
                    explanation = recipe_values['title'] + " contains "
                    if len(calciumIngredientsInRecipe) == 1:
                        explanation += calciumIngredientsInRecipe[0] + " which is an ingredient rich in calcium, "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, calciumIngredientsInRecipe))
                        explanation += " which are ingredients rich in calcium. "
                    explanation += over_50_motivation
                elif len(vitaminDIngredientsInRecipe) > 0:
                    explanation = recipe_values['title'] + " contains "
                    if len(vitaminDIngredientsInRecipe) == 1:
                        explanation += vitaminDIngredientsInRecipe[0] + " which is an ingredient rich in vitamin D, "
                    else:
                        # concatenate list of ingredients separated by ',' to the explanation
                        explanation += str(reduce(lambda x, y: x + "," + y, vitaminDIngredientsInRecipe))
                        explanation += " which are ingredients rich in vitamin D. "
                    explanation += over_50_motivation

            explanation = explanation.replace('[', "")
            explanation = explanation.replace(']', "")
            return explanation

        """
        The function userAge_two evaluate if certain ingredients are present in the recommended recipes to evaluate 
        if they are rich in the recommended nutrient for a certain age group, and compare the recipes
        """

        def userAge_two(user_age, recipeA_values, recipeB_values):
            explanation = ""
            # from https://www.myfooddata.com/articles/foods-high-in-calcium.php
            richCalciumList = ["tofu", "milk", "yogurt", "parmesan", "spinach",
                               "black-eyed peas", "okra", "trout", "squash", "clams"]
            # from https://www.myfooddata.com/articles/food-sources-of-iron.php
            richIronList = ["cereals", "beef", "shellfish", "apricots", "white beans",
                            "spinach", "dark chocolate", "quinoa", "mushrooms", "pumpkin seeds"]
            # from https://www.myfooddata.com/articles/foods-high-in-magnesium.php#magnesium-rich-foods-list
            richMagnesiumList = ["spinach", "pumpkin seeds", "beans", "tuna", "brown rice",
                                 "almonds", "dark chocolate", "avocado", "yogurt", "banana"]
            # to evaluate whether an ingredient is antioxidant, it is necessary to evaluate whether it contains
            # elements that are. The main antioxidants in foods are lycopene and beta carotene.
            # from https://www.myfooddata.com/articles/high-lycopene-foods.php
            richLycopeneList = ["guavas", "tomato", "watermelon", "grapefruit", "papaya",
                                "red peppers", "persimmon", "asparagus", "red cabbage", "mangos"]
            # from https://www.myfooddata.com/articles/natural-food-sources-of-beta-carotene.php
            richBetaCaroteneList = ["sweet potato", "carrots", "spinach", "butternut squash", "cantaloupe",
                                    "romaine lettuce", "red peppers", "apricots", "broccoli", "peas"]
            richAntioxidantList = richLycopeneList + richBetaCaroteneList
            # from https://www.myfooddata.com/articles/vitamin-c-foods.php
            richVitaminCList = ["guavas", "kiwi", "red peppers", "strawberries", "oranges",
                                "papaya", "broccoli", "tomato", "peas", "kale"]
            # from https://www.myfooddata.com/articles/vitamin-e-foods.php
            richVitaminEList = ["sunflower seeds", "almonds", "avocado", "spinach", "butternut squash",
                                "kiwi", "broccoli", "trout", "olive oil", "shrimp"]
            # from https://www.myfooddata.com/articles/high-vitamin-D-foods.php
            richVitaminDList = ["salmon", "chestnut", "milk", "soy milk", "tofu",
                                "yogurt", "breakfast cereal", "orange juice", "pork chops", "eggs"]
            # Motivations for every age group
            under_30_motivation = " In your age group, calcium intake is important to help the bones reach their " \
                                  "maximum development. In addition, it is important to take iron to support " \
                                  "metabolism, improve concentration, improve oxygen transfer to the muscles " \
                                  "and produce hormones."
            under_40_motivation = " In your age group, the intake of magnesium is important, a mineral that helps " \
                                  "generate energy for the body, regulate blood pressure and blood sugar, and keep " \
                                  "bones strong."
            under_50_motivation = " In your age group, taking antioxidants, vitamin C and E is important to fend " \
                                  "off harmful free radicals. Harmful free radical damage contributes to aging and " \
                                  "many chronic diseases."
            over_50_motivation = " In your age group, calcium intake is important to counteract bone loss. It is " \
                                 "also important to take vitamin D."

            if user_age == "U30":
                # int this age we want food that contain calcium and iron
                u30IngredientsFeatureList = richCalciumList + richIronList
                u30IngredientsFeatureList = list(dict.fromkeys(u30IngredientsFeatureList))
                # ingredients in recipe A that are rich in calcium or iron
                goodIngredientsInRecipeA = isRichIn(u30IngredientsFeatureList, recipeA_values)

                # ingredients in recipe B that are rich in calcium or iron
                goodIngredientsInRecipeB = isRichIn(u30IngredientsFeatureList, recipeB_values)

                # define explanation
                if (len(goodIngredientsInRecipeA) > 0) and (len(goodIngredientsInRecipeB) > 0):
                    # both recipes contain good ingredients for the user age
                    explanation = recipeA_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeA))
                    explanation += " and " + recipeB_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeB)) + ". "
                    explanation += under_30_motivation
                elif len(goodIngredientsInRecipeA) > 0:
                    explanation = recipeA_values['title'] + " compared to " + recipeB_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeA)) + ". "
                    explanation += under_30_motivation
                elif len(goodIngredientsInRecipeB) > 0:
                    explanation = recipeB_values['title'] + " compared to " + recipeA_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeB)) + ". "
                    explanation += under_30_motivation
            if user_age == "U40":
                # in this age we want ingredients wich are rich in magnesium
                u40IngredientsFeatureList = richMagnesiumList
                u40IngredientsFeatureList = list(dict.fromkeys(u40IngredientsFeatureList))
                goodIngredientsInRecipeA = isRichIn(u40IngredientsFeatureList, recipeA_values)

                goodIngredientsInRecipeB = isRichIn(u40IngredientsFeatureList, recipeB_values)
                # define explanation
                # define explanation
                if (len(goodIngredientsInRecipeA) > 0) and (len(goodIngredientsInRecipeB) > 0):
                    # both recipes contain good ingredients for the user age
                    explanation = recipeA_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeA))
                    explanation += " and " + recipeB_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeB)) + ". "
                    explanation += under_40_motivation
                elif len(goodIngredientsInRecipeA) > 0:
                    explanation = recipeA_values['title'] + " versus " + recipeB_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeA)) + ". "
                    explanation += under_40_motivation
                elif len(goodIngredientsInRecipeB) > 0:
                    explanation = recipeB_values['title'] + " versus " + recipeA_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeB)) + ". "
                    explanation += under_40_motivation
            if user_age == "U50":
                # we want ingredients rich in vitamin c and e and antioxidants
                u50IngredientsFeatureList = richAntioxidantList + richVitaminCList + richVitaminEList
                u50IngredientsFeatureList = list(dict.fromkeys(u50IngredientsFeatureList))
                # ingredients in recipe A that are good
                goodIngredientsInRecipeA = isRichIn(u50IngredientsFeatureList, recipeA_values)

                # ingredients in recipe B that are good
                goodIngredientsInRecipeB = isRichIn(u50IngredientsFeatureList, recipeB_values)

                # define explanation
                if (len(goodIngredientsInRecipeA) > 0) and (len(goodIngredientsInRecipeB) > 0):
                    # both recipes contain good ingredients for the user age
                    explanation = recipeA_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeA))
                    explanation += " and " + recipeB_values + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeB)) + ". "
                    explanation += under_50_motivation
                elif len(goodIngredientsInRecipeA) > 0:
                    explanation = recipeA_values['title'] + " compared to " + recipeB_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeA)) + ". "
                    explanation += under_50_motivation
                elif len(goodIngredientsInRecipeB) > 0:
                    explanation = recipeB_values['title'] + " compared to " + recipeA_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeB)) + ". "
                    explanation += under_50_motivation

            if (user_age == "U60") or (user_age == "060"):
                # in this age group we want ingredients that are rich in calcium and vitamin d
                o60IngredientsFeatureList = richCalciumList + richVitaminDList
                o60IngredientsFeatureList = list(dict.fromkeys(o60IngredientsFeatureList))
                # ingredients in recipe A that are good
                goodIngredientsInRecipeA = isRichIn(o60IngredientsFeatureList, recipeA_values)

                # ingredients in recipe B that are good
                goodIngredientsInRecipeB = isRichIn(o60IngredientsFeatureList, recipeB_values)

                # define explanation
                if (len(goodIngredientsInRecipeA) > 0) and (len(goodIngredientsInRecipeB) > 0):
                    # both recipes contain good ingredients for the user age
                    explanation = recipeA_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeA))
                    explanation += " and " + recipeB_values + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeB)) + ". "
                    explanation += over_50_motivation
                elif len(goodIngredientsInRecipeA) > 0:
                    explanation = recipeA_values['title'] + " compared to " + recipeB_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeA)) + ". "
                    explanation += over_50_motivation
                elif len(goodIngredientsInRecipeB) > 0:
                    explanation = recipeB_values['title'] + " compared to " + recipeA_values['title'] + " contains "
                    # concatenate list of ingredients separated by ',' to the explanation
                    explanation += str(reduce(lambda x, y: x + "," + y, goodIngredientsInRecipeB)) + ". "
                    explanation += over_50_motivation

            explanation = explanation.replace('[', "")
            explanation = explanation.replace(']', "")
            return explanation

        def isRichIn(ingredientsListRichsIn, recipe_values):
            richInRecipe = []
            recipe_ingredients_str = recipe_values['ingredients']
            # clean string
            recipe_ingredients_str.translate({ord('['): None})
            recipe_ingredients_str.translate({ord(']'): None})
            recipe_ingredients_str.translate({ord('"'): None})
            recipe_ingredients = recipe_ingredients_str.split(',')  # array of ingredients
            for richInIngredient in ingredientsListRichsIn:
                for ingredient in recipe_ingredients:
                    if ingredient.casefold().find(richInIngredient) != -1:
                        richInRecipe.append(ingredient)
            # remove duplicates
            richInRecipe = list(dict.fromkeys(richInRecipe))
            return richInRecipe

        # -----
        # Function get_string_exp returns the explanation of a specific type
        # (popularity, food features, user features, ecc...)
        # ---
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
                if (userRestrictions is None):
                    expl = ""
                else:
                    flag = 0
                    random.shuffle(listRestrictions)
                    i = 0
                    # encoded(vegetarian,lactosefree,glutenfree,lownichel,light)
                    while (flag == 0 and i < len(listRestrictions)):
                        if (listRestrictions[i] in userRestrictions):
                            restriction = listRestrictions[i]
                            description = restrictions["one"][restriction]
                            if (listRestrictions[i] == "lactosefree"):
                                restriction = "lactose-free"
                            if (listRestrictions[i] == "glutenfree"):
                                restriction = "gluten-free"
                            if (listRestrictions[i] == "lownichel"):
                                restriction = "low-nichel"
                            flag = 1

                        i += 1

                    expl = foodPreferences_one(restriction, description, recipeName)
            elif type_explanation == 'foodFeatures_one':
                expl, _, _ = foodFeatures_one(recipe_values,
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
            # new expls
            elif type_explanation == 'userTime_one':
                user_time = int(user['User_time'])
                expl = userTime_one(user_time, recipe_values)
            elif type_explanation == 'userCosts_one':
                user_costs = int(user['User_cost'])
                if (recipe_values['cost'] == ""):
                    expl = ""
                else:
                    expl = userCosts_one(user_costs, recipe_values)
            elif type_explanation == 'userLifestyle_one':
                user_health_lifestyle = int(user['Health_style'])
                user_health_condition = int(user['Health_condition'])
                expl = userLifestyle_one(user_health_lifestyle, user_health_condition, recipe_values)
            elif type_explanation == 'userIngredients_one':
                user_ingredients = user['User_ingredients'].split("-")
                if user_ingredients is None:
                    expl = ""
                else:
                    expl = userIngredients_one(user_ingredients, recipe_values)
            elif type_explanation == 'userAge_one':
                user_age = user['Age']
                expl = userAge_one(user_age, recipe_values)
            elif type_explanation == 'description':
                if recipe_values['description'] != "":
                    expl = recipe_values['description']
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
                if (userRestrictions is None):
                    expl = ""
                else:
                    flag = 0
                    random.shuffle(listRestrictions)
                    i = 0

                    while (flag == 0 and i < len(listRestrictions)):
                        if (listRestrictions[i] in userRestrictions):
                            restriction = listRestrictions[i]
                            description = restrictions["two"][restriction]
                            if (listRestrictions[i] == "lactosefree"):
                                restriction = "lactose-free"
                            if (listRestrictions[i] == "glutenfree"):
                                restriction = "gluten-free"
                            if (listRestrictions[i] == "lownichel"):
                                restriction = "low-nichel"
                            flag = 1

                        i += 1

                    expl = foodPreferences_two(restriction, description)

            elif type_explanation == 'foodFeatures_two':
                expl, _, _ = foodFeatures_two(recipeA_values,
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
                expl = foodFeatureHealthRisk_two(recipeA_values, recipeB_values, nutrients)
            elif type_explanation == 'foodFeatureHealthBenefits_two':
                expl = foodFeatureHealthBenefits_two(recipeA_values, recipeB_values, nutrients)
            elif type_explanation == 'userFeatureHealthRisk_two':
                expl = userFeatureHealthRisk_two(user, recipeA_values, recipeB_values, nutrients)
            elif type_explanation == 'userFeatureHealthBenefits_two':
                expl = userFeatureHealthBenefits_two(user, recipeA_values, recipeB_values, nutrients)

            # new expls
            elif type_explanation == 'userTime_two':
                user_time = int(user['User_time'])
                expl = userTime_two(user_time, recipeA_values, recipeB_values)

            elif type_explanation == 'userCosts_two':
                user_costs = int(user['User_cost'])
                if (recipeA_values['cost'] == "") and (recipeB_values['cost'] == ""):
                    expl = ""
                else:
                    expl = userCosts_two(user_costs, recipeA_values, recipeB_values)

            elif type_explanation == 'userLifestyle_two':
                user_health_lifestyle = int(user['Health_style'])
                user_health_condition = int(user['Health_condition'])
                expl = userLifestyle_two(user_health_lifestyle, user_health_condition, recipeA_values, recipeB_values)
            elif type_explanation == 'userIngredients_two':
                user_ingredients = user['User_ingredients'].split("-")
                if user_ingredients is None:
                    expl = ""
                else:
                    expl = userIngredients_two(user_ingredients, recipeA_values, recipeB_values)
            elif type_explanation == 'userAge_two':
                user_age = user['Age']
                expl = userAge_two(user_age, recipeA_values, recipeB_values)
            elif type_explanation == 'descriptions':
                if (recipeA_values['description'] != "") and (recipeB_values['description'] != ""):
                    expl = recipeA_values['description'] + recipeB_values['description']
            return expl

        # ---

        nutrientsPath = 'Nutrient.json'
        restrictionsPath = 'Restrictions.json'

        recipeA_url = request.args.get('imgurl1')
        recipeB_url = request.args.get('imgurl2')
        url_dataset_en = 'dataset_en.csv'

        # df = pd.read_csv(url_dataset_en)

        # read file
        with open(nutrientsPath, 'r') as myfile:
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
            if (row["imageURL"] == recipeA_url):
                recipeA_values = row
            if (row["imageURL"] == recipeB_url):
                recipeB_values = row

        recipeA_values["sodium"] = recipeA_values["sodium"] / 1000
        recipeB_values["sodium"] = recipeB_values["sodium"] / 1000

        recipeA_values["cholesterol"] = recipeA_values["cholesterol"] / 1000
        recipeB_values["cholesterol"] = recipeB_values["cholesterol"] / 1000

        user = {
            'Age': request.args.get('user_age'),  # U20/U30/U40/U50/U60/060
            'Mood': request.args.get('mood'),  # bad/good/neutral
            'Stressed': request.args.get('stress'),  # yes/no
            'Depressed': request.args.get('depression'),  # yes/no
            'BMI': request.args.get('bmi'),  # over/under/normal
            'Health_style': request.args.get('health_style'),  # 1/2/3/4/5
            'Health_condition': request.args.get('health_condition'),  # 1/2/3/4/5
            'Activity': request.args.get('activity'),  # low/high/normal
            'Sleep': request.args.get('sleep'),  # low/good
            'Cooking_exp': request.args.get('difficulty'),  # 1/2/3/4/5
            'User_time': request.args.get('user_time'),  # time for prep in mins [10,200]; 0 stans for "no constraints"
            'User_cost': request.args.get('user_cost'),  # 1/2/3/4 5= not important
            'Goal': request.args.get('goal'),  # lose/gain/no
            'User_restriction': request.args.get('restr'),
            # encoded(vegetarian,lactosefree,glutenfree,lownichel,light)
            'User_ingredients': request.args.get('user_ingredients')
        }

        two_recipes = [
            "popularity_two",
            "foodGoals_two",
            "foodPreferences_two",  # user restrictions
            "foodFeatures_two",
            "userSkills_two",
            "foodFeatureHealthRisk_two",
            "foodFeatureHealthBenefits_two",
            "userFeatureHealthRisk_two",
            "userFeatureHealthBenefits_two",
            # new explanations
            "userTime_two",
            "userCosts_two",
            "userLifestyle_two",
            "userIngredients_two",
            "userAge_two",
            "descriptions"
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
            "userFeatureHealthBenefits_one",
            # new explanations
            "userTime_one",
            "userCosts_one",
            "userLifestyle_one",
            "userIngredients_one",
            "userAge_one",
            "description"
        ]


        # exps for the configuration
        two_recipes_experiment = [
            "popularity_two",
            "foodGoals_two",
            "foodPreferences_two",
            "foodFeatures_two",
            "userSkills_two",
            "foodFeatureHealthRisk_two",
            "foodFeatureHealthBenefits_two",
            "userFeatureHealthRisk_two",
            "userFeatureHealthBenefits_two",
            "userTime_two",
            "userCosts_two",
            "userLifestyle_two",
            "userIngredients_two",
            "userAge_two",
            "descriptions"
        ]
        one_recipe_experiment = [
            "popularity_one",
            "foodGoals_one",
            "foodPreferences_one",
            "foodFeatures_one",
            "userSkills_one",
            "foodFeatureHealthRisk_one",
            "foodFeatureHealthBenefits_one",
            "userFeatureHealthRisk_one",
            "userFeatureHealthBenefits_one",
            "userTime_one",
            "userCosts_one",
            "userLifestyle_one",
            "userIngredients_one",
            "userAge_one",
            "description"
        ]

        # web app request a specific type of explanation for every recipe(use if u want that same type of exp is shown)
        # type_explanation_requested = int(request.args.get('type'))
        explanations = {}

        expl = ""
        for type_exp in one_recipe_experiment:
            expl = get_str_exp_one(user,
                                   recipeA_values,
                                   type_exp,
                                   listRestrictions,
                                   nutrients)
            if expl != "":
                type_for_recipe_a = type_exp + "A"
                explWithTypeA = {type_for_recipe_a : expl}
                explanations.update(explWithTypeA)

        #expls b
        for type_exp in one_recipe_experiment:
            expl = get_str_exp_one(user,
                                   recipeB_values,
                                   type_exp,
                                   listRestrictions,
                                   nutrients)
            if expl != "":
                type_for_recipe_B = type_exp + "B"
                explWithTypeA = {type_for_recipe_B: expl}
                explanations.update(explWithTypeA)

        expl = ""
        for type_exp in two_recipes_experiment:
            expl = get_str_exp_two(user,
                                   recipeA_values,
                                   recipeB_values,
                                   type_exp,
                                   listRestrictions,
                                   nutrients)
            if expl != "":
                explWithType = {type_exp: expl}
                explanations.update(explWithType)

        # list_exp.append(expl)

        # conversion Array to JSON
        json_exp = json.dumps({'explanations': explanations})


        return json_exp


api.add_resource(Explain, '/exp/')

if __name__ == '__main__':
    app.run(port=5003)
