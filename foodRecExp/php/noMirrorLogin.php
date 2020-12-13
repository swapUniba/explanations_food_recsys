<?php
	
	$dish = $_POST['dish'];

	//type of exps for experiment
    $typeExps = array(
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
     );

    //for the experiment I use a random exp, one of these random, different for every dish
    $expMainIndex = rand(0, count($typeExps) - 1);
    $expSecondIndex = rand(0, count($typeExps) - 1);
    $expDessertIndex = rand(0, count($typeExps) - 1);



	if($dish == "main"){
        $sex = $_POST['sexOption'];
        $age = $_POST['age'];
        $height = $_POST['height'];
        $weight = $_POST['weight'];
        $fatclass = ($weight * 10000) / ($height * $height);
        $health_style = $_POST['HS'];
        $health_condition = $_POST['HC'];
        $health_food_choise = $_POST['HFC'];
        $control_nutritional_value = $_POST['HNV'];
        $occupation = $_POST['occupation'];
        $websiteUsage = $_POST['websiteUsage'];
        $cookingFreq = $_POST['cookingFreq'];
        $user_difficulty = $_POST['difficulty'];
        $goal = $_POST['goal'];
        $mood = $_POST['mood'];
        $activity = $_POST['activity'];
        $sleep = $_POST['sleepOption'];
        $stress = $_POST['stressOption'];
        $depression = $_POST['depressionOption'];
        $user_time = $_POST['user_time'];
        $user_cost = $_POST['user_cost'];

        $answers = $sex . ":q," . $age . ":q," . $fatclass . ":q," . $health_style . ":q,"
            . $health_condition . ":q," . $health_food_choise . ":q," . $control_nutritional_value . ":q,"
            . $occupation . ":q," . $websiteUsage . ":q," . $cookingFreq . ":q,"
            . $user_difficulty . ":q," . $goal . ":q," . $mood . ":q,"
            . $activity . ":q," . $sleep . ":q," . $stress . ":q," . $depression . ":q,"
            . $user_cost . ":q," . $user_time . ":q," ;

        #recipe's ingredients
        $userFavIngredients = $_POST['user_ingredients'];
        $userFavIngredients = trim($userFavIngredients);
        $userFavIngredients = str_replace(",", "-", $userFavIngredients);
        $userFavIngredients = str_replace(";", "-", $userFavIngredients);
        $userFavIngredients = preg_replace('/[^A-Za-z0-9\-]/', '', $userFavIngredients); // Removes special chars
        preg_replace('/-+/', '-', $userFavIngredients); // Replaces multiple hyphens with single one
        $answers = $answers . $userFavIngredients . ":q," ;

        if(isset($_POST['vegetarian'])){
            $vegetarian = $_POST['vegetarian'];
            $answers = $answers . "-vegetarian-";
        }
        else{
            $vegetarian = false;
        }

        if(isset($_POST['lactose'])){
            $lactose = $_POST['lactose'];
            $answers = $answers . "-lactosefree-";
        }
        else{
            $lactose = false;
        }

        if(isset($_POST['gluten'])){
            $gluten = $_POST['gluten'];
            $answers = $answers . "-glutenfree-";
        }
        else{
            $gluten = false;
        }

        if(isset($_POST['nickel'])){
            $nickel = $_POST['nickel'];
            $answers = $answers . "-lownickel-";
        }
        else{
            $nickel = false;
        }

        if(isset($_POST['light'])){
            $light = $_POST['light'];
            $answers = $answers . "-light-";
        }
        else{
            $light = false;
        }


        $answers = $answers . ',';

        /*$underweight = false;
                $overweight = false;
                if($fatclass < 19)
                    $underweight = true;
                if($fatclass >= 25)
                    $overweight = true;
                 */




        $url_old = createURL_old($mood, $stress, $depression, $fatclass, $activity, $sleep, $vegetarian, $lactose,
            $gluten, $nickel, $light, $user_difficulty);
        $url_new = createURL($mood, $stress, $depression, $fatclass, $activity, $sleep, $vegetarian, $lactose,
            $gluten, $nickel, $light, $user_difficulty, $user_time, $user_cost, $age, $goal);


		
		
		//here is created the recommendation
        $data = getRecipes($url_new, $url_old);
		//$data = getRecipes(createURL($mood, $stress, $depression, $underweight, $overweight, $activity, $sleep, $vegetarian, $lactose, $gluten, $nickel, $light, $exp));
		
		$explanations = [];
		
		$imgurlA = $data['personalized_main_1']['imgURL'];
		$imgurlB = $data['personalized_main_2']['imgURL'];
		
		$explanations["main_exp"] = getExplanation(createUrlExp(
                $mood, $stress, $depression,
                $fatclass, $health_style, $health_condition, $activity, $sleep,
                $vegetarian, $lactose, $gluten, $nickel, $light,
                $user_time, $user_cost, $age, $goal,
                $user_difficulty, $imgurlA, $imgurlB,
                $userFavIngredients)
		);
		while (! array_key_exists($typeExps[$expMainIndex], $explanations["main_exp"]))
        {
            $expMainIndex = rand(0, count($typeExps) - 1);
        }
        $mainTypeExpl = $typeExps[$expMainIndex];
		
		$imgurlA = $data['personalized_second_1']['imgURL'];
		$imgurlB = $data['personalized_second_2']['imgURL'];
		
		$explanations["second_exp"] = getExplanation(createUrlExp(
                $mood, $stress, $depression,
                $fatclass, $health_style, $health_condition, $activity, $sleep,
                $vegetarian, $lactose, $gluten, $nickel, $light,
                $user_time, $user_cost, $age, $goal,
                $user_difficulty, $imgurlA, $imgurlB,
                $userFavIngredients)
		);
		while (! array_key_exists($typeExps[$expSecondIndex], $explanations["second_exp"] ))
        {
            $expSecondIndex = rand(0, count($typeExps) -1);
        }
        $secondTypeExpl = $typeExps[$expSecondIndex];
		
		$imgurlA = $data['personalized_dessert_1']['imgURL'];
		$imgurlB = $data['personalized_dessert_2']['imgURL'];
			
		$explanations["dessert_exp"] = getExplanation(createUrlExp(
                $mood, $stress, $depression,
                $fatclass, $health_style, $health_condition, $activity, $sleep,
                $vegetarian, $lactose, $gluten, $nickel, $light,
                $user_time, $user_cost, $age, $goal,
                $user_difficulty, $imgurlA, $imgurlB,
                $userFavIngredients)
		);
        while (! array_key_exists($typeExps[$expDessertIndex], $explanations["dessert_exp"] ))
        {
            $expDessertIndex = rand(0, count($typeExps) -1);
        }
        $dessertTypeExpl = $typeExps[$expDessertIndex];

		$answers = $answers 
			. $data['personalized_main_1']['name']
			. ','. $data['personalized_main_2']['name']
			. ',' . $data['personalized_second_1']['name']
			. ',' . $data['personalized_second_2']['name']
			. ',' .$data['personalized_dessert_1']['name']
			. ',' . $data['personalized_dessert_2']['name'] . ',';

		//Save in the answer (for log) the explanations used for every couple of recipes
        $answers = $answers . $mainTypeExpl . ',' . $secondTypeExpl . ',' . $dessertTypeExpl . ',';
			
		$_SESSION['data'] = $data;
		$_SESSION['explanations'] = $explanations;
		$_SESSION['profile'] = $answers;
        $_SESSION['mainTypeExpl'] = $mainTypeExpl;
        $_SESSION['secondTypeExpl'] = $secondTypeExpl;
        $_SESSION['dessertTypeExpl'] = $dessertTypeExpl;
	} else {		
		$data = $_SESSION['data'];
		$explanations = $_SESSION['explanations'];
        $mainTypeExpl = $_SESSION['mainTypeExpl'];
        $secondTypeExpl = $_SESSION['secondTypeExpl'];
        $dessertTypeExpl = $_SESSION['dessertTypeExpl'];
	}

	if($dish == "dessert_exp"){
		$postPage = 'action="bye.php"';
	}

?>