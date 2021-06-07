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

        lang = request.args.get('lang')

        if lang == 'en':
            df = pd.read_csv(url_dataset_en)

        else:
            df = pd.read_csv(url_dataset_it)

        # rich ingridients list
        richCalciumList = ["tofu", "latte", "yogurt", "parmigiano", "spinaci",
                           "piselli dagli occhi neri", "gombo", "trota", "zucca", "vongole"]

        richIronList = ["cereali", "manzo", "crostacei", "albicocche", "fagioli bianchi",
                        "spinaci", "cioccolato fondente", "quinoa", "funghi", "semi di zucca"]

        richLycopeneList = ["guaiave", "pomodoro", "anguria", "pompelmo", "papaia",
                            "peperoni rossi", "cachi", "asparagi", "cavoli rossi", "mango"]

        richBetaCaroteneList = ["patata dolce", "carote", "spinaci", "zucca", "melone",
                                "lattuga romana", "peperoni rossi", "albicocche", "broccoli", "piselli"]
        richAntioxidantList = richLycopeneList + richBetaCaroteneList

        richVitaminCList = ["guaiave", "kiwi", "peperoni rossi", "fragole", "arance",
                            "papaya", "broccoli", "pomodoro", "piselli", "cavolo nero"]

        richVitaminEList = ["semi di girasole", "mandorle", "avocado", "spinaci", "zucca",
                            "kiwi", "broccoli", "trota", "olio d'oliva", "gamberetti"]

        richVitaminDList = ["salmone", "castagna", "latte", "latte di soia", "tofu",
                            "yogurt", "cereali per la colazione", "succo d'arancia", "braciole di maiale", "uova"]
        richMagnesium = ['crusca', 'mandorle', 'anacardi', 'cereali integrali', 'piselli', 'fagioli', 'datteri',
                         'aneto', 'fichi', 'nocciole']

        cibiAntistress = ['latte intero', 'riso', 'pollo', 'cereali integrali', 'manzo', 'fagioli', 'noci',
                          'cioccolato', 'formaggio', 'broccoli']

        # parametrization

        # The rescore_parameter function has become the core of the webservice after the cleanup and parameterization
        # of the project. All the rescore functions uses this subfunction now

        def rescore_parameter(param, score_update, low, high, score_low, score_mid, score_high):

            if score_low is not None:
                if param < low:
                    score_update = score_update * score_low
                elif low < param < high:
                    score_update = score_update * score_mid
                elif param > high:
                    score_update = score_update * score_high
                else:
                    if low < param < high:
                        score_update = score_update * score_mid
                    elif param > high:
                        score_update = score_update * score_high

                return score_update

        # All the is rich functions do the same thing actually, return an indication of how many ingredients are rich in
        # said nutrient. You can actually generalize all these functions into one but, since this part of the project is
        # the one who is most subject to changes/improvements, i've created a function for each nutrient in order to not
        # unnecessarily complicate future work
        def isRichMagnesium(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            magnesium = 0
            for elem in richMagnesium:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    magnesium += 1
            mg = magnesium / len(richMagnesium)
            return (mg)

        def isRichIron(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            Iron = 0
            for elem in richIronList:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    Iron += 1
            fe = Iron / len(richIronList)
            return (fe)

        def isRichAntioxidant(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            AntiOxidant = 0
            for elem in richAntioxidantList:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    AntiOxidant += 1
            Ao = AntiOxidant / len(richAntioxidantList)
            return (Ao)

        def isRichVitaminC(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            VitaminC = 0
            for elem in richVitaminCList:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    VitaminC += 1
            Vc = VitaminC / len(richVitaminCList)
            return (Vc)

        def isRichVitaminD(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            VitaminD = 0
            for elem in richVitaminDList:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    VitaminD += 1
            Vd = VitaminD / len(richVitaminDList)
            return (Vd)

        def isRichVitaminE(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            VitaminE = 0
            for elem in richVitaminEList:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    VitaminE += 1
            Ve = VitaminE / len(richVitaminEList)
            return (Ve)

        def isRichCalcium(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            Calcium = 0
            for elem in richCalciumList:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    Calcium += 1
            Ca = Calcium / len(richCalciumList)
            return (Ca)


        # score by richness

        def dfFromIngredient(df, searchIngrendient):
            new_rows = []
            returnDf = pd.DataFrame()

            for index, row in df.iterrows():
                listIngredients = row.ingredients.strip("[ ]").split(", ")

                if any(not (ingredient.lower().find(searchIngrendient)) for ingredient in listIngredients):
                    new_rows.append(row)

            return returnDf.append(pd.DataFrame(new_rows, columns=df.columns))

        def rescoreOverweight(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=2, score_mid=1.2,
                                          score_high=0.1)
            # fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=2, score_mid=1.2,
                                          score_high=0.1)

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1, score_mid=1.2,
                                          score_high=1.5)

            # fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.1, score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescoreObesity(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=3, score_mid=1.2,
                                          score_high=0.01)
            # fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=3, score_mid=1,
                                          score_high=0.01)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.01, score_mid=1,
                                          score_high=2.5)

            # fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.01, score_mid=1,
                                          score_high=3)
            return new_score

        def rescoreObesityPlus(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=4, score_mid=0.9,
                                          score_high=0.001)
            # fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=4, score_mid=0.9,
                                          score_high=0.001)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.001, score_mid=0.9,
                                          score_high=3.5)

            # fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.001, score_mid=0.9,
                                          score_high=4)

            return new_score

        def rescoreUnderweight(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=0.1, score_mid=1.2,
                                          score_high=2)

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1, score_mid=1.2,
                                          score_high=2)

            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1, score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescoreActivityMedium(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=0.1, score_mid=1.2,
                                          score_high=1.5)
            # proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1, score_mid=1.2,
                                          score_high=1.5)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1, score_mid=1.2,
                                          score_high=1.5)

            return new_score

        def rescoreActivityHigh(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.5, high=400.5, score_low=2, score_mid=1.2,
                                          score_high=0.1)
            # fat
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1, score_mid=1.2,
                                          score_high=2)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1, score_mid=1.2,
                                          score_high=2)
            return new_score

        def isAntistress(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            antistress = 0
            for elem in cibiAntistress:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    antistress += 1
            antiS = antistress / len(cibiAntistress)
            return (antiS)

        # cleanup
        def rescoreStress(row):
            new_score = row.score

            if row.sodium < sodiumAvg - sodiumStd:
                new_score = new_score * 2
            if sodiumAvg - sodiumStd <= row.sodium <= sodiumAvg + sodiumStd:
                new_score = new_score * 1.2
            if row.sodium > sodiumAvg + sodiumStd:
                new_score = new_score * 0.1

            if row.antistress == 0.1:
                new_score = new_score * 10
            if row.antistress == 0.2:
                new_score = new_score * 20
            if row.antistress >= 0.3:
                new_score = new_score * 30

            return new_score

        def rescoreDepression(row):
            new_score = row.score

            # Saturated Fat
            new_score = rescore_parameter(row.saturatedFat, new_score, low=1.35, high=4.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # fibers
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescoreMoodBad(row):

            new_score = rescore_parameter(row.sugar, row.score, low=6, high=18, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            return new_score

        def rescoreCoffe(row):
            listIngredients = row.ingredients.strip("[ ]").split(", ")

            if 'caffè' in listIngredients:
                return row.score * 0.5
            if 'Caffè' in listIngredients:
                return row.score * 0.5
            else:
                return row.score


        def rescoreMagnesium(row):
            if row.magnesium == 0.1:
                return row.score * 10
            if row.magnesium == 0.2:
                return row.score * 20
            if row.magnesium == 0.3:
                return row.score * 30
            else:
                return row.score

        def rescoreIron(row):
            if row.iron == 0.1:
                return row.score * 10
            if row.iron == 0.2:
                return row.score * 20
            if row.iron == 0.3:
                return row.score * 30
            else:
                return row.score

        def rescoreAntiOxidant(row):
            if row.antioxidant == 0.1:
                return row.score * 10
            if row.antioxidant == 0.2:
                return row.score * 20
            if row.antioxidant == 0.3:
                return row.score * 30
            else:
                return row.score

        def rescoreCalcium(row):
            if row.calcium == 0.1:
                return row.score * 10
            if row.calcium == 0.2:
                return row.score * 20
            if row.calcium == 0.3:
                return row.score * 30
            else:
                return row.score

        def rescoreVitaminC(row):
            if row.vitaminC == 0.1:
                return row.score * 10
            if row.vitaminC == 0.2:
                return row.score * 20
            if row.vitaminC == 0.3:
                return row.score * 30
            else:
                return row.score

        def rescoreVitaminD(row):
            if row.vitaminD == 0.1:
                return row.score * 10
            if row.vitaminD == 0.2:
                return row.score * 20
            if row.vitaminD == 0.3:
                return row.score * 30
            else:
                return row.score

        def rescoreVitaminE(row):
            if row.vitaminE == 0.1:
                return row.score * 10
            if row.vitaminE == 0.2:
                return row.score * 20
            if row.vitaminE == 0.3:
                return row.score * 30
            else:
                return row.score

        def rescoreSleep(row):
            new_score = row.score

            if row.fat > 13.95:
                new_score = new_score * 0.1

            return new_score

        def rescoreDifficulty(row, difficulty):
            new_score = row.score

            if difficulty == 1:
                if row.difficulty == 'Molto facile':
                    new_score = new_score * 2

            if difficulty == 2:
                if row.difficulty == 'Facile':
                    new_score = new_score * 2
                if row.difficulty == 'Molto facile':
                    new_score = new_score * 1.5

            if difficulty == 3:
                if row.difficulty == 'Media':
                    new_score = new_score * 2
                if row.difficulty == 'Facile':
                    new_score = new_score * 1.5
                if row.difficulty == 'Molto facile':
                    new_score = new_score * 1.5

            if difficulty == 4:
                if row.difficulty == 'Difficile':
                    new_score = new_score * 2
                if row.difficulty == 'Media':
                    new_score = new_score * 1.5
                if row.difficulty == 'Facile':
                    new_score = new_score * 1.5
                if row.difficulty == 'Molto facile':
                    new_score = new_score * 1.5

            if difficulty == 5:
                if row.difficulty == 'Molto difficile':
                    new_score = new_score * 2
                if row.difficulty == 'Difficile':
                    new_score = new_score * 1.5
                if row.difficulty == 'Media':
                    new_score = new_score * 1.5
                if row.difficulty == 'Facile':
                    new_score = new_score * 1.5
                if row.difficulty == 'Molto facile':
                    new_score = new_score * 1.5

            return new_score

        def rescoreGoalPlus(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.35, high=400.5, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # proteins
            new_score = rescore_parameter(row.calories, new_score, low=3.35, high=10.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescoreGoalMinus(row):
            new_score = row.score

            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.35, high=400.5, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            if row.fat < 4.65:
                new_score = new_score * 2
            if row.fat > 13.95:
                new_score = new_score * 0.1

            return new_score

        def rescoreCost(row, cost):
            new_score = row.score
            # if cost is 5 this function doesn't rescore

            if cost == 1:
                if row.cost == 'Molto basso':
                    new_score = new_score * 2
                else:
                    new_score = new_score * 0.1

            if cost == 2:
                if row.cost == 'Basso':
                    new_score = new_score * 2
                elif row.cost == 'Molto basso':
                    new_score = new_score * 1.5
                else:
                    new_score = new_score * 0.1

            if cost == 3:
                if row.cost == 'Medio':
                    new_score = new_score * 2
                elif row.cost == 'Basso':
                    new_score = new_score * 1.5
                elif row.cost == 'Molto basso':
                    new_score = new_score * 1.5
                else:
                    new_score = new_score * 0.1

            if cost == 4:
                if row.cost == 'Elevato':
                    new_score = new_score * 2
                elif row.cost == 'Medio':
                    new_score = new_score * 1.5
                elif row.cost == 'Basso':
                    new_score = new_score * 1.5
                elif row.cost == 'Molto basso':
                    new_score = new_score * 1.5

            return new_score

        def rescoreTime(row, time):
            new_score = row.score

            i = len(row.totalTime) - 2
            potenzaDieci = 1
            totalTime = 0
            while i >= 2:
                totalTime = totalTime + int(row.totalTime[i]) * potenzaDieci
                potenzaDieci = potenzaDieci * 10
                i -= 1

            if time == totalTime:
                new_score = new_score * 2
            elif time < totalTime:
                new_score = new_score * 0.1
            elif time > totalTime:
                new_score = new_score * 1.5

            return new_score

        def rescoreU20(row):
            new_score = row.score

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # saturated Fat
            new_score = rescore_parameter(row.saturatedFat, new_score, low=1.35, high=4.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # Fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            return new_score

        def rescoreU30(row):
            new_score = row.score

            # carbohydrates
            new_score = rescore_parameter(row.carbohydrates, new_score, low=18, high=54, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # saturated Fat
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # Fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescoreU40(row):
            new_score = row.score
            # Proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # Fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescoreU50(row):
            new_score = row.score
            # Proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # Fat
            new_score = rescore_parameter(row.fat, new_score, low=4.65, high=13.95, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescoreU60(row):
            new_score = row.score

            # Fibers
            new_score = rescore_parameter(row.fibers, new_score, low=1.65, high=4.95, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            #  Fat
            new_score = rescore_parameter(row.saturatedFat, new_score, low=4.65, high=13.95, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescoreO60(row):
            new_score = row.score

            # Proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.35, high=400.5, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)

            return new_score

        def rescore_sex_M(row):
            new_score = row.score

            # Proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.35, high=400.5, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            return new_score

        def rescore_sex_F(row):
            new_score = row.score

            # Proteins
            new_score = rescore_parameter(row.proteins, new_score, low=3.35, high=10.05, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            # calories
            new_score = rescore_parameter(row.calories, new_score, low=133.35, high=400.5, score_low=0.1,
                                          score_mid=1.2,
                                          score_high=2)
            return new_score

        def score(row):
            score = row.ratingValue * np.log10(row.ratingCount)
            return score

        # TODO start script

        df['score'] = df.apply(score, axis=1)

        # calcolo medie prima di 'tagliare' il DataFrame
        # sugarAvg = df.sugars.mean()
        # sugarStd = df.sugars.std()

        # proteinsAvg = df.proteins.mean()
        # proteinsStd = df.proteins.std()

        # caloriesAvg = df.calories.mean()
        # caloriesStd = df.calories.std()

        # fatAvg = df.fat.mean()
        # fatStd = df.fat.std()

        # sFatAvg = df.saturatedFat.mean()
        # sFatStd = df.saturatedFat.std()

        sodiumAvg = df.sodium.mean()
        sodiumStd = df.sodium.std()

        # carbsAvg = df.carbohydrates.mean()
        # carbsStd = df.carbohydrates.std()

        # fiberAvg = df.fibers.mean()
        # fiberStd = df.fibers.std()

        # accorgimenti parametri
        n = int(request.args.get('n')) if (request.args.get('n') is not None) else -1

        recipeName = request.args.get('recipeName')
        ingredient = request.args.get('ingredient')
        category = request.args.get('category')
        cost = request.args.get('cost')

        isLowNickel = int(request.args.get('isLowNickel')) if (request.args.get('isLowNickel') is not None) else ''
        isVegetarian = int(request.args.get('isVegetarian')) if (request.args.get('isVegetarian') is not None) else ''
        isLactoseFree = int(request.args.get('isLactoseFree')) if (
                request.args.get('isLactoseFree') is not None) else ''
        isGlutenFree = int(request.args.get('isGlutenFree')) if (request.args.get('isGlutenFree') is not None) else ''
        isLight = int(request.args.get('isLight')) if (request.args.get('isLight') is not None) else ''
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

        # overweight = request.args.get('overweight')
        # underweight = request.args.get('underweight')

        # height = request.args.get('height')
        # weight = request.args.get('weight')
        # bmi = weight / (height * height)

        bmi = float(request.args.get('fatclass')) if (request.args.get('fatclass') is not None) else ''

        healthy = request.args.get('healthy')

        # filtro il DF sulle ricette salutari
        # https://acmrecsys.github.io/rsss2019/Food-Recommender-ctrattner.pdf
        if healthy == 'high':
            # print("healthy: ", healthy)
            df = df[(df.sugars <= 5) & (df.fat <= 3) & (df.saturatedFat <= 1.5)]
        elif healthy == 'medium':
            # print("healthy: ", healthy)
            df = df[(df.sugars >= 5) & (df.sugars <= 15) &
                    (df.fat >= 3) & (df.fat <= 20) &
                    (df.saturatedFat >= 1.5) & (df.saturatedFat <= 5)
                    ]
        elif healthy == 'low':
            # print("healthy: ", healthy)
            df = df[(df.sugars >= 15) & (df.fat >= 20) & (df.saturatedFat > 5) & (df.sodium >= 1.5)]

        # filtro il DataFrame su nome della ricetta cercata
        if recipeName:
            # print("recipeName: " + recipeName)
            df = df[df.title.str.contains(recipeName, case=False)]

        # filtro il DataFrame su ingrediente della ricetta cercato

        if ingredient:
            # print("ingredient: " + ingredient)
            df = dfFromIngredient(df, ingredient)

        # categories = df.category.unique()
        # ['Dolci', 'Primi piatti', 'Lievitati', 'Salse e Sughi', 'Piatti Unici', 'Contorni', 'Antipasti',
        # 'Secondi piatti','Torte salate', 'Bevande', 'Insalate', 'Marmellate e Conserve']

        if category:
            # print('category: ' + category)
            df = df[df.category == category]

        # cost = df.cost.unique()
        # ['Molto basso', 'Medio', 'Basso', 'None', 'Elevato', 'Molto elevata']

        if cost:
            # print("cost: " + cost)
            df = df[df.cost == cost]

        if isLowNickel:
            # print("isLowNickel: " + str(isLowNickel))
            df = df[df.isLowNickel == isLowNickel]

        if isVegetarian:
            # print("isVegetarian: " + str(isVegetarian))
            df = df[df.isVegetarian == isVegetarian]

        if isLactoseFree:
            # print("isLactoseFree: " + str(isLactoseFree))
            df = df[df.isLactoseFree == isLactoseFree]

        if isGlutenFree:
            # print("isGlutenFree: " + str(isGlutenFree))
            df = df[df.isGlutenFree == isGlutenFree]

        if isLight:
            # print("isLight: " + str(isLight))
            df = df[df.isLight == isLight]

        # if overweight:
        # print('overweight:', overweight)
        # df.score = df.apply(rescoreOverweight, axis=1)
        # df = df.sort_values('score', ascending=False)
        # print(df[['title', 'score']].head(10))

        # if underweight:
        # print('underweight: ', underweight)
        # df.score = df.apply(rescoreUnderweight, axis=1)
        # df = df.sort_values('score', ascending=False)
        # print(df[['title', 'score']].head(10))

        bmiWeight = 'normal'
        if bmi < 19:
            bmiWeight = 'under'
            df.score = df.apply(rescoreUnderweight, axis=1)
        elif 25 <= bmi < 30:
            bmiWeight = 'over'
            df.score = df.apply(rescoreOverweight, axis=1)
        elif 30 <= bmi < 35:
            bmiWeight = 'over'
            df.score = df.apply(rescoreObesity, axis=1)
        elif bmi >= 35:
            bmiWeight = 'over'
            df.score = df.apply(rescoreObesityPlus, axis=1)
        df = df.sort_values('score', ascending=False)

        if mood == 'bad':
            # print('mood: bad')
            # print("sugarAvg: " + str(sugarAvg))

            # df = df[df.sugar > sugarAvg]
            df.score = df.apply(rescoreMoodBad, axis=1)
            df = df.sort_values('score', ascending=False)
            # print(df[['title', 'score']].head(10))

        if activity == 'medium':
            df.score = df.apply(rescoreActivityMedium, axis=1)
            df = df.sort_values('score', ascending=False)
        elif activity == 'high':
            # print('activity: high')
            # print("caloriesAvg: " + str(caloriesAvg))
            # print("proteinsAvg: " + str(proteinsAvg))

            # df = df[(df.calories > caloriesAvg) & (df.proteins > proteinsAvg)]
            df.score = df.apply(rescoreActivityHigh, axis=1)
            df = df.sort_values('score', ascending=False)
            # print(df[['title', 'score']].head(10))

        # stress => cibo salato (https://www.nutritestesso.it/it/lo-stretto-legame-cibo-ed-emozioni/)
        if stress == 'yes':
            # print('stress : ' + str(stress))
            print("sodiumAvg: " + str(sodiumAvg))

            # df = df[df.sodium > sodiumAvg]
            df['antistress'] = df.ingredients.apply(isAntistress)
            df.score = df.apply(rescoreStress, axis=1)
            df.score = df.apply(rescoreCoffe, axis=1)
            df = df.sort_values('score', ascending=False)
            # print(df[['title', 'score']].head(10))

        # poco sonno => mangia magnesio
        if sleep == 'low':
            # print("sleep: " + sleep)
            # df = df[df.magnesium > 0]
            df['magnesium'] = df.ingredients.apply(isRichMagnesium)
            df.score = df.apply(rescoreMagnesium, axis=1)
            df.score = df.apply(rescoreCoffe, axis=1)
            df.score = df.apply(rescoreSleep, axis=1)

        # sera => ricalcolo il caffe
        if hour == 'evening':
            # print ("hour: " + hour)
            df.score = df.apply(rescoreCoffe, axis=1)

        # depressione => meno grassi
        if depression == 'yes':
            # print ("depression: " + depression)
            # print("fatAvg: " + str(fatAvg))

            # df = df[df.fat < fatAvg]
            df['magnesium'] = df.ingredients.apply(isRichMagnesium)
            df.score = df.apply(rescoreDepression, axis=1)
            df.score = df.apply(rescoreCoffe, axis=1)
            df.score = df.apply(rescoreMagnesium, axis=1)
            df = df.sort_values('score', ascending=False)
            # print(df[['title', 'score']].head(10))

        if user_difficulty != '':
            # print ('user_difficulty: ', user_difficulty)
            df.score = df.apply(rescoreDifficulty, difficulty=user_difficulty, axis=1)
            df = df.sort_values('score', ascending=False)
            # print(df[['title', 'score']].head(10))

        if goal != '':
            # print ('goal: ', goal)

            # se vuole prendere peso e non è sovrappeso
            if bmiWeight != 'over' and goal == 1:
                # if((not(overweight)) and goal == 1):
                df.score = df.apply(rescoreGoalPlus, axis=1)
            # se vuole perdere peso e non è sottopeso
            if bmiWeight != 'under' and goal == -1:
                df.score = df.apply(rescoreGoalMinus, axis=1)

            df = df.sort_values('score', ascending=False)

        # value '5' stands for 'not important', so we don't sway the recommender
        if user_cost != '':
            # print ('user_cost: ', user_cost)
            df.score = df.apply(rescoreCost, cost=user_cost, axis=1)
            df = df.sort_values('score', ascending=False)

        # value '0' stands for 'no costraints', so we don't sway the recommender
        if user_time != '':
            # print ('user_time: ', user_time)
            if user_time == 0:
                user_time = 200
            df.score = df.apply(rescoreTime, time=user_time, axis=1)
            df = df.sort_values('score', ascending=False)
        if sex == "M":
            df.score = df.apply(rescore_sex_M, axis=1)
        else:
            df.score = df.apply(rescore_sex_F, axis=1)

            # print ('age: ', age)
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
            df.score = df.apply(rescoreDepression, axis=1)
        elif age == 'U50':
            df.score = df.apply(rescoreU40, axis=1)
            df['magnesium'] = df.ingredients.apply(isRichMagnesium)
            df.score = df.apply(rescoreDepression, axis=1)
        elif age == 'U60':
            df.score = df.apply(rescoreU60, axis=1)
            df['calcium'] = df.ingredients.apply(isRichCalcium)
            df.score = df.apply(rescoreCalcium, axis=1)
            df['vitaminD'] = df.ingredients.apply(isRichCalcium)
            df.score = df.apply(rescoreCalcium, axis=1)
        elif age == 'O60':
            df.score = df.apply(rescoreO60, axis=1)
            df['calcium'] = df.ingredients.apply(isRichCalcium)
            df.score = df.apply(rescoreCalcium, axis=1)
            df['vitaminD'] = df.ingredients.apply(isRichCalcium)
            df.score = df.apply(rescoreCalcium, axis=1)

        df = df.sort_values('score', ascending=False)

        return df.head(n).sample(frac=1).to_json(orient='split')


api.add_resource(Mood, '/mood/')

if __name__ == '__main__':
    app.run(port=5009)
