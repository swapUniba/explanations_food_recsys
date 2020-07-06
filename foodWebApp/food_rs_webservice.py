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
            df = pd.read_csv(url_dataset_en, encoding = "utf8")

        else:
            df = pd.read_csv(url_dataset_it, encoding = "utf8")

        #print('dataset language: ', lang)

        # dfFromIngredient
        def dfFromIngredient(df, searchIngrendient):
            new_rows = []
            returnDf = pd.DataFrame()

            for index, row in df.iterrows():
                listIngredients = row.ingredients.strip("[ ]").split(", ")

                if any(not(ingredient.lower().find(searchIngrendient)) for ingredient in listIngredients):
                    new_rows.append(row)
                    
            return returnDf.append(pd.DataFrame(new_rows, columns=df.columns))

        def rescoreOverweight(row):
            if row.calories < caloriesAvg - caloriesStd:
                return row.score * 2
            if row.calories >= caloriesAvg - caloriesStd and row.calories <= caloriesAvg + caloriesStd:
                return row.score * 1.2
            if row.calories > caloriesAvg + caloriesStd:
                return row.score * 0.01
                
        def rescoreUnderweight(row):
            if row.calories < caloriesAvg - caloriesStd:
                return row.score * 0.1
            if row.calories >= caloriesAvg - caloriesStd and row.calories <= caloriesAvg + caloriesStd:
                return row.score * 1.2
            if row.calories > caloriesAvg + caloriesStd:
                return row.score * 2

        def rescoreActivityLow(row):
            if row.calories < caloriesAvg - caloriesStd:
                return row.score * 4
            if row.calories >= caloriesAvg - caloriesStd and row.calories <= caloriesAvg + caloriesStd:
                return row.score * 1
            if row.calories > caloriesAvg + caloriesStd:
                return row.score * 0.01

        def rescoreActivityHighCalories(row):
            if row.calories > caloriesAvg + caloriesStd:
                return row.score * 4
            if row.calories >= caloriesAvg - caloriesStd and row.calories <= caloriesAvg + caloriesStd:
                return row.score * 1
            if row.calories < caloriesAvg - caloriesStd:
                return row.score * 0.01

        def rescoreActivityHighProteins(row):
            if row.proteins > proteinsAvg + proteinsStd:
                return row.score * 4
            if row.proteins >= proteinsAvg - proteinsStd and row.proteins <= proteinsAvg + proteinsStd:
                return row.score * 1
            if row.proteins < proteinsAvg - proteinsStd:
                return row.score * 0.01
            
        def rescoreStress(row):
            if row.sodium < sodiumAvg - sodiumStd:
                return row.score * 0.01
            if row.sodium >= sodiumAvg - sodiumStd and row.sodium <= sodiumAvg + sodiumStd:
                return row.score * 1.2
            if row.sodium > sodiumAvg + sodiumStd:
                return row.score * 2

        def rescoreDepression(row):
            if row.fat < fatAvg - fatStd:
                return row.score * 2
            if row.fat >= fatAvg - fatStd and row.fat <= fatAvg + fatStd:
                return row.score * 1.2
            if row.fat > fatAvg + fatStd:
                return row.score * 0.1

        def rescoreMoodBad(row):
            if row.sugars < sugarAvg - sugarStd:
                return row.score * 0.1
            if row.sugars >= sugarAvg - sugarStd and row.sugars <= sugarAvg + sugarStd:
                return row.score * 1.2
            if row.sugars > sugarAvg + sugarStd:
                return row.score * 2
                
        def rescoreCoffe(row):    
            listIngredients = row.ingredients.strip("[ ]").split(", ")

            if 'caffè' in listIngredients:
                return row.score * 0.5
            if  'Caffè' in listIngredients:
                return row.score * 0.5
            else:
                return row.score

        richMagnesium = ['crusca', 'mandorle', 'anacardi', 'cereali integrali', 'piselli', 'fagioli', 'datteri', 'aneto', 'fichi', 'nocciole']

        def isRichMagnesium(ingredients):
            listIngredients = ingredients.strip("[ ]").split(", ")

            magnesium = 0
            for elem in richMagnesium:
                if any(elem in ingredient.lower() for ingredient in listIngredients):
                    magnesium += 1
            mg = magnesium / len(richMagnesium)
            return (mg)

        def rescoreSleep(row):
            if row.magnesium == 0.1:
                return row.score * 10
            if row.magnesium == 0.2:
                return row.score * 20
            if row.magnesium == 0.3:
                return row.score * 30
            else:
                return row.score
                
        def rescoreDifficulty(row, difficulty):
            if difficulty == 1:
                if row.difficulty == 'Molto facile':
                    return row.score * 2
            
            if difficulty == 2:
                if row.difficulty == 'Facile':
                    return row.score * 2
                
            if difficulty == 3:
                if row.difficulty == 'Media':
                    return row.score * 2
                
            if difficulty == 4:
                if row.difficulty == 'Difficile':
                    return row.score * 2
                
            if difficulty == 5:
                if row.difficulty == 'Molto difficile':
                    return row.score * 2

        def score(row):
            score = row.ratingValue * np.log10(row.ratingCount)
            return score

        df['score'] = df.apply(score, axis=1)

        # calcolo medie prima di 'tagliare' il DataFrame
        sugarAvg = df.sugars.mean()
        sugarStd = df.sugars.std()

        proteinsAvg = df.proteins.mean()
        proteinsStd = df.proteins.std()

        caloriesAvg = df.calories.mean()
        caloriesStd = df.calories.std()

        fatAvg = df.fat.mean()
        fatStd = df.fat.std()

        sodiumAvg = df.sodium.mean()
        sodiumStd = df.sodium.std()

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

        # orario
        hour = request.args.get('hour')

        # mood
        mood = request.args.get('mood')
        activity = request.args.get('activity')
        stress = request.args.get('stress')
        sleep = request.args.get('sleep')
        depression = request.args.get('depression')

        overweight = request.args.get('overweight')
        underweight = request.args.get('underweight')
        
        healthy = request.args.get('healthy')

        # filtro il DF sulle ricette salutari
        # https://acmrecsys.github.io/rsss2019/Food-Recommender-ctrattner.pdf
        if healthy == 'high':
            #print("healthy: ", healthy)
            df = df[(df.sugars <= 5) & (df.fat <= 3) & (df.saturatedFat <= 1.5)]

        if healthy == 'medium':
            #print("healthy: ", healthy)
            df = df[(df.sugars >= 5) & (df.sugars <= 15) &
                    (df.fat >= 3) & (df.fat <= 20) & 
                    (df.saturatedFat >= 1.5) & (df.saturatedFat <= 5)
                    ]

        if healthy == 'low':
            #print("healthy: ", healthy)
            df = df[(df.sugars >= 15) & (df.fat >= 20) & (df.saturatedFat > 5) & (df.sodium >= 1.5)]

        # filtro il DataFrame su nome della ricetta cercata
        if recipeName:
            #print("recipeName: " + recipeName)
            df = df[df.title.str.contains(recipeName, case=False)]

        # filtro il DataFrame su ingrediente della ricetta cercato

        if ingredient:
            #print("ingredient: " + ingredient)
            df = dfFromIngredient(df, ingredient)

        # categories = df.category.unique()
        # ['Dolci', 'Primi piatti', 'Lievitati', 'Salse e Sughi', 'Piatti Unici', 'Contorni', 'Antipasti', 'Secondi piatti', 'Torte salate', 'Bevande', 'Insalate', 'Marmellate e Conserve']

        if category:
            #print('category: ' + category)
            df = df[df.category == category]

        # cost = df.cost.unique()
        # ['Molto basso', 'Medio', 'Basso', 'None', 'Elevato', 'Molto elevata']

        if cost:
            #print("cost: " + cost)
            df = df[df.cost == cost]

        if isLowNickel:
            #print("isLowNickel: " + str(isLowNickel))
            df = df[df.isLowNickel == isLowNickel]

        if isVegetarian:
            #print("isVegetarian: " + str(isVegetarian))
            df = df[df.isVegetarian == isVegetarian]

        if isLactoseFree:
            #print("isLactoseFree: " + str(isLactoseFree))
            df = df[df.isLactoseFree == isLactoseFree]

        if isGlutenFree:
            #print("isGlutenFree: " + str(isGlutenFree))
            df = df[df.isGlutenFree == isGlutenFree]

        if isLight:
            #print("isLight: " + str(isLight))
            df = df[df.isLight == isLight]

        if overweight:
            #print('overweight:', overweight)
            df.score = df.apply(rescoreOverweight, axis=1)
            df = df.sort_values('score', ascending=False)
            #print(df[['title', 'score']].head(10))
            
        if underweight:
            #print('underweight: ', underweight)
            df.score = df.apply(rescoreUnderweight, axis=1)
            df = df.sort_values('score', ascending=False)
            #print(df[['title', 'score']].head(10))

        if mood == 'bad':
            #print('mood: bad')
            #print("sugarAvg: " + str(sugarAvg))

            # df = df[df.sugar > sugarAvg]
            df.score = df.apply(rescoreMoodBad, axis=1)
            df = df.sort_values('score', ascending=False)
            #print(df[['title', 'score']].head(10))
            
        if activity == 'low':
            #print('activity: low')
            # print("caloriesAvg: " + str(caloriesAvg))

            # df = df[df.calories < caloriesAvg]
            df.score = df.apply(rescoreActivityLow, axis=1)
            df = df.sort_values('score', ascending=False)
            #print(df[['title', 'score']].head(10))
           
        if activity == 'high':
            #print('activity: high')
            #print("caloriesAvg: " + str(caloriesAvg))
            #print("proteinsAvg: " + str(proteinsAvg))

            # df = df[(df.calories > caloriesAvg) & (df.proteins > proteinsAvg)]
            df.score = df.apply(rescoreActivityHighCalories, axis=1)
            df.score = df.apply(rescoreActivityHighProteins, axis=1)
            df = df.sort_values('score', ascending=False)
            #print(df[['title', 'score']].head(10))

        # stress => cibo salato (https://www.nutritestesso.it/it/lo-stretto-legame-cibo-ed-emozioni/)
        if stress:
            #print('stress : ' + str(stress))
            # print("sodiumAvg: " + str(sodiumAvg))

            # df = df[df.sodium > sodiumAvg]
            df.score = df.apply(rescoreStress, axis=1)
            df = df.sort_values('score', ascending=False)
            #print(df[['title', 'score']].head(10))
            
        # poco sonno => mangia magnesio
        if sleep == 'low':
            #print("sleep: " + sleep)
            #df = df[df.magnesium > 0]
            df['magnesium'] = df.ingredients.apply(isRichMagnesium)
            df.score = df.apply(rescoreSleep, axis=1)

        # sera => ricalcolo il caffe
        if hour == 'evening':
            #print ("hour: " + hour)
            df.score = df.apply(rescoreCoffe, axis=1)
            
        # depressione => meno grassi
        if depression == 'yes':
            #print ("depression: " + depression)
            # print("fatAvg: " + str(fatAvg))

            # df = df[df.fat < fatAvg]
            df.score = df.apply(rescoreDepression, axis=1)
            df = df.sort_values('score', ascending=False)
            #print(df[['title', 'score']].head(10))
            
        if user_difficulty != '':
            #print ('user_difficulty: ', user_difficulty)
            df.score = df.apply(rescoreDifficulty, difficulty = user_difficulty, axis = 1)
            df = df.sort_values('score', ascending=False)
            #print(df[['title', 'score']].head(10))

        df = df.sort_values('score', ascending=False)

        #print(len(df))
        
        return df.head(n).sample(frac=1).to_json(orient='split')
        
api.add_resource(Mood, '/mood/')

if __name__ == '__main__':
     app.run(port=5002)
