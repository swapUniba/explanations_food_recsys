from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps

import pandas as pd
import numpy as np

app = Flask(__name__)
api = Api(app)

class Mood(Resource):
    def get(self):

        url_dataset_it = 'dataset.csv'
        url_dataset_en = 'dataset_en.csv'

        lang = request.args.get('lang')

        if lang == 'en':
            df = pd.read_csv(url_dataset_en)

        else:
            df = pd.read_csv(url_dataset_it)

        # print('dataset language: ', lang)

        # dfFromIngredient
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

            if row.calories < 133.35:
                new_score = new_score * 2
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 1.2
            if row.calories > 400.05:
                new_score = new_score * 0.1

            if row.fat < 4.65:
                new_score = new_score * 2
            if row.fat >= 4.65 and row.fat <= 13.95:
                new_score = new_score * 1.2
            if row.fat > 13.95:
                new_score = new_score * 0.1

            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2
            if row.carbohydrates > 54:
                new_score = new_score * 1.5

            if row.fibers < 1.65:
                new_score = new_score * 0.1
            if row.fibers >= 1.65 and row.fibers <= 4.95:
                new_score = new_score * 1.2
            if row.fibers > 4.95:
                new_score = new_score * 2

            return new_score

        def rescoreObesity(row):
            new_score = row.score

            if row.calories < 133.35:
                new_score = new_score * 3
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 1.2
            if row.calories > 400.05:
                new_score = new_score * 0.01

            if row.fat < 4.65:
                new_score = new_score * 3
            if row.fat >= 4.65 and row.fat <= 13.95:
                new_score = new_score * 1
            if row.fat > 13.95:
                new_score = new_score * 0.01

            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1
            if row.carbohydrates > 54:
                new_score = new_score * 2.5

            if row.fibers < 1.65:
                new_score = new_score * 0.01
            if row.fibers >= 1.65 and row.fibers <= 4.95:
                new_score = new_score * 1
            if row.fibers > 4.95:
                new_score = new_score * 3

            return new_score

        def rescoreObesityPlus(row):
            new_score = row.score

            if row.calories < 133.35:
                new_score = new_score * 4
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 0.9
            if row.calories > 400.05:
                new_score = new_score * 0.001

            if row.fat < 4.65:
                new_score = new_score * 4
            if row.fat >= 4.65 and row.fat <= 13.95:
                new_score = new_score * 0.9
            if row.fat > 13.95:
                new_score = new_score * 0.001

            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 0.9
            if row.carbohydrates > 54:
                new_score = new_score * 3.5

            if row.fibers < 1.65:
                new_score = new_score * 0.001
            if row.fibers >= 1.65 and row.fibers <= 4.95:
                new_score = new_score * 0.9
            if row.fibers > 4.95:
                new_score = new_score * 4

            return new_score

        def rescoreUnderweight(row):
            new_score = row.score

            if row.calories < 133.35:
                new_score = new_score * 0.1
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 1.2
            if row.calories > 400.05:
                new_score = new_score * 2

            if row.carbohydrates < 18:
                new_score = new_score * 0.1
            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2
            if row.carbohydrates > 54:
                new_score = new_score * 2

            if row.proteins < 3.35:
                new_score = new_score * 0.1
            if row.proteins >= 3.35 and row.proteins <= 10.05:
                new_score = new_score * 1.2
            if row.proteins > 10.05:
                new_score = new_score * 2

            return new_score

        def rescoreActivityMedium(row):
            new_score = row.score

            if row.calories > 400.05:
                new_score = new_score * 1.5
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 1.2
            if row.calories < 133.35:
                new_score = new_score * 0.1

            if row.proteins > 10.05:
                new_score = new_score * 1.5
            if row.proteins >= 3.35 and row.proteins <= 10.05:
                new_score = new_score * 1.2
            if row.proteins < 3.35:
                new_score = new_score * 0.1

            if row.carbohydrates > 54:
                new_score = new_score * 1.5
            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2
            if row.carbohydrates < 18:
                new_score = new_score * 0.1

            return new_score

        def rescoreActivityHigh(row):
            new_score = row.score

            if row.calories > 400.05:
                new_score = new_score * 2
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 1.2
            if row.calories < 133.35:
                new_score = new_score * 0.1

            if row.proteins > 10.05:
                new_score = new_score * 2
            if row.proteins >= 3.35 and row.proteins <= 10.05:
                new_score = new_score * 1.2
            if row.proteins < 3.35:
                new_score = new_score * 0.1

            if row.carbohydrates > 54:
                new_score = new_score * 2
            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2
            if row.carbohydrates < 18:
                new_score = new_score * 0.1

            return new_score

        cibiAntistress = ['latte intero', 'riso', 'pollo', 'cereali integrali', 'manzo', 'fagioli', 'noci',
                          'cioccolato', 'formaggio', 'broccoli']

        def isAntistress(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            antistress = 0
            for elem in cibiAntistress:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    antistress += 1
            antiS = antistress / len(cibiAntistress)
            return (antiS)

        def rescoreStress(row):
            new_score = row.score

            if row.sodium < sodiumAvg - sodiumStd:
                new_score = new_score * 2
            if row.sodium >= sodiumAvg - sodiumStd and row.sodium <= sodiumAvg + sodiumStd:
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

            if row.saturatedFat < 1.35:
                new_score = new_score * 2
            if row.saturatedFat >= 1.35 and row.saturatedFat <= 4.05:
                new_score = new_score * 1.2
            if row.saturatedFat > 4.05:
                new_score = new_score * 0.1

            if row.carbohydrates > 54:
                new_score = new_score * 2
            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2
            if row.carbohydrates < 18:
                new_score = new_score * 0.1

            if row.fibers >= 1.65 and row.fibers <= 4.95:
                new_score = new_score * 1.5
            if row.fibers > 4.95:
                new_score = new_score * 2

            return new_score

        def rescoreMoodBad(row):
            if row.sugars < 6:
                return row.score * 0.1
            if row.sugars >= 6 and row.sugars <= 18:
                return row.score * 1.2
            if row.sugars > 18:
                return row.score * 2

        def rescoreCoffe(row):
            listIngredients = row.ingredients.strip("[ ]").split(", ")

            if 'caffè' in listIngredients:
                return row.score * 0.5
            if 'Caffè' in listIngredients:
                return row.score * 0.5
            else:
                return row.score

        richMagnesium = ['crusca', 'mandorle', 'anacardi', 'cereali integrali', 'piselli', 'fagioli', 'datteri',
                         'aneto', 'fichi', 'nocciole']

        def isRichMagnesium(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            magnesium = 0
            for elem in richMagnesium:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    magnesium += 1
            mg = magnesium / len(richMagnesium)
            return (mg)

        def rescoreMagnesium(row):
            if row.magnesium == 0.1:
                return row.score * 10
            if row.magnesium == 0.2:
                return row.score * 20
            if row.magnesium == 0.3:
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

            if row.calories < 133.35:
                new_score = new_score * 0.1
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 1.2
            if row.calories > 400.05:
                new_score = new_score * 2

            if row.carbohydrates > 54:
                new_score = new_score * 2
            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2
            if row.carbohydrates < 18:
                new_score = new_score * 0.1

            if row.proteins < 3.35:
                new_score = new_score * 0.1
            if row.proteins >= 3.35 and row.proteins <= 10.05:
                new_score = new_score * 1.2
            if row.proteins > 10.05:
                new_score = new_score * 2

            return new_score

        def rescoreGoalMinus(row):
            new_score = row.score

            if row.calories < 133.35:
                new_score = new_score * 2
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 1.2
            if row.calories > 400.05:
                new_score = new_score * 0.1

            if row.carbohydrates > 54:
                new_score = new_score * 1.4
            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2

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

            if row.carbohydrates > 54:
                new_score = new_score * 2
            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2
            if row.carbohydrates < 18:
                new_score = new_score * 0.1

            if row.saturatedFat < 1.35:
                new_score = new_score * 2
            if row.saturatedFat >= 1.35 and row.saturatedFat <= 4.05:
                new_score = new_score * 1.2
            if row.saturatedFat > 4.05:
                new_score = new_score * 0.1

            if row.fibers < 1.65:
                new_score = new_score * 0.1
            if row.fibers >= 1.65 and row.fibers <= 4.95:
                new_score = new_score * 1.2
            if row.fibers > 4.95:
                new_score = new_score * 2

            return new_score

        def rescoreU30(row):
            new_score = row.score

            if row.carbohydrates > 54:
                new_score = new_score * 2
            if row.carbohydrates >= 18 and row.carbohydrates <= 54:
                new_score = new_score * 1.2
            if row.carbohydrates < 18:
                new_score = new_score * 0.1

            if row.proteins < 3.35:
                new_score = new_score * 0.1
            if row.proteins >= 3.35 and row.proteins <= 10.05:
                new_score = new_score * 1.2
            if row.proteins > 10.05:
                new_score = new_score * 2

            if row.fibers < 1.65:
                new_score = new_score * 0.1
            if row.fibers >= 1.65 and row.fibers <= 4.95:
                new_score = new_score * 1.2
            if row.fibers > 4.95:
                new_score = new_score * 2

            return new_score

        def rescoreU40(row):
            new_score = row.score

            if row.proteins < 3.35:
                new_score = new_score * 0.1
            if row.proteins >= 3.35 and row.proteins <= 10.05:
                new_score = new_score * 1.2
            if row.proteins > 10.05:
                new_score = new_score * 2

            if row.fat < 4.65:
                new_score = new_score * 2
            if row.fat >= 4.65 and row.fat <= 13.95:
                new_score = new_score * 1.2
            if row.fat > 13.95:
                new_score = new_score * 0.1

            return new_score

        def rescoreU60(row):
            new_score = row.score

            if row.fibers < 1.65:
                new_score = new_score * 0.1
            if row.fibers >= 1.65 and row.fibers <= 4.95:
                new_score = new_score * 1.2
            if row.fibers > 4.95:
                new_score = new_score * 2

            if row.fat < 4.65:
                new_score = new_score * 2
            if row.fat >= 4.65 and row.fat <= 13.95:
                new_score = new_score * 1.2
            if row.fat > 13.95:
                new_score = new_score * 0.1

            return new_score

        def rescoreO60(row):
            new_score = row.score

            if row.proteins < 3.35:
                new_score = new_score * 0.1
            if row.proteins >= 3.35 and row.proteins <= 10.05:
                new_score = new_score * 1.2
            if row.proteins > 10.05:
                new_score = new_score * 2

            if row.calories < 133.35:
                new_score = new_score * 0.1
            if row.calories >= 133.35 and row.calories <= 400.05:
                new_score = new_score * 1.2
            if row.calories > 400.05:
                new_score = new_score * 2

            return new_score

        def score(row):
            score = row.ratingValue * np.log10(row.ratingCount)
            return score

        df['score'] = df.apply(score, axis=1)

        # calcolo medie prima di 'tagliare' il DataFrame
        #sugarAvg = df.sugars.mean()
        #sugarStd = df.sugars.std()

        #proteinsAvg = df.proteins.mean()
        #proteinsStd = df.proteins.std()

        #caloriesAvg = df.calories.mean()
        #caloriesStd = df.calories.std()

        #fatAvg = df.fat.mean()
        #fatStd = df.fat.std()

        #sFatAvg = df.saturatedFat.mean()
        #sFatStd = df.saturatedFat.std()

        sodiumAvg = df.sodium.mean()
        sodiumStd = df.sodium.std()

        #carbsAvg = df.carbohydrates.mean()
        #carbsStd = df.carbohydrates.std()

        #fiberAvg = df.fibers.mean()
        #fiberStd = df.fibers.std()

        # accorgimenti parametri
        n = int(request.args.get('n')) if (request.args.get('n') != None) else -1

        recipeName = request.args.get('recipeName')
        ingredient = request.args.get('ingredient')
        category = request.args.get('category')
        cost = request.args.get('cost')

        isLowNickel = int(request.args.get('isLowNickel')) if (request.args.get('isLowNickel') != None) else ''
        isVegetarian = int(request.args.get('isVegetarian')) if (request.args.get('isVegetarian') != None) else ''
        isLactoseFree = int(request.args.get('isLactoseFree')) if (request.args.get('isLactoseFree') != None) else ''
        isGlutenFree = int(request.args.get('isGlutenFree')) if (request.args.get('isGlutenFree') != None) else ''
        isLight = int(request.args.get('isLight')) if (request.args.get('isLight') != None) else ''
        user_difficulty = int(request.args.get('difficulty')) if (request.args.get('difficulty') != None) else ''

        goal = int(request.args.get('goal')) if (request.args.get('goal') != None) else ''
        user_cost = int(request.args.get('user_cost')) if (request.args.get('user_cost') != None) else ''
        user_time = int(request.args.get('user_time')) if (request.args.get('user_time') != None) else ''
        # age = int(request.args.get('age')) if (request.args.get('age') != None) else ''
        age = request.args.get('age')

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

        #height = request.args.get('height')
        #weight = request.args.get('weight')
        #bmi = weight / (height * height)

        bmi = float(request.args.get('fatclass')) if (request.args.get('fatclass') != None) else ''

        healthy = request.args.get('healthy')

        # filtro il DF sulle ricette salutari
        # https://acmrecsys.github.io/rsss2019/Food-Recommender-ctrattner.pdf
        if healthy == 'high':
            # print("healthy: ", healthy)
            df = df[(df.sugars <= 5) & (df.fat <= 3) & (df.saturatedFat <= 1.5)]

        if healthy == 'medium':
            # print("healthy: ", healthy)
            df = df[(df.sugars >= 5) & (df.sugars <= 15) &
                    (df.fat >= 3) & (df.fat <= 20) &
                    (df.saturatedFat >= 1.5) & (df.saturatedFat <= 5)
                    ]

        if healthy == 'low':
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
        # ['Dolci', 'Primi piatti', 'Lievitati', 'Salse e Sughi', 'Piatti Unici', 'Contorni', 'Antipasti', 'Secondi piatti', 'Torte salate', 'Bevande', 'Insalate', 'Marmellate e Conserve']

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
        elif bmi >= 25 and bmi < 30:
            bmiWeight = 'over'
            df.score = df.apply(rescoreOverweight, axis=1)
        elif bmi >= 30 and bmi < 35:
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

        if activity == 'high':
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
            # print("sodiumAvg: " + str(sodiumAvg))

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
            if (bmiWeight != 'over' and goal == 1):
                # if((not(overweight)) and goal == 1):
                df.score = df.apply(rescoreGoalPlus, axis=1)
            # se vuole perdere peso e non è sottopeso
            if (bmiWeight != 'under' and goal == -1):
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

        # print ('age: ', age)
        if age == 'U20':
            df.score = df.apply(rescoreU20, axis=1)
        elif age == 'U30':
            df.score = df.apply(rescoreU30, axis=1)
        elif age == 'U40':
            df.score = df.apply(rescoreU40, axis=1)
        elif age == 'U60':
            df.score = df.apply(rescoreU60, axis=1)
        elif age == 'O60':
            df.score = df.apply(rescoreO60, axis=1)

        df = df.sort_values('score', ascending=False)

        # print(len(df))

        return df.head(n).sample(frac=1).to_json(orient='split')

api.add_resource(Mood, '/mood/')


if __name__ == '__main__':
    app.run(port=5009)