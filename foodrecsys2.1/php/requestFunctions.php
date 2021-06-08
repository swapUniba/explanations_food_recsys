<?php
include "myrror/json_read.php";

function getLogData(){
    $param = "";
	$json_data = queryMyrror($param);
    $data = getMyrrorData($json_data);
    
    return $data;
}

function createURL_old($mood, $stress, $depression, $fatclass, $activity, $sleep, $vegetarian, $lactose, $gluten, $nickel, $light, $diabetes, $pregnant, $exp){
    $url = "http://localhost:5002/mood/?";

    if($mood == 'Bad')
        $url = $url . "mood=bad&";
    if($stress== 'yes')
        $url = $url . "stress=yes&";
    if($depression == 'yes')
        $url = $url . "depression=yes&";
    if($fatclass < 19)
        $url = $url . "underweight=yes&";
    if($fatclass >= 25)
        $url = $url . "overweight=yes&";
    if($activity == "high")
        $url = $url . "activity=high&";
    if($activity == "low")
        $url = $url . "activity=low&";
    if($sleep == 'low')
        $url = $url . "sleep=low&";
    if($vegetarian)
        $url = $url . "isVegetarian=1&";
    if($diabetes)
        $url = $url . "isDiabetes=1&";
    if($pregnant)
        $url = $url . "isPregnant=1&";
    if($lactose)
        $url = $url . "isLactoseFree=1&";
    if($gluten)
        $url = $url . "isGlutenFree=1&";
    if($nickel)
        $url = $url . "isLowNickel=1&";
    if($light)
        $url = $url . "'isLight'=1&";

    $url = $url . "difficulty=". $exp ."&";
    $url = $url . "n=10&lang=en";

    return $url;
}

function createURL($mood, $stress, $depression, $fatclass, $activity, $sleep, $vegetarian, $lactose, $gluten, $nickel, $light, $diabetes, $pregnant, $exp, $user_time, $user_cost, $age, $goal){
    $url = "http://localhost:5009/mood/?";

    if($mood == 'Bad')
        $url = $url . "mood=bad&";
    if($stress== 'yes')
        $url = $url . "stress=yes&";
    if($depression == 'yes')
        $url = $url . "depression=yes&";
    $url = $url . "fatclass=". $fatclass ."&";
    if($activity == "high")
        $url = $url . "activity=high&";
    if($activity == "normal")
        $url = $url . "activity=medium&";
    if($sleep == 'low')
        $url = $url . "sleep=low&";
    if($vegetarian)
        $url = $url . "isVegetarian=1&";
    if($diabetes)
        $url = $url . "isDiabetes=1&";
    if($pregnant)
        $url = $url . "isPregnant=1&";
    if($lactose)
        $url = $url . "isLactoseFree=1&";
    if($gluten)
        $url = $url . "isGlutenFree=1&";
    if($nickel)
        $url = $url . "isLowNickel=1&";
    if($light)
        $url = $url . "'isLight'=1&";

    $url = $url . "difficulty=". $exp ."&";
    $url = $url . "user_time=". $user_time ."&";
    $url = $url . "user_cost=". $user_cost ."&";
    $url = $url . "age=". $age ."&";
    $url = $url . "goal=". $goal ."&";

    $url = $url . "n=10&lang=en";

    return $url;
}

function createUrlExp(
		$mood, $stress, $depression,
		$fatclass, $health_style, $health_condition, $activity, $sleep,
		$vegetarian, $lactose, $gluten, $nickel, $light, $diabetes, $pregnant,
		$user_time, $user_cost, $age, $goal,
		$user_difficulty, $imgurlA, $imgurlB,
        $userFavIngredient, $type_explanation)
	{	
	$url = "http://localhost:5003/exp/?";

	    //TYPE EXPLANATIION
        $url = $url . "type=" . $type_explanation . "&";

        //MOOD
        if($mood == 'Bad')
            $url = $url . "mood=bad&";
        else {
            if($mood == 'Good')
                $url = $url . "mood=good&";
            else
                $url = $url . "mood=neutral&";
        }
        //STRESS
        if($stress== 'yes')
            $url = $url . "stress=yes&";
        else
            $url = $url . "stress=no&";

        //DEPRESSION
        if($depression == 'yes')
            $url = $url . "depression=yes&";
        else
            $url = $url . "depression=no&";

        //HEALTH LIFESTYLE
        $url = $url . "health_style=". $health_style ."&";
        //HEALTH CONDITION
        $url = $url . "health_condition=" . $health_condition . "&";
        //BMI
        if($fatclass<19.0)
            $url = $url . "bmi=under&";
        else {
            if($fatclass>=19.0 && $fatclass<25.0)
                $url = $url . "bmi=over&";
            else
                $url = $url . "bmi=normal&";
        }

        //ACTIVITY
        if($activity == "high")
            $url = $url . "activity=high&";
        else {
            if($activity == "low")
                $url = $url . "activity=low&";
            else
                $url = $url . "activity=normal&";
        }

        //SLEEP
        if($sleep == 'low')
            $url = $url . "sleep=low&";
        else
            $url = $url . "sleep=good&";

        //COOKING EXPERIENCE
        $url = $url . "difficulty=". $user_difficulty ."&";

        //TIME and COST
        $url = $url . "user_time=". $user_time ."&";
        $url = $url . "user_cost=". $user_cost ."&";

        //AGE
        $url = $url . "user_age=". $age ."&";

        //GOAL
        if($goal == "Lose weight")
            $url = $url . "goal=lose&";
        else {
            if($goal == "Gain weight")
                $url = $url . "goal=gain&";
            else
                $url = $url . "goal=no&";
        }

        //RESTRICTION & INGREDIENTS
        $restrictions = [];

        //RESTRICTION
        if($vegetarian)
            array_push($restrictions,"vegetarian");
        if($diabetes)
            array_push($restrictions,"diabetes");
        if($pregnant)
            array_push($restrictions,"pregnant");
        if($lactose)
            array_push($restrictions,"lactosefree");
        if($gluten)
            array_push($restrictions,"glutenfree");
        if($nickel)
            array_push($restrictions,"lownichel");
        if($light)
            array_push($restrictions,"light");

        if(count($restrictions) > 0)
            $url = $url . "restr=" . urlencode(implode(",",$restrictions)) . "&";

        //INGREDIENTS
        $url = $url . "user_ingredients=" . $userFavIngredient . "&";

        //IMGURL
        $url = $url
            . "imgurl1=" . urlencode($imgurlA)
            . "&imgurl2=" . urlencode($imgurlB);
        //."&n=5&lang=en";

        return $url;
}

function getExplanation($url) {
	return performRequestExp($url);
}


function getRecipes($pers_url_new, $pers_url_old){
    /*
    se il valore di $rec_1 o $rec_2 è 0 allora è stato utilizzato il sistema di raccomandazione popolare
    se il valore di $rec_1 o $rec_2 è 1 allora è stato utilizzato il sistema di raccomandazione precedente (run on 5002)
    se il valore di $rec_1 o $rec_2 è 2 allora è stato utilizzato il sistema di raccomandazione attuale (run on 5009)

    $rec_1 = rand(0,2);

    if($rec_1 == 0){
        $pers_url_1 = "http://localhost:5009/mood/?fatclass=22&n=10&lang=en";
        $rec_2 = rand(1,2);

        if($rec_2 == 1){
            $pers_url_2 = $pers_url_old;
        }
        else{
            $pers_url_2 = $pers_url_new;
        }
    }

    if($rec_1 == 1){
        $pers_url_1 = $pers_url_old;
        $rec_2 = rand(0,1) * 2;

        if($rec_2 == 0){
            $pers_url_2 = "http://localhost:5009/mood/?fatclass=22&n=10&lang=en";
        }
        else{
            $pers_url_2 = $pers_url_new;
        }
    }

    if($rec_1 == 2){
        $pers_url_1 = $pers_url_new;
        $rec_2 = rand(0,1);

        if($rec_2 == 0){
            $pers_url_2 = "http://localhost:5009/mood/?fatclass=22&n=10&lang=en";
        }
        else{
            $pers_url_2 = $pers_url_old;
        }
    }
    /* per test
    $rec_1 = 2;
    $rec_2 = 1;

    $pers_url_2 = $pers_url_old;
    $pers_url_1 = $pers_url_new;
    */

    $rec_1 = 2;
    $rec_2 = 0;

    $pers_url_1 = $pers_url_new;
    $pers_url_2 = "http://localhost:5009/mood/?fatclass=22&n=10&lang=en";
    $pers_data_primo_1 = performRequest(($pers_url_1."&category=Primi%20piatti"), $rec_1);
    $pers_data_primo_2 = performRequest(($pers_url_2."&category=Primi%20piatti"), $rec_2);

    $pers_data_secondo_1 = performRequest(($pers_url_1."&category=Secondi%20piatti"), $rec_1);
    $pers_data_secondo_2 = performRequest(($pers_url_2."&category=Secondi%20piatti"), $rec_2);

    $pers_data_dolce_1 = performRequest(($pers_url_1."&category=Dolci"), $rec_1);
    $pers_data_dolce_2 = performRequest(($pers_url_2."&category=Dolci"), $rec_2);

    return array(
        "personalized_main_1" => $pers_data_primo_1,
        "personalized_main_2" => $pers_data_primo_2,
        "personalized_second_1" => $pers_data_secondo_1,
        "personalized_second_2" => $pers_data_secondo_2,
        "personalized_dessert_1" => $pers_data_dolce_1,
        "personalized_dessert_2" => $pers_data_dolce_2,
        "rec_1" => $rec_1,
        "rec_2" => $rec_2);
}

function performRequest($url, $typeRecommendation){
    /*
    se il valore di $typeRecommendation è 0 allora è stato utilizzato il sistema di raccomandazione popolare
    se il valore di $typeRecommendation è 1 allora è stato utilizzato il sistema di raccomandazione precedente (run on 5002)
    se il valore di $typeRecommendation è 2 allora è stato utilizzato il sistema di raccomandazione attuale (run on 5009)
    */
    $top = 0; //indica la ricetta restituita, se 0 => top-1

    /*
     * Se si tratta della ricetta consigliata con il sistema popolare ($typeRecommendation = 0) restituiamo una random tra le top-5 per diversificare
     * Se si tratta della ricetta consigliata dal recommender ($typeRecommendation = 1 o 2) restituiamo la top-1
     */
    if ($typeRecommendation == 0)
    {
        $top = rand(0, 4);
    }

    ///  Initiate curl
    $ch = curl_init();
    // Will return the response, if false it print the response
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    // Set the url
    curl_setopt($ch, CURLOPT_URL, $url);
    // Execute
    $result=curl_exec($ch);
    // Closing
    curl_close($ch);

    //sostituisco \" con " e \\ con \ nel risultato, poi elimino il primo carattere (") e gli ultimi due ("\n)
    //$result = str_replace("\\", "", "$result");
    $result = str_replace('\\"', "\"", "$result");
    $result = str_replace('\\\\', "\\", "$result");
    $result = substr($result, 1);
    $result = substr_replace($result ,"", -2);
    //echo $result;

    //vado a decodificare il json e lo metto in un array
    $arr = json_decode($result,true);

    //salvo il nome della ricetta, l'url dell'immagine e gli altri elementi da restituire
    if(!empty($arr["data"])) {
        $name = $arr["data"][$top][1];
        $imageURL = $arr["data"][$top][4];
        $ingredients = $arr["data"][$top][24];
        $description = $arr["data"][$top][5];
        $url = $arr["data"][$top][0];


        return array("name" => $name, "imgURL" => $imageURL, "ingredients" => $ingredients, "description" => $description, "url" => $url);
    }
    else{
        return array("name" => "Purtroppo non ho trovato nessuna ricetta &#x1f60c");
    }
}

function performRequestExp($url){
	
	//  Initiate curl
	$ch = curl_init();
	
	// Will return the response, if false it print the response
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	
	// Set the url
	curl_setopt($ch, CURLOPT_URL, $url);
	
	// Execute
	$result=curl_exec($ch);
	
	// Closing
	curl_close($ch);
	
	//json dedode in array
	$jsonArray = json_decode(json_decode($result),true);
	
	return($jsonArray['explanations']);
}

function getMyrrorData($json_data){
	$dateOfBirth = null;
    $height = null;
    $weight = null;
    $emotion = null;
    $mood = null;
    $stress = null;
    $BMI=null;
    $depression = null;
    $activity = array(0,0,0);
    $overweight = null;
    $underweight = null;    
    $count = 0;
    $sumInBed = 0;
    $sumAsleep = 0;
    $sleep = null;

	foreach ($json_data as $key1 => $value1) {
		//trovo la data di nascita
        if(isset($value1['dateOfBirth'])){
			foreach ($value1['dateOfBirth'] as $key2 => $value2) {
				if ($key2 == "value") {
					$dateOfBirth = $value2;
				} 	
        	}	
		}
        
        //trovo l'altezza
        if(isset($value1['height'])){
			foreach ($value1['height'] as $key2 => $value2) {
				if ($key2 == "value") {
					$height = $value2;
				} 	
        	}	
		}
        
        //trovo il peso
        if(isset($value1['weight'])){
			foreach ($value1['weight'] as $key2 => $value2) {
				if ($key2 == "value") {
					$weight = $value2;
				} 	
        	}	
		}
        
        //trovo l'umore
        $max = "";
        if($key1 == 'affects'){
			foreach ($value1 as $affect) {
                $date = substr($affect['date'],0, 10);
				if ($date > $max) {
					$emotion = $affect['emotion'];
                    $max = $date;
				} 	
        	}	
		}
        
        //controllo l'attività
        $max = 0;
        if(isset($value1['fromActivity'])){
            foreach ($value1['fromActivity'] as $key2 => $value2) {
                $timestamp = $value2['timestamp'];
                if($timestamp >= $max && $value2['nameActivity'] != "calories"  && $value2['nameActivity'] != "steps" && $value2['nameActivity'] != "minutesSedentary"  && $value2['nameActivity'] != "distance"){
                    switch ($value2['nameActivity']) {
                        case 'fairly':
                            $activity[0] = $value2['minutesFairlyActive'];        
                            $max = $timestamp;
                            break;
                        
                        case 'minutesLightlyActive':
                            $activity[1] = $value2['minutesLightlyActive'];
                            $max = $timestamp;
                            break;
                        
                        case 'veryActive':
                            $activity[2] = $value2['minutesVeryActive'];
                            $max = $timestamp;
                            break;
                        
                        default:
                            break;
                    }
                }
            }
        }
        
        //sonno
        if(isset($value1['sleep'])){
            //ricerca per periodo   
            foreach ($value1['sleep'] as $key2 => $value2) {
                $sumInBed += $value2['timeInBed'];
                $sumAsleep += $value2['minutesAsleep'];
                $count++;         
            }
        }
        
	}
    
    //calcolo età
    $years = null;
	if(!is_null($dateOfBirth)){
		$today = date("Y-m-d");
		$diff = abs(strtotime($today) - strtotime($dateOfBirth));
    	$years = floor($diff / (365*60*60*24));
	}
        
    //controllo sull'emozione per avvalorare mood, depression e stress
	switch ($emotion) { //gioia, paura, rabbia, disgusto, tristezza, sorpresa
        case "fear\n":
            $mood = "Bad";
            $stress = "no"; 
            $depression = "no";
        break;
      case "anger\n":
            $mood = "Bad";
			$stress = "yes"; 
            $depression = "no";
        break;
      case "disgust\n":
			$mood = "Bad";
            $stress = "no"; 
            $depression = "no";
        break;
      case "sad\n":
            $mood = "Bad";
            $stress = "no"; 
			$depression = "yes";
        break;
    }
    
    //regola per l'attività fisica
    $sum = $activity[0] + $activity[1] + $activity[2];
	if($sum >=30){
		$activity = "high";
	}
	else{
		$activity = "low";
	}
    
    //controllo sul sonno
    if($count != 0){
        $sleepAV = intval($sumAsleep/$count);
        $inBedAV =intval($sumInBed/$count);
        
        if($sleepAV <= 390)
            $sleep = "low";
        else $sleep = "high";
    }
    
    //calcoloBMI
    if(!is_null($height) && !is_null($weight)){
         $BMI = $weight / (pow(($height/100),2));
    }
    
    if(!is_null($BMI) && $BMI > 25){
        $overweight = true;
        $underweight = false;
    }
    else if(!is_null($BMI) && $BMI < 18.5){
        $overweight = false;
        $underweight = true;
    }
    else if(!is_null($BMI)){
        $overweight = false;
        $underweight = false;
    }

    
    return array("age" => $years,"overweight" => $overweight, "underweight" => $underweight, "mood" => $mood, "stress" => $stress, "depression" => $depression, "activity" => $activity, "sleep" => $sleep);
}

function createIngText($ingredients){
    $ingredients = str_replace("\"","",$ingredients);
    $ingredients = str_replace("[","",$ingredients);
    $ingredients = str_replace("]","",$ingredients);
    $ingredients = str_replace(",","<br>",$ingredients);
    return $ingredients;
}