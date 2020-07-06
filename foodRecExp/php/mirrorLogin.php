<?php
	
	$dish = $_COOKIE['myrrorDish'];
	$myrrorData = unserialize(base64_decode($_POST["myrrorData"]));     
	
	$sex = $_POST['sexOption'];
	$occupation = $_POST['occupation'];
	$websiteUsage = $_POST['websiteUsage'];
	$cookingFreq = $_POST['cookingFreq'];
	$exp = $_POST['exp'];
	$goal = $_POST['goal'];
	
	$HS = $_POST['HS'];
	$HC = $_POST['HC'];
	$HFC = $_POST['HFC'];
	$HNV = $_POST['HNV'];
	
	$answers = $sex . ":q,";
	
	if(isset($_POST['age'])){
		$age = $_POST['age'];
		$answers = $answers . $age . ":q,";
	}
	else{
		$age = $myrrorData['age'];
		$answers = $answers . $age . ":m,";
	}
	
	$answers = $answers . $HS . ":q," . $HC . ":q," . $HFC . ":q," . $HNV . ":q,"
	
	if(isset($_POST['BMI'])){
		$fatclass = $_POST['BMI'];
		$answers = $answers . $fatclass . ":q,";
		
		$underweight = false;
		$overweight = false;
		
		if($fatclass == 'Underweight (BMI < 19.0)')
			$underweight = true;
		else if($fatclass == 'Overweight (BMI 23.0–24.9)' || $fatclass == 'Class I obesity (BMI 25.0–29.9)' || $fatclass == 'Class II obesity (BMI ≥30.0)' )
			$overweight = true;
	}
	else{
		$underweight = $myrrorData['underweight'];
		$overweight = $myrrorData['overweight'];
		
		if($underweight)
		   $fatclass = 'underweight';
		else if($overweight)
		   $fatclass = 'overweight';
		
		$answers = $answers . $fatclass . ":m,";
	}
	
	$answers = $answers . $occupation . ":q," . $websiteUsage . ":q," . $cookingFreq . ":q," . $exp . ":q," . $goal . ":q,"; 
	
	if(isset($_POST['mood'])){
		$mood = $_POST['mood'];
		$answers = $answers . $mood . ":q,";
	} else {
		$mood = $myrrorData['mood'];
		$answers = $answers . $mood . ":m,";
	}
	
	if(isset($_POST['activity'])){
		$activity = $_POST['activity'];
		$answers = $answers . $activity . ":q,";
	} else {
		$activity = $myrrorData['activity'];
		$answers = $answers . $activity . ":m,";
	}
	
	if(isset($_POST['sleepOption'])){
		$sleep = $_POST['sleepOption'];
		$answers = $answers . $sleep . ":q,";
	} else {
		$sleep = $myrrorData['sleep'];
		$answers = $answers . $sleep . ":m,";
	}
	
	if(isset($_POST['stressOption'])){
		$stress = $_POST['stressOption']; 
		$answers = $answers . $stress . ":q,";
	} else {
		$stress = $myrrorData['stress'];
		$answers = $answers . $stress . ":m,";
	}   
	
	if(isset($_POST['depressionOption'])){
		$depression = $_POST['depressionOption'];
		$answers = $answers . $depression . ":q,";
	} else{
		$depression = $myrrorData['depression'];
		$answers = $answers . $depression . ":m,";
	}
	
	
	
	//shorthand if: VAR = IF_COND ? true : false;
	$joint 			= (isset($_POST['joint'])) 			? $_POST['joint'] 			: false;
	$cholesterol 	= (isset($_POST['cholesterol'])) 	? $_POST['cholesterol'] 	: false;
	$heart 			= (isset($_POST['heart'])) 			? $_POST['heart'] 			: false;
	$pressure 		= (isset($_POST['pressure'])) 		? $_POST['pressure'] 		: false;
	$diabete 		= (isset($_POST['diabete'])) 		? $_POST['diabete'] 		: false;
	
	$answers = $answers . ($joint 		? '-joint-' 		: '');
	$answers = $answers . ($cholesterol ? '-cholesterol-' 	: '');
	$answers = $answers . ($heart 		? '-heart-' 		: '');
	$answers = $answers . ($pressure 	? '-pressure-' 		: '');
	$answers = $answers . ($diabete 	? '-diabete-' 		: '');
	
	$answers = $answers . ',';
	
	

	if(isset($_POST['vegetarian'])){
		$vegetarian = $_POST['vegetarian']; 
		$answers = $answers . "-vegetarian-";
	} else {
		$vegetarian = false;
	}

	if(isset($_POST['lactose'])){
		$lactose = $_POST['lactose'];
		$answers = $answers . "-lactosefree-";
	} else {
		$lactose = false;
	}

	if(isset($_POST['gluten'])){
		$gluten = $_POST['gluten'];
		$answers = $answers . "-glutenfree-";
	} else {
		$gluten = false;
	}

	if(isset($_POST['nickel'])){
		$nickel = $_POST['nickel'];
		$answers = $answers . "-lownickel-";
	} else {
		$nickel = false;
	}

	if(isset($_POST['light'])){
		$light = $_POST['light']; 
		$answers = $answers . "-light-";
	} else {
		$light = false;
	}
	
	$answers = $answers . ',';
	
	//here is created the recommendation
	$data = getRecipes(createURL($mood, $stress, $depression, $underweight, $overweight, $activity, $sleep, $vegetarian, $lactose, $gluten, $nickel, $light, $exp));  
	
	$explanations = [];
		
	$imgurlA = $data['personalized_main']['imgURL'];
	$imgurlB = $data['not_personalized_main']['imgURL'];
	
	//For each dish is created an explanation, image url is used as reference in the dataset
	//Explanation for main course
	$explanations["main_exp"] = getExplanation(createUrlExp(
		$mood, $stress, $depression,
		$underweight, $overweight, $activity, $goal, $sleep,
		$vegetarian, $lactose, $gluten, $nickel, $light,
		$joint, $cholesterol, $heart, $pressure, $diabete,
		$exp, $imgurlA, $imgurlB)
	);
	
	$imgurlA = $data['personalized_second']['imgURL'];
	$imgurlB = $data['not_personalized_second']['imgURL'];
	
	
	//Explanation for second course
	$explanations["second_exp"] = getExplanation(createUrlExp(
		$mood, $stress, $depression,
		$underweight, $overweight, $activity, $goal, $sleep,
		$vegetarian, $lactose, $gluten, $nickel, $light,
		$joint, $cholesterol, $heart, $pressure, $diabete,
		$exp, $imgurlA, $imgurlB)
	);
	
	$imgurlA = $data['personalized_dessert']['imgURL'];
	$imgurlB = $data['not_personalized_dessert']['imgURL'];
		
	//Explanation for dessert
	$explanations["dessert_exp"] = getExplanation(createUrlExp(
		$mood, $stress, $depression,
		$underweight, $overweight, $activity, $goal, $sleep,
		$vegetarian, $lactose, $gluten, $nickel, $light,
		$joint, $cholesterol, $heart, $pressure, $diabete,
		$exp, $imgurlA, $imgurlB)
	);
	
	$answers = $answers . $data['personalized_main']['url'] . ','
		. $data['not_personalized_main']['url'] . ','
		. $data['personalized_second']['url'] . ',' 
		. $data['not_personalized_second']['url'] 
		. ',' . $data['personalized_dessert']['url'] 
		. ',' . $data['not_personalized_dessert']['url'] . ',';
	
	$_SESSION['data'] = $data;
	$_SESSION['explanations'] = $explanations;
	$_SESSION['profile'] = $answers;
?>