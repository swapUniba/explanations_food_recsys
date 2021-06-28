<?php
	
	$dish = $_POST['dish'];

	$showExpl = $_SESSION['showExpl'];

    //typeExps AB
    $typeExpsTwo = array(
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

    //type exps single A
    $typeExpsOneA = array (
        "popularity_oneA",
        "foodGoals_oneA",
        "foodPreferences_oneA",
        "foodFeatures_oneA",
        "userSkills_oneA",
        "foodFeatureHealthRisk_oneA",
        "foodFeatureHealthBenefits_oneA",
        "userFeatureHealthRisk_oneA",
        "userFeatureHealthBenefits_oneA",
        "userTime_oneA",
        "userCosts_oneA",
        "userLifestyle_oneA",
        "userIngredients_oneA",
        "userAge_oneA",
        "descriptionA"
    );

    //type exps single B
    $typeExpsOneB = array (
        "popularity_oneB",
        "foodGoals_oneB",
        "foodPreferences_oneB",
        "foodFeatures_oneB",
        "userSkills_oneB",
        "foodFeatureHealthRisk_oneB",
        "foodFeatureHealthBenefits_oneB",
        "userFeatureHealthRisk_oneB",
        "userFeatureHealthBenefits_oneB",
        "userTime_oneB",
        "userCosts_oneB",
        "userLifestyle_oneB",
        "userIngredients_oneB",
        "userAge_oneB",
        "descriptionB"
    );

	// explanation index to get the same type of explanation for every dish
	// $type_explanation = rand(0, count($typeExpsTwo) - 1);

    // explanation indexes to get the different explanations for every dishes
    $expMainIndex = rand(0, count($typeExpsTwo) - 1);
    $expSecondIndex = rand(0, count($typeExpsTwo) - 1);
    $expDessertIndex = rand(0, count($typeExpsTwo) - 1);

    $mainTypeExpl = "";
    $mainTypeExplA = "";
    $mainTypeExplB= "";

    $secondTypeExpl= "";
    $secondTypeExplA= "";
    $secondTypeExplB= "";

    $dessertTypeExpl= "";
    $dessertTypeExplA= "";
    $dessertTypeExplB= "";


	if(($dish == "main") || ($dish == "main_exp") ){
        $sex = $_POST['sexOption'];
        $age = $_POST['age'];
        $height = $_POST['height'] / 100;
        $weight = $_POST['weight'];

        //$fatclass = ($weight * 1.3) / ($height ** 2.5);
        $fatclass = ($weight * 1.3) / (pow($height, 2.5));

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

        if(isset($_POST['diabetes'])){
            $diabetes = $_POST['diabetes'];
            $answers = $answers . "-diabetes-";
        }
        else{
            $diabetes = false;
        }

        if(isset($_POST['pregnant'])){
            $pregnant = $_POST['pregnant'];
            $answers = $answers . "-pregnant-";
        }
        else{
            $pregnant = false;
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

        $url_old = createURL_old($mood, $stress, $depression, $fatclass, $activity, $sleep, $vegetarian, $lactose,
            $gluten, $nickel, $light, $diabetes, $pregnant, $user_difficulty);
        $url_new = createURL($mood, $stress, $depression, $fatclass, $activity, $sleep, $vegetarian, $lactose,
            $gluten, $nickel, $light, $diabetes, $pregnant, $user_difficulty, $user_time, $user_cost, $age, $goal);
		
		//here is created the recommendation
        $data = getRecipes($url_new, $url_old);
		
		$explanations = [];
		
		$imgurlA = $data['personalized_main_1']['imgURL'];
		$imgurlB = $data['personalized_main_2']['imgURL'];
		
		$explanations["main_exp"] = getExplanation(createUrlExp(
                $mood, $stress, $depression,
                $fatclass, $health_style, $health_condition, $activity, $sleep,
                $vegetarian, $lactose, $gluten, $nickel, $light, $diabetes, $pregnant,
                $user_time, $user_cost, $age, $goal,
                $user_difficulty, $imgurlA, $imgurlB,
                $userFavIngredients, $expMainIndex)
		);

		switch ($showExpl){
            case 0: //no expl
                break;
            case 1: //single recipe explanations in one
                if (! array_key_exists($typeExpsOneA[$expMainIndex], $explanations["main_exp"])){
                    $explanations["main_exp"] += array($typeExpsOneA[$expMainIndex] => "");
                }
                if (! array_key_exists($typeExpsOneB[$expMainIndex], $explanations["main_exp"])){
                    $explanations["main_exp"] += array($typeExpsOneB[$expMainIndex] => "");
                }

                $mainTypeExplA = $typeExpsOneA[$expMainIndex];
                $mainTypeExplB = $typeExpsOneB[$expMainIndex];
                break;
            case 2: //double recipe explanations
                if (! array_key_exists($typeExpsTwo[$expMainIndex], $explanations["main_exp"])){
                    $explanations["main_exp"] += array($typeExpsTwo[$expMainIndex] => "");
                }
                $mainTypeExpl = $typeExpsTwo[$expMainIndex];
                break;
        }
		
		$imgurlA = $data['personalized_second_1']['imgURL'];
		$imgurlB = $data['personalized_second_2']['imgURL'];
		
		$explanations["second_exp"] = getExplanation(createUrlExp(
                $mood, $stress, $depression,
                $fatclass, $health_style, $health_condition, $activity, $sleep,
                $vegetarian, $lactose, $gluten, $nickel, $light, $diabetes, $pregnant,
                $user_time, $user_cost, $age, $goal,
                $user_difficulty, $imgurlA, $imgurlB,
                $userFavIngredients, $expSecondIndex)
		);
        switch ($showExpl){
            case 0: //no explanation
                break;
            case 1:
                if (! array_key_exists($typeExpsOneA[$expMainIndex], $explanations["second_exp"])){
                    $explanations["second_exp"] += array($typeExpsOneA[$expMainIndex] => "");
                }
                if (! array_key_exists($typeExpsOneB[$expMainIndex], $explanations["second_exp"])){
                    $explanations["second_exp"] += array($typeExpsOneB[$expMainIndex] => "");
                }
                $secondTypeExplB = $typeExpsOneB[$expSecondIndex];
                $secondTypeExplA = $typeExpsOneA[$expSecondIndex];
                break;
            case 2:
                if (! array_key_exists($typeExpsTwo[$expMainIndex], $explanations["second_exp"])){
                    $explanations["second_exp"] += array($typeExpsTwo[$expMainIndex] => "");
                }
                $secondTypeExpl = $typeExpsTwo[$expSecondIndex];
                break;
        }
		
		$imgurlA = $data['personalized_dessert_1']['imgURL'];
		$imgurlB = $data['personalized_dessert_2']['imgURL'];
			
		$explanations["dessert_exp"] = getExplanation(createUrlExp(
                $mood, $stress, $depression,
                $fatclass, $health_style, $health_condition, $activity, $sleep,
                $vegetarian, $lactose, $gluten, $nickel, $light, $diabetes, $pregnant,
                $user_time, $user_cost, $age, $goal,
                $user_difficulty, $imgurlA, $imgurlB,
                $userFavIngredients, $expDessertIndex)
		);
        switch ($showExpl){
            case 0: //single expl for recipe A
                break;
            case 1:
                if (! array_key_exists($typeExpsOneA[$expMainIndex], $explanations["dessert_exp"])){
                    $explanations["dessert_exp"] += array($typeExpsOneA[$expMainIndex] => "");
                }
                if (! array_key_exists($typeExpsOneB[$expMainIndex], $explanations["dessert_exp"])){
                    $explanations["dessert_exp"] += array($typeExpsOneB[$expMainIndex] => "");
                }
                $dessertTypeExplB = $typeExpsOneB[$expDessertIndex];
                $dessertTypeExplA = $typeExpsOneA[$expDessertIndex];
                break;
            case 2:
                if (! array_key_exists($typeExpsTwo[$expMainIndex], $explanations["dessert_exp"])){
                    $explanations["dessert_exp"] += array($typeExpsTwo[$expMainIndex] => "");
                }
                $dessertTypeExpl = $typeExpsTwo[$expDessertIndex];
                break;
        }

		$answers = $answers 
			. $data['personalized_main_1']['name']
			. ','. $data['personalized_main_2']['name']
			. ',' . $data['personalized_second_1']['name']
			. ',' . $data['personalized_second_2']['name']
			. ',' .$data['personalized_dessert_1']['name']
			. ',' . $data['personalized_dessert_2']['name'] . ',';

        if ($showExpl != 0)
        {
            //Salvo le tipologie di spiegazioni mostrate
            $answers = $answers . 'ShowExpl=' . $showExpl . ',';
            if ($showExpl == 1)
            {
                $answers = $answers . $mainTypeExplA . ',' . $secondTypeExplA . ',' . $dessertTypeExplA . ',';
            }
            if ($showExpl == 2)
            {
                $answers = $answers . $mainTypeExpl . ',' . $secondTypeExpl . ',' . $dessertTypeExpl . ',';
            }

        }
        else{
            $answers = $answers . 'ShowExpl=' . $showExpl . ',';
        }
			
		$_SESSION['data'] = $data;
		$_SESSION['explanations'] = $explanations;
		$_SESSION['profile'] = $answers;
		$showExpl = $_SESSION['showExpl'];

        $_SESSION['mainTypeExpl'] = $mainTypeExpl;
        $_SESSION['secondTypeExpl'] = $secondTypeExpl;
        $_SESSION['dessertTypeExpl'] = $dessertTypeExpl;

        $_SESSION['mainTypeExplA'] = $mainTypeExplA;
        $_SESSION['secondTypeExplA'] = $secondTypeExplA;
        $_SESSION['dessertTypeExplA'] = $dessertTypeExplA;

        $_SESSION['mainTypeExplB'] = $mainTypeExplB;
        $_SESSION['secondTypeExplB'] = $secondTypeExplB;
        $_SESSION['dessertTypeExplB'] = $dessertTypeExplB;
	} else {
		$data = $_SESSION['data'];
		$explanations = $_SESSION['explanations'];
        $mainTypeExpl = $_SESSION['mainTypeExpl'];
        $secondTypeExpl = $_SESSION['secondTypeExpl'];
        $dessertTypeExpl = $_SESSION['dessertTypeExpl'];

        $mainTypeExplA = $_SESSION['mainTypeExplA'];
        $secondTypeExplA = $_SESSION['secondTypeExplA'];
        $dessertTypeExplA = $_SESSION['dessertTypeExplA'];

        $mainTypeExplB = $_SESSION['mainTypeExplB'];
        $secondTypeExplB = $_SESSION['secondTypeExplB'];
        $dessertTypeExplB = $_SESSION['dessertTypeExplB'];
	}

	//If the last page is dessert with exp (or dessert if we don't have to show the expl) go to bye.php
	if(($dish == "dessert_exp") || ($dish == "dessert" and $showExpl==0)){
		$postPage = 'action="bye.php"';
	}

?>