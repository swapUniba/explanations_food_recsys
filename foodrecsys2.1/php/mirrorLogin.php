<?php

    $dish = $_COOKIE['myrrorDish'];
    $myrrorData = unserialize(base64_decode($_POST["myrrorData"]));


    $sex = $_POST['sexOption'];

    $answers = $sex . ":q,";

    $occupation = $_POST['occupation'];
    $websiteUsage = $_POST['websiteUsage'];
    $cookingFreq = $_POST['cookingFreq'];
    $user_difficulty = $_POST['difficulty'];
    $goal = $_POST['goal'];

    if(isset($_POST['age'])){
        $age = $_POST['age'];
        $answers = $answers . $age . ":q,";
    }
    else{
        $age = $myrrorData['age'];
        $answers = $answers . $age . ":m,";
    }

    if(isset($_POST['BMI'])){
        $fatclass = $_POST['BMI'];

        $answers = $answers . $fatclass . ":q,";

        $underweight = false;
        $overweight = false;

        if($fatclass < 19)
            $underweight = true;

        if($fatclass >= 25)
            $overweight = true;
    }
    else{

        $underweight = $myrrorData['underweight'];
        $overweight = $myrrorData['overweight'];

        if($underweight)
            $fatclass = 'underweight';

        if($overweight)
            $fatclass = 'overweight';


        $answers = $answers . $fatclass . ":m,";
    }

    $answers = $answers . $occupation . ":q," . $websiteUsage . ":q," . $cookingFreq . ":q," . $user_difficulty . ":q," . $goal . ":q,";

    if(isset($_POST['mood'])){
        $mood = $_POST['mood'];

        $answers = $answers . $mood . ":q,";
    }
    else{
        $mood = $myrrorData['mood'];

        $answers = $answers . $mood . ":m,";
    }

    if(isset($_POST['activity'])){
        $activity = $_POST['activity'];

        $answers = $answers . $activity . ":q,";
    }
    else{
        $activity = $myrrorData['activity'];

        $answers = $answers . $activity . ":m,";
    }

    if(isset($_POST['sleepOption'])){
        $sleep = $_POST['sleepOption'];

        $answers = $answers . $sleep . ":q,";
    }
    else{
        $sleep = $myrrorData['sleep'];

        $answers = $answers . $sleep . ":m,";
    }

    if(isset($_POST['stressOption'])){
        $stress = $_POST['stressOption'];

        $answers = $answers . $stress . ":q,";
    }
    else{
        $stress = $myrrorData['stress'];

        $answers = $answers . $stress . ":m,";
    }

    if(isset($_POST['depressionOption'])){
        $depression = $_POST['depressionOption'];

        $answers = $answers . $depression . ":q,";
    }
    else{
        $depression = $myrrorData['depression'];

        $answers = $answers . $depression . ":m,";
    }

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
	
	//here is created the recommendation
    $url_old = createURL_old($mood, $stress, $depression, $fatclass, $activity, $sleep, $vegetarian, $lactose, $gluten, $nickel, $light, $user_difficulty);
    $url_new = createURL($mood, $stress, $depression, $fatclass, $activity, $sleep, $vegetarian, $lactose, $gluten, $nickel, $light, $user_difficulty,
            $user_time, $user_cost, $age, $goal);

    $data = getRecipes($url_new, $url_old);

    /*
    se il valore di $rec_1 o $rec_2 è 0 allora è stato utilizzato il sistema di raccomandazione popolare
    se il valore di $rec_1 o $rec_2 è 1 allora è stato utilizzato il sistema di raccomandazione precedente (run on 5002)
    se il valore di $rec_1 o $rec_2 è 2 allora è stato utilizzato il sistema di raccomandazione attuale (run on 5009)
    */
    $rec_1 = $data['rec_1'];
    $rec_2 = $data['rec_2'];
	
	$explanations = [];
		
	$imgurlA = $data['personalized_main_1']['imgURL1'];
	$imgurlB = $data['personalized_main_2']['imgURL2'];
	
	//For each dish is created an explanation, image url is used as reference in the dataset
	//Explanation for main course
    $explanations = [];

    $imgurlA = $data['personalized_main_1']['imgURL'];
    $imgurlB = $data['personalized_main_2']['imgURL'];

    $explanations["main_exp"] = getExplanation(createUrlExp(
            $mood, $stress, $depression,
            $fatclass, $health_style, $health_condition, $activity, $sleep,
            $vegetarian, $lactose, $gluten, $nickel, $light,
            $user_time, $user_cost, $age, $goal,
            $user_difficulty, $imgurlA, $imgurlB)
    );

    $imgurlA = $data['personalized_second_1']['imgURL'];
    $imgurlB = $data['personalized_second_2']['imgURL'];

    $explanations["second_exp"] = getExplanation(createUrlExp(
            $mood, $stress, $depression,
            $fatclass, $health_style, $health_condition, $activity, $sleep,
            $vegetarian, $lactose, $gluten, $nickel, $light,
            $user_time, $user_cost, $age, $goal,
            $user_difficulty, $imgurlA, $imgurlB)
    );

    $imgurlA = $data['personalized_dessert_1']['imgURL'];
    $imgurlB = $data['personalized_dessert_2']['imgURL'];

    $explanations["dessert_exp"] = getExplanation(createUrlExp(
            $mood, $stress, $depression,
            $fatclass, $health_style, $health_condition, $activity, $sleep,
            $vegetarian, $lactose, $gluten, $nickel, $light,
            $user_time, $user_cost, $age, $goal,
            $user_difficulty, $imgurlA, $imgurlB)
    );
	
	$answers = $answers . $data['personalized_main_1']['url'] . ','
		. $data['personalized_main_2']['url'] . ','
		. $data['personalized_second_1']['url'] . ','
		. $data['personalized_second_2']['url']
		. ',' . $data['personalized_dessert_1']['url']
		. ',' . $data['personalized_dessert_2']['url'] . ',';
	
	$_SESSION['data'] = $data;
	$_SESSION['explanations'] = $explanations;
	$_SESSION['profile'] = $answers;
?>