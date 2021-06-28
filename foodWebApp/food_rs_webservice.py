from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps

import pandas as pd
import numpy as np

app = Flask(__name__)
api = Api(app)


class Mood(Resource):
    def get(self):

        url_dataset_it = "dataset.csv"
        url_dataset_en = "dataset_en.csv"
        url_dataset_en_v2 = "dataset_en_v2.csv"

        lang = request.args.get('lang')

        if lang == 'it':
            df = pd.read_csv(url_dataset_it)
        else:
            # df = pd.read_csv(url_dataset_en)
            df = pd.read_csv(url_dataset_en_v2, sep=';')


        # rich ingridients list
        richCalciumList = ["tofu", "latte", "yogurt", "parmigiano", "spinaci",
                           "piselli", "gombo", "trota", "zucca", "vongole"]

        richCalciumList_en = ["tofu", "milk", "yogurt", "parmigiano", "spinach",
                           "peas", "okra", "trout", "pumpkin", "clams"]

        richIronList = ["cereali", "manzo", "crostacei", "albicocche", "fagioli bianchi",
                        "spinaci", "cioccolato fondente", "quinoa", "funghi", "semi di zucca"]

        richIronList_en = ["grains", "beef", "shellfish", "apricots", "white beans",
                        "spinach," "dark chocolate," "quinoa," "mushrooms," "pumpkin seeds"]

        richLycopeneList = ["guaiave", "pomodoro", "anguria", "pompelmo", "papaia",
                            "peperoni rossi", "cachi", "asparagi", "cavoli rossi", "mango"]

        richLycopeneList_en = ["guavas", "tomato", "watermelon", "grapefruit", "papaya",
                            "red peppers," "persimmons," "asparagus," "red cabbage," "mango"]

        richBetaCaroteneList = ["patata dolce", "carote", "spinaci", "zucca", "melone",
                                "lattuga romana", "peperoni rossi", "albicocche", "broccoli", "piselli"]

        richBetaCaroteneList_en = ["sweet potato", "carrots", "spinach", "squash", "cantaloupe",
                                "lettuce", "red peppers", "apricots", "broccoli", "peas"]

        richAntioxidantList = richLycopeneList + richBetaCaroteneList

        richAntioxidantList_en = richLycopeneList_en + richBetaCaroteneList_en

        richVitaminCList = ["guaiave", "kiwi", "peperoni rossi", "fragole", "arance",
                            "papaya", "broccoli", "pomodoro", "piselli", "cavolo nero"]

        richVitaminCList_en = ["guavas," "kiwis," "red peppers," "strawberries," "oranges."
                            "papaya", "broccoli", "tomato", "peas", "kale"]

        richVitaminEList = ["semi di girasole", "mandorle", "avocado", "spinaci", "zucca",
                            "kiwi", "broccoli", "trota", "olio d'oliva", "gamberetti"]

        richVitaminEList_en = ["sunflower seeds", "almonds", "avocado", "spinach", "pumpkin",
                            "kiwi", "broccoli", "trout", "olive oil", "shrimp"]

        richVitaminDList = ["salmone", "castagna", "latte", "latte di soia", "tofu",
                            "yogurt", "cereali per la colazione", "succo d'arancia", "braciole di maiale", "uova"]

        richVitaminDList_en = ["salmon", "chestnut", "milk", "soy milk", "tofu",
                            "yogurt," "breakfast cereal," "orange juice," "pork chops," "eggs"]

        richMagnesium = ['crusca', 'mandorle', 'anacardi', 'cereali integrali', 'piselli', 'fagioli', 'datteri',
                         'aneto', 'fichi', 'nocciole']

        richMagnesium_en = ['bran', 'almonds', 'cashews', 'whole grains', 'peas', 'beans', 'dates',
                         'dill', 'figs', 'hazelnuts']

        cibiAntistress = ['latte intero', 'riso', 'pollo', 'cereali integrali', 'manzo', 'fagioli', 'noci',
                          'cioccolato', 'formaggio', 'broccoli']

        cibiAntistress_en = ['whole milk', 'rice', 'chicken', 'whole grain', 'beef', 'beans', 'nuts',
                          'chocolate', 'cheese', 'broccoli']

        # parametrization

        # The rescore_parameter function has become the core of the webservice after the cleanup and parameterization
        # of the project. All the rescore functions uses this subfunction now

        def rescore_parameter(param, score_update, low, high, score_low, score_mid, score_high):

            if score_low is not None:
                if param <= low:
                    score_update = score_update * score_low
                elif low < param < high:
                    score_update = score_update * score_mid
                else:
                    score_update = score_update * score_high

                return score_update

        # All the is rich functions do the same thing actually, return an indication of how many ingredients are rich in
        # said nutrient. You can actually generalize all these functions into one but, since this part of the project is
        # the one who is most subject to changes/improvements, i've created a function for each nutrient in order to not
        # unnecessarily complicate future work
        def isRichMagnesium(ingredients):
            listIngredients = ingredients.strip("[ ]").split(",")

            magnesium = 0
            if lang == 'it':
                for elem in richMagnesium:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        magnesium += 1
                mg = magnesium / len(richMagnesium)
            else:
                for elem in richMagnesium_en:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        magnesium += 1
                mg = magnesium / len(richMagnesium_en)
            return (mg)

        def isRichIron(ingredients):
            listIngredients = ingredients.strip("[ ]").split(",")

            Iron = 0
            if lang == 'it':
                for elem in richIronList:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        Iron += 1
                fe = Iron / len(richIronList)
            else:
                for elem in richIronList_en:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        Iron += 1
                fe = Iron / len(richIronList_en)
            return (fe)

        def isRichAntioxidant(ingredients):
            listIngredients = ingredients.strip("[ ]").split(",")

            AntiOxidant = 0
            if lang == 'it':
                for elem in richAntioxidantList:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        AntiOxidant += 1
                Ao = AntiOxidant / len(richAntioxidantList)
            else:
                for elem in richAntioxidantList_en:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        AntiOxidant += 1
                Ao = AntiOxidant / len(richAntioxidantList_en)
            return (Ao)

        def isRichVitaminC(ingredients):
            listIngredients = ingredients.strip("[ ]").split(",")

            VitaminC = 0
            if lang == 'it':
                for elem in richVitaminCList:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        VitaminC += 1
                Vc = VitaminC / len(richVitaminCList)
            else:
                for elem in richVitaminCList_en:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        VitaminC += 1
                Vc = VitaminC / len(richVitaminCList_en)
            return (Vc)

        def isRichVitaminD(ingredients):
            listIngredients = ingredients.strip("[ ]").split(",")

            VitaminD = 0
            if lang == 'it':
                for elem in richVitaminDList:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        VitaminD += 1
                Vd = VitaminD / len(richVitaminDList)
            else:
                for elem in richVitaminDList_en:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        VitaminD += 1
                Vd = VitaminD / len(richVitaminDList_en)
            return (Vd)

        def isRichVitaminE(ingredients):
            listIngredients = ingredients.strip("[ ]").split(",")

            VitaminE = 0
            if lang == 'it':
                for elem in richVitaminEList:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        VitaminE += 1
                Ve = VitaminE / len(richVitaminEList)
            else:
                for elem in richVitaminEList_en:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        VitaminE += 1
                Ve = VitaminE / len(richVitaminEList_en)
            return (Ve)

        def isRichCalcium(ingredients):
            listIngredients = ingredients.strip("[ ]").split(",")

            Calcium = 0
            if lang == 'it':
                for elem in richCalciumList:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        Calcium += 1
                Ca = Calcium / len(richCalciumList)
            else:
                for elem in richCalciumList_en:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        Calcium += 1
                Ca = Calcium / len(richCalciumList_en)
            return (Ca)

        def isAntistress(ingredients):
            listIngredients = ingredients.strip("[ ]").split(",")

            antistress = 0
            if lang == 'it':
                for elem in cibiAntistress:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        antistress += 1
                antiS = antistress / len(cibiAntistress)
            else:
                for elem in cibiAntistress_en:
                    if any(elem in ingredient.lower() for ingredient in listIngredients):
                        antistress += 1
                antiS = antistress / len(cibiAntistress_en)
            return (antiS)

        # score by richness
        def dfFromIngredient(df, searchIngrendient):
            new_rows = []
            returnDf = pd.DataFrame()

            for index, row in df.iterrows():
                listIngredients = row.ingredients.strip("[ ]").split(",")

                if any(not (ingredient.lower().find(searchIngrendient)) for ingredient in listIngredients):
                    new_rows.append(row)

            return returnDf.append(pd.DataFrame(new_rows, columns=df.columns))

        def rescoreOverweight(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=2, score_mid=0.9,
                                          score_high=0.4)
            # fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=2, score_mid=0.9,
                                          score_high=0.4)

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=2, score_mid=0.9,
                                          score_high=0.4)

            # fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.4, score_mid=1.1,
                                          score_high=2)

            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.4, score_mid=1.1,
                                          score_high=2)

            return new_score

        def rescoreObesity(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=2.5, score_mid=0.85,
                                          score_high=0.3)
            # fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=2.5, score_mid=0.85,
                                          score_high=0.3)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=2.5, score_mid=0.85,
                                          score_high=0.3)

            # fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.3, score_mid=1.15,
                                          score_high=2.5)

            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.3, score_mid=1.15,
                                          score_high=2.5)

            return new_score

        def rescoreObesityPlus(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=3, score_mid=0.8,
                                          score_high=0.2)
            # fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=3, score_mid=0.8,
                                          score_high=0.2)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=3, score_mid=0.8,
                                          score_high=0.2)

            # fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.2, score_mid=1.2,
                                          score_high=3)

            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.2, score_mid=1.2,
                                          score_high=3)
            return new_score

        def rescoreUnderweight(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=0.4, score_mid=1.1,
                                          score_high=2)

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.4, score_mid=1.1,
                                          score_high=2)

            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.4, score_mid=1.1,
                                          score_high=2)

            return new_score

        def rescoreActivityMedium(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=0.9, score_mid=1.25,
                                          score_high=1.5)
            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.9, score_mid=1.25,
                                          score_high=1.5)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.9, score_mid=1.25,
                                          score_high=1.5)

            return new_score

        def rescoreActivityHigh(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=0.85, score_mid=1.5,
                                          score_high=2)
            # fat
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.85, score_mid=1.5,
                                          score_high=2)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.85, score_mid=1.5,
                                          score_high=2)
            return new_score

        def rescoreStress(row):
            new_score = row.score

            # Sodium
            new_score = rescore_parameter(row.sodium, new_score, low=225, high=875, score_low=1.5, score_mid=1.25,
                                          score_high=1)

            if row.antistress >= 0.1:
                new_score = new_score * 1.25
            elif 0.2 < row.antistress < 0.3:
                new_score = new_score * 1.5
            else:
                new_score = new_score * 2

            return new_score

        def rescoreDepression(row):
            new_score = row.score

            # fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=0.5,
                                          score_mid=1,
                                          score_high=2)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.5,
                                          score_mid=1,
                                          score_high=2)

            #proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=2,
                                          score_mid=1,
                                          score_high=0.5)

            new_score = rescore_parameter(row.sugars, new_score, low=6, high=18, score_low=2,
                                          score_mid=1,
                                          score_high=0.5)

            return new_score

        def rescoreMoodBad(row):

            new_score = rescore_parameter(row.sugars, row.score, low=6, high=18, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            return new_score

        def rescore_less_sugar(row):

            new_score = rescore_parameter(row.sugars, row.score, low=6, high=18, score_low=2, score_mid=0.9,
                                          score_high=0.4)
            return new_score

        def rescore_good_food(row, food):
            listIngredients = row.ingredients.strip("[ ]").split(",")

            for ingredient in listIngredients:
                if food.lower() == ingredient.lower():
                    return row.score * 2

            return row.score

        def rescore_bad_food(row, food):
            listIngredients = row.ingredients.strip("[ ]").split(",")

            for ingredient in listIngredients:
                if food.lower() == ingredient.lower():
                    return row.score * 0.5

            return row.score

        def rescoreMagnesium(row):
            if row.magnesium == 0.1:
                return row.score * 1.25
            if row.magnesium == 0.2:
                return row.score * 1.5
            if row.magnesium == 0.3:
                return row.score * 2
            else:
                return row.score

        def rescoreIron(row):
            if row.iron == 0.1:
                return row.score * 1.25
            if row.iron == 0.2:
                return row.score * 1.5
            if row.iron == 0.3:
                return row.score * 2
            else:
                return row.score

        def rescoreAntiOxidant(row):
            if row.antioxidant == 0.1:
                return row.score * 1
            if row.antioxidant == 0.2:
                return row.score * 1.25
            if row.antioxidant == 0.3:
                return row.score * 2
            else:
                return row.score

        def rescoreCalcium(row):
            if row.calcium == 0.1:
                return row.score * 1.25
            if row.calcium == 0.2:
                return row.score * 1.5
            if row.calcium == 0.3:
                return row.score * 2
            else:
                return row.score

        def rescoreVitaminC(row):
            if row.vitaminC == 0.1:
                return row.score * 1.25
            if row.vitaminC == 0.2:
                return row.score * 1.5
            if row.vitaminC == 0.3:
                return row.score * 2
            else:
                return row.score

        def rescoreVitaminD(row):
            if row.vitaminD == 0.1:
                return row.score * 1.25
            if row.vitaminD == 0.2:
                return row.score * 1.5
            if row.vitaminD == 0.3:
                return row.score * 2
            else:
                return row.score

        def rescoreVitaminE(row):
            if row.vitaminE == 0.1:
                return row.score * 1.25
            if row.vitaminE == 0.2:
                return row.score * 1.5
            if row.vitaminE == 0.3:
                return row.score * 2
            else:
                return row.score

        def rescoreSleep(row):
            new_score = row.score

            # fat
            new_score = rescore_parameter(row.saturatedFat, new_score, low=1.35, high=4.05, score_low=2, score_mid=1,
                                          score_high=0.5)

            return new_score

        def rescoreDifficulty(row, difficulty):
            new_score = row.score

            if difficulty == 1:
                if row.difficulty == 'Molto facile':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            if difficulty == 2:
                if row.difficulty == 'Facile' or row.difficulty == 'Molto facile':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            if difficulty == 3:
                if row.difficulty == 'Media' or row.difficulty == 'Facile' or \
                        row.difficulty == 'Molto facile':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            if difficulty == 4:
                if row.difficulty == 'Difficile' or row.difficulty == 'Media' or \
                        row.difficulty == 'Facile' or row.difficulty == 'Molto facile':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            if difficulty == 5:
                if row.difficulty == 'Molto difficile' or row.difficulty == 'Difficile' or \
                        row.difficulty == 'Media' or row.difficulty == 'Facile' or row.difficulty == 'Molto facile':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            return new_score

        def rescoreGoalPlus(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.35, high=400.5, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)

            return new_score

        def rescoreGoalMinus(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=2, score_mid=0.95,
                                          score_high=0.5)
            # fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=2, score_mid=0.95,
                                          score_high=0.5)

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=2, score_mid=0.95,
                                          score_high=0.5)

            # fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.5, score_mid=1.05,
                                          score_high=2)

            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.5, score_mid=1.05,
                                          score_high=2)

            return new_score

        def rescoreCost(row, cost):
            new_score = row.score
            # if cost is 5 this function doesn't rescore

            if cost == 1:
                if row.cost == 'Molto basso':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            if cost == 2:
                if row.cost == 'Basso' or row.cost == 'Molto basso':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            if cost == 3:
                if row.cost == 'Medio' or row.cost == 'Basso' or \
                        row.cost == 'Molto basso':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            if cost == 4:
                if row.cost == 'Elevato' or row.cost == 'Medio' or \
                        row.cost == 'Basso' or row.cost == 'Molto basso':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 1

            return new_score

        def rescoreTime(row, time):
            new_score = row.score

            time_split = row.totalTime.split(sep='.')

            totalTime = int(time_split[1]) * 60 + int(time_split[2])

            if time == totalTime:
                new_score = new_score * 1.5
            elif time > totalTime:
                new_score = new_score * 2
            elif time < totalTime:
                new_score = new_score * 0.1

            return new_score

        def rescoreU20(row):
            new_score = row.score

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # saturated Fat
            new_score = rescore_parameter(row.saturatedFat, new_score, low=1.35, high=4.05, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # Fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            return new_score

        def rescoreU30(row):
            new_score = row.score

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # saturated Fat
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # Fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)

            return new_score

        def rescoreU40(row):
            new_score = row.score
            # Proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # Fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)

            return new_score

        def rescoreU50(row):
            new_score = row.score
            # Proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # Fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)

            return new_score

        def rescoreU60(row):
            new_score = row.score

            # Fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            #  saturatedFat
            new_score = rescore_parameter(row.saturatedFat, new_score, low=4.65, high=13.95, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)

            return new_score

        def rescoreO60(row):
            new_score = row.score

            # Proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)
            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.35, high=400.5, score_low=0.5,
                                          score_mid=1.05,
                                          score_high=2)

            return new_score

        def rescore_sex_M(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.35, high=400.5, score_low=0.9,
                                          score_mid=1.25,
                                          score_high=1.5)
            return new_score

        def score(row):
            score = row.ratingValue * np.log10(row.ratingCount)

            if np.isnan(score):
                score = 0

            return score

        # MARKER add column "score" to the dataframe
        df['score'] = df.apply(score, axis=1)

        # MARKER get request.args
        n = int(request.args.get('n')) if (request.args.get('n') is not None) else -1

        recipeName = request.args.get('recipeName')
        ingredient = request.args.get('ingredient')
        category = request.args.get('category')

        isLowNickel = int(request.args.get('isLowNickel')) if (request.args.get('isLowNickel') is not None) else ''
        isVegetarian = int(request.args.get('isVegetarian')) if (request.args.get('isVegetarian') is not None) else ''
        isLactoseFree = int(request.args.get('isLactoseFree')) if (
                request.args.get('isLactoseFree') is not None) else ''
        isGlutenFree = int(request.args.get('isGlutenFree')) if (request.args.get('isGlutenFree') is not None) else ''
        isLight = int(request.args.get('isLight')) if (request.args.get('isLight') is not None) else ''
        isDiabetes = int(request.args.get('isDiabetes')) if (request.args.get('isDiabetes') is not None) else ''
        isPregnant = int(request.args.get('isPregnant')) if (request.args.get('isPregnant') is not None) else ''

        user_difficulty = int(request.args.get('difficulty')) if (request.args.get('difficulty') is not None) else ''

        goal = int(request.args.get('goal')) if (request.args.get('goal') is not None) else ''
        user_cost = int(request.args.get('user_cost')) if (request.args.get('user_cost') is not None) else ''
        user_time = int(request.args.get('user_time')) if (request.args.get('user_time') is not None) else ''
        age = request.args.get('age')
        sex = request.args.get('sex')

        # orario
        hour = request.args.get('hour')

        # mood
        mood = request.args.get('mood')
        activity = request.args.get('activity')
        stress = request.args.get('stress')
        sleep = request.args.get('sleep')
        depression = request.args.get('depression')

        bmi = float(request.args.get('fatclass')) if (request.args.get('fatclass') is not None) else ''

        # MARKER filtro il DataFrame su nome della ricetta cercata
        if recipeName:
            df = df[df.title.str.contains(recipeName, case=False)]

        # MARKER filtro il DataFrame su ingrediente della ricetta cercato
        if ingredient:
            df = dfFromIngredient(df, ingredient)

        # MARKER change score for category - 'Primi piatti', 'Secondi piatti', 'Dolci'
        if category:
            df = df[df.category == category]

        # MARKER change score for restrictions
        if isLowNickel:
            df = df[df.isLowNickel == isLowNickel]

        if isVegetarian:
            df = df[df.isVegetarian == isVegetarian]

        if isLactoseFree:
            df = df[df.isLactoseFree == isLactoseFree]

        if isGlutenFree:
            df = df[df.isGlutenFree == isGlutenFree]

        if isLight:
            df = df[df.isLight == isLight]

        if isDiabetes:
            if lang == 'it':
                df.score = df.apply(rescore_good_food, axis=1, food='salmone')
                df.score = df.apply(rescore_good_food, axis=1, food='tonno')
                df.score = df.apply(rescore_good_food, axis=1, food='trota')
                df.score = df.apply(rescore_good_food, axis=1, food='sgombro')
                df.score = df.apply(rescore_good_food, axis=1, food='uova')
                df.score = df.apply(rescore_good_food, axis=1, food='yogurt')
                df.score = df.apply(rescore_good_food, axis=1, food='fagioli')
                df.score = df.apply(rescore_good_food, axis=1, food='noci')
                df.score = df.apply(rescore_good_food, axis=1, food='mandorle')
                df.score = df.apply(rescore_good_food, axis=1, food='nocciole')
            else:
                df.score = df.apply(rescore_good_food, axis=1, food='salmon')
                df.score = df.apply(rescore_good_food, axis=1, food='tuna')
                df.score = df.apply(rescore_good_food, axis=1, food='trout')
                df.score = df.apply(rescore_good_food, axis=1, food='mackerel')
                df.score = df.apply(rescore_good_food, axis=1, food='eggs')
                df.score = df.apply(rescore_good_food, axis=1, food='yogurt')
                df.score = df.apply(rescore_good_food, axis=1, food='beans')
                df.score = df.apply(rescore_good_food, axis=1, food='walnuts')
                df.score = df.apply(rescore_good_food, axis=1, food='almond')
                df.score = df.apply(rescore_good_food, axis=1, food='nuts')
            df.score = df.apply(rescore_less_sugar, axis=1)

        if isPregnant and sex != "M":
            if lang == 'it':
                df.score = df.apply(rescore_good_food, axis=1, food='formaggio')
                df.score = df.apply(rescore_good_food, axis=1, food='yogurt')
                df.score = df.apply(rescore_good_food, axis=1, food='fagioli')
                df.score = df.apply(rescore_good_food, axis=1, food='lenticchie')
                df.score = df.apply(rescore_good_food, axis=1, food='salmone')
                df.score = df.apply(rescore_good_food, axis=1, food='tonno')
                df.score = df.apply(rescore_good_food, axis=1, food='trota')
                df.score = df.apply(rescore_good_food, axis=1, food='sgombro')
                df.score = df.apply(rescore_good_food, axis=1, food='uova')
                df.score = df.apply(rescore_bad_food, axis=1, food='caffè')
            else:
                df.score = df.apply(rescore_good_food, axis=1, food='cheese')
                df.score = df.apply(rescore_good_food, axis=1, food='yogurt')
                df.score = df.apply(rescore_good_food, axis=1, food='beans')
                df.score = df.apply(rescore_good_food, axis=1, food='lentils')
                df.score = df.apply(rescore_good_food, axis=1, food='salmon')
                df.score = df.apply(rescore_good_food, axis=1, food='tuna')
                df.score = df.apply(rescore_good_food, axis=1, food='trout')
                df.score = df.apply(rescore_good_food, axis=1, food='mackerel')
                df.score = df.apply(rescore_good_food, axis=1, food='eggs')
                df.score = df.apply(rescore_bad_food, axis=1, food='coffee')

        # MARKER change score for bmi value
        if bmi < 19:
            # SOTTOPESO
            df.score = df.apply(rescoreUnderweight, axis=1)
        elif 25 <= bmi < 30:
            # SOVRAPPESO
            df.score = df.apply(rescoreOverweight, axis=1)
        elif 30 <= bmi < 35:
            # OBESITÀ CLASSE I
            df.score = df.apply(rescoreObesity, axis=1)
        elif bmi >= 35:
            # OBESITÀ CLASSE II
            df.score = df.apply(rescoreObesityPlus, axis=1)

        # MARKER change score if mood == 'bad'
        if mood == 'bad':
            df.score = df.apply(rescoreMoodBad, axis=1)
            if lang == 'it':
                df.score = df.apply(rescore_good_food, axis=1, food='salmone')
                df.score = df.apply(rescore_good_food, axis=1, food='tonno')
                df.score = df.apply(rescore_good_food, axis=1, food='trota')
                df.score = df.apply(rescore_good_food, axis=1, food='sgombro')
                df.score = df.apply(rescore_good_food, axis=1, food='cioccolato')
                df.score = df.apply(rescore_good_food, axis=1, food='yogurt')
                df.score = df.apply(rescore_good_food, axis=1, food='banana')
                df.score = df.apply(rescore_good_food, axis=1, food='avena')
                df.score = df.apply(rescore_good_food, axis=1, food='caffè')
                df.score = df.apply(rescore_good_food, axis=1, food='nocciole')
                df.score = df.apply(rescore_good_food, axis=1, food='fagioli')
                df.score = df.apply(rescore_good_food, axis=1, food='lenticchie')
            else:
                df.score = df.apply(rescore_good_food, axis=1, food='salmon')
                df.score = df.apply(rescore_good_food, axis=1, food='tuna')
                df.score = df.apply(rescore_good_food, axis=1, food='trout')
                df.score = df.apply(rescore_good_food, axis=1, food='mackerel')
                df.score = df.apply(rescore_good_food, axis=1, food='chocolate')
                df.score = df.apply(rescore_good_food, axis=1, food='yogurt')
                df.score = df.apply(rescore_good_food, axis=1, food='banana')
                df.score = df.apply(rescore_good_food, axis=1, food='oat')
                df.score = df.apply(rescore_good_food, axis=1, food='coffee')
                df.score = df.apply(rescore_good_food, axis=1, food='nuts')
                df.score = df.apply(rescore_good_food, axis=1, food='beans')
                df.score = df.apply(rescore_good_food, axis=1, food='lentils')

        # MARKER change score for activity
        if activity == 'medium':
            df.score = df.apply(rescoreActivityMedium, axis=1)
        elif activity == 'high':
            df.score = df.apply(rescoreActivityHigh, axis=1)

        # MARKER change score if stress == 'yes'
        if stress == 'yes':
            df['antistress'] = df.ingredients.apply(isAntistress)
            df.score = df.apply(rescoreStress, axis=1)
            if lang == 'it':
                df.score = df.apply(rescore_bad_food, axis=1, food='caffè')
            else:
                df.score = df.apply(rescore_bad_food, axis=1, food='coffee')

        # MARKER change score if sleep == 'low'
        if sleep == 'low':
            df['magnesium'] = df.ingredients.apply(isRichMagnesium)
            df.score = df.apply(rescoreMagnesium, axis=1)
            df.score = df.apply(rescoreSleep, axis=1)
            if lang == 'it':
                df.score = df.apply(rescore_good_food, axis=1, food='tacchino')
                df.score = df.apply(rescore_good_food, axis=1, food='cammomilla')
                df.score = df.apply(rescore_good_food, axis=1, food='kiwi')
                df.score = df.apply(rescore_good_food, axis=1, food='ciliegie')
                df.score = df.apply(rescore_good_food, axis=1, food='salmone')
                df.score = df.apply(rescore_good_food, axis=1, food='tonno')
                df.score = df.apply(rescore_good_food, axis=1, food='trota')
                df.score = df.apply(rescore_good_food, axis=1, food='sgombro')
                df.score = df.apply(rescore_good_food, axis=1, food='noci')
                df.score = df.apply(rescore_good_food, axis=1, food='riso')
                df.score = df.apply(rescore_good_food, axis=1, food='formaggio')
                df.score = df.apply(rescore_good_food, axis=1, food='yogurt')
                df.score = df.apply(rescore_good_food, axis=1, food='avena')
                df.score = df.apply(rescore_bad_food, axis=1, food='caffè')
            else:
                df.score = df.apply(rescore_good_food, axis=1, food='turkey')
                df.score = df.apply(rescore_good_food, axis=1, food='chamomile')
                df.score = df.apply(rescore_good_food, axis=1, food='kiwi')
                df.score = df.apply(rescore_good_food, axis=1, food='cherry')
                df.score = df.apply(rescore_good_food, axis=1, food='salmon')
                df.score = df.apply(rescore_good_food, axis=1, food='tuna')
                df.score = df.apply(rescore_good_food, axis=1, food='trout')
                df.score = df.apply(rescore_good_food, axis=1, food='mackerel')
                df.score = df.apply(rescore_good_food, axis=1, food='walnuts')
                df.score = df.apply(rescore_good_food, axis=1, food='rice')
                df.score = df.apply(rescore_good_food, axis=1, food='cheese')
                df.score = df.apply(rescore_good_food, axis=1, food='yogurt')
                df.score = df.apply(rescore_good_food, axis=1, food='oat')
                df.score = df.apply(rescore_bad_food, axis=1, food='coffee')

        # MARKER change score if hour == 'evening'
        if hour == 'evening':
            if lang == 'it':
                df.score = df.apply(rescore_bad_food, axis=1, food='caffè')
                df.score = df.apply(rescore_bad_food, axis=1, food='cioccolato')
            else:
                df.score = df.apply(rescore_bad_food, axis=1, food='coffee')
                df.score = df.apply(rescore_bad_food, axis=1, food='chocolate')

        # MARKER change score if depression == 'yes'
        if depression == 'yes':
            df.score = df.apply(rescoreDepression, axis=1)

            df['magnesium'] = df.ingredients.apply(isRichMagnesium)
            df.score = df.apply(rescoreMagnesium, axis=1)

            if lang == 'it':
                df.score = df.apply(rescore_bad_food, axis=1, food='caffè')
            else:
                df.score = df.apply(rescore_bad_food, axis=1, food='coffee')

        # MARKER change score for user_difficulty
        if user_difficulty != '':
            df.score = df.apply(rescoreDifficulty, difficulty=user_difficulty, axis=1)

        # MARKER change score for goal
        if goal != '':
            # se vuole aumentare di peso e non è sovrappeso
            if goal == 1 and bmi < 25:
                df.score = df.apply(rescoreGoalPlus, axis=1)

            # se vuole perdere peso e non è sottopeso
            if goal == -1 and bmi > 19:
                df.score = df.apply(rescoreGoalMinus, axis=1)

        # MARKER change score for user_cost - value '5' stands for 'not important', so we don't sway the recommender
        if user_cost != '':
            df.score = df.apply(rescoreCost, cost=user_cost, axis=1)

        # MARKER change score for user_time - value '0' stands for 'no costraints', so we don't sway the recommender
        if user_time != '' and user_time != 0:
            df.score = df.apply(rescoreTime, time=user_time, axis=1)

        # MARKER change score for sex
        if sex == "M":
            df.score = df.apply(rescore_sex_M, axis=1)

        # MARKER change score for age
        if age == 'U20':
            df.score = df.apply(rescoreU20, axis=1)
        elif age == 'U30':
            df.score = df.apply(rescoreU30, axis=1)
            df['iron'] = df.ingredients.apply(isRichIron)
            df.score = df.apply(rescoreIron, axis=1)
            df['calcium'] = df.ingredients.apply(isRichCalcium)
            df.score = df.apply(rescoreCalcium, axis=1)
        elif age == 'U40':
            df.score = df.apply(rescoreU40, axis=1)
            df['magnesium'] = df.ingredients.apply(isRichMagnesium)
            df.score = df.apply(rescoreMagnesium, axis=1)
        elif age == 'U50':
            df.score = df.apply(rescoreU50, axis=1)
            df['magnesium'] = df.ingredients.apply(isRichMagnesium)
            df.score = df.apply(rescoreMagnesium, axis=1)
        elif age == 'U60':
            df.score = df.apply(rescoreU60, axis=1)
            df['calcium'] = df.ingredients.apply(isRichCalcium)
            df.score = df.apply(rescoreCalcium, axis=1)
            df['vitaminD'] = df.ingredients.apply(isRichVitaminD)
            df.score = df.apply(rescoreVitaminD, axis=1)
        elif age == 'O60':
            df.score = df.apply(rescoreO60, axis=1)
            df['calcium'] = df.ingredients.apply(isRichCalcium)
            df.score = df.apply(rescoreCalcium, axis=1)
            df['vitaminD'] = df.ingredients.apply(isRichVitaminD)
            df.score = df.apply(rescoreVitaminD, axis=1)

        # MARKER sort dataframe by score value
        df = df.sort_values('score', ascending=False)

        # print(df[['title', 'score']].head(n))

        return df.head(n).to_json(orient='split')


# MARKER create API
api.add_resource(Mood, '/mood/')

if __name__ == '__main__':
    app.run(port=5009)
