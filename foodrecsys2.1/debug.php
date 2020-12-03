<?php

/*
if(empty($_POST))
	header("location:index.php");


if(isset($_POST['prevDish'])) {
	@session_start();
	if(session_status() === PHP_SESSION_NONE)
		header("location:index.php");

} else {
	@session_start();
}

*/


@session_start();
$typeExps = array(
    "popularity_two",
    "descriptions",
    "foodGoals_two",
    "userLifestyle_two",
    "foodFeatureHealthRisk_two",
    "foodFeatureHealthBenefits_two",
    "userFeatureHealthRisk_two",
    "userFeatureHealthBenefits_two"
);


?>
<!DOCTYPE html>
<html lang="en">
<?php include "php/head.php"; ?>
<body data-spy="scroll" data-target="#navbar-nav-header" class="single-layout">
<?php

include "php/requestFunctions.php";

$postPage = 'action="debug.php"';
$answers = '';

//QUI RANDOMIZZA TUTTO
$dish = $_POST['dish'];
#type explanation to get the same type for every recipe (u can use if u want a specific  type of exp for every recipe -> manage in expl web serv)
$type_explanation = rand(0, 13);

//type of exps for experiment
$typeExps = array(
    "popularity_two",
    "descriptions",
    "foodGoals_two",
    "userLifestyle_two",
    "foodFeatureHealthRisk_two",
    "foodFeatureHealthBenefits_two"
);

//for the experiment I use a random exp, one of these random, different for every dish
$expMainIndex = rand(0, count($typeExps) - 1);
$expSecondIndex = rand(0, count($typeExps) - 1);
$expDessertIndex = rand(0, count($typeExps) - 1);



if($dish == "main"){
    $sexOptions = array("m", "f");
    $sex = $sexOptions[rand(0,1)];
    $ageOptions = array("U20", "U40", "U60");
    $age = $ageOptions[rand(0,2)];
    $height = rand(150,200);
    $weight = rand(50,100);
    $fatclass = ($weight * 10000) / ($height * $height);
    $health_style = rand(1,5);
    $health_condition = rand(1,5);
    $health_food_choise = rand(1,5);
    $control_nutritional_value = rand(1,5);
    $occupation = "Student";
    $websiteUsage = "Never";
    $cookingFreq = "Daily";
    $user_difficulty = rand(1,5);
    $goalOptions = array(0,1,-1);
    $goal = $goalOptions[rand(0,2)];
    $moodOptions = array("Good", "Bad", "Neutral");
    $mood = $moodOptions[rand(0,2)];
    $activityOptions = array("high", "medium", "low");
    $activity = $activityOptions[rand(0,2)];
    $sleepOptions = array("high", "low");
    $sleep = $sleepOptions[rand(0,1)];
    $stressOptions = array("yes", "no");
    $stress = $stressOptions[rand(0,1)];
    $depression =  $stressOptions[rand(0,1)];
    $user_time = 0;
    $user_cost = 5;

    $answers = $sex . ":q," . $age . ":q," . $fatclass . ":q," . $health_style . ":q,"
        . $health_condition . ":q," . $health_food_choise . ":q," . $control_nutritional_value . ":q,"
        . $occupation . ":q," . $websiteUsage . ":q," . $cookingFreq . ":q,"
        . $user_difficulty . ":q," . $goal . ":q," . $mood . ":q,"
        . $activity . ":q," . $sleep . ":q," . $stress . ":q," . $depression . ":q,"
        . $user_cost . ":q," . $user_time . ":q," ;

    #recipe's ingredients
    $userFavIngredients = "niente, nulla";
    $userFavIngredients = trim($userFavIngredients);
    $userFavIngredients = str_replace(",", "-", $userFavIngredients);
    $userFavIngredients = str_replace(";", "-", $userFavIngredients);
    $userFavIngredients = preg_replace('/[^A-Za-z0-9\-]/', '', $userFavIngredients); // Removes special chars
    preg_replace('/-+/', '-', $userFavIngredients); // Replaces multiple hyphens with single one
    $answers = $answers . $userFavIngredients . ":q," ;

    if(rand(0,1) ==1){
        $vegetarian = true;
        $answers = $answers . "-vegetarian-";
    }
    else{
        $vegetarian = false;
    }

    if(rand(0,1) ==1){
        $lactose = true;
        $answers = $answers . "-lactosefree-";
    }
    else{
        $lactose = false;
    }

    if(rand(0,1) ==1){
        $gluten= true;
        $answers = $answers . "-glutenfree-";
    }
    else{
        $gluten = false;
    }

    if(rand(0,1) ==1){
        $nickel=true;
        $answers = $answers . "-lownickel-";
    }
    else{
        $nickel = false;
    }

    if(rand(0,1) ==1){
        $light=true;
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
            $userFavIngredients, $type_explanation)
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
            $userFavIngredients, $type_explanation)
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
            $userFavIngredients, $type_explanation)
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
    $postPage = 'action="byeDebug.php"';
}

$dish_name = $dish;
if($dish_name !== 'dessert')
    $dish_name = $dish_name . ' course';

//salvo le risposte al questionario
//if(isset($_POST['answers']))
//	$answers = $_POST['answers'];

if(isset($_POST['Q1']))
    $answers = $answers . $_POST['Q1'] . ',';

if(isset($_POST['Q2']))
    $answers = $answers . $_POST['Q2'] . ',';
else if($dish !== "main")
    $answers = $answers . ',';

if(isset($_POST['Q3']))
    $answers = $answers . $_POST['Q3'] . ',';
else if($dish !== "main")
    $answers = $answers . ',';

if(isset($_POST['Q4']))
    $answers = $answers . $_POST['Q4'] . ',';
else if($dish !== "main")
    $answers = $answers . ',';

if(isset($_POST['Q5']))
    $answers = $answers . $_POST['Q5'] . ',';
else if($dish !== "main")
    $answers = $answers . ',';

if(isset($_POST['Q6']))
    $answers = $answers . $_POST['Q6'] . ',';
else if($dish !== "main")
    $answers = $answers . ',';

if(isset($_POST['Q7']))
    $answers = $answers . str_replace(",", " ", $_POST['Q7']) . ',';
else if($dish !== "main")
    $answers = $answers . ',';

if(isset($_POST['prevDish']))
    $_SESSION['answers'][$_POST['prevDish']] = $answers;
?>

<div class="boxed-page">
    <?php include "php/header.php"; ?>
    <section id="gtco-single-content" class="bg-white">
        <div class="container">
            <div class="section-content blog-content">

                <!-- Section Title -->
                <div class="title-wrap">
                    <h2 class="section-title">Your recipes</h2>
                    <p class="section-sub-title">Take a look to the <?= strpos($dish_name,"exp") ? str_replace("_exp","",$dish) : $dish_name ?> and answer the questions</p>
                </div>
                <!-- End of Section Title -->

                <div class="row">  <!-- none, show-->
                    <?php

                    $exp = (strpos($dish, "exp")) ? true : false;

                    if($exp) {
                        $rec = str_replace("_exp","",$dish);

                        $pRecipeName = $data[('personalized_'.$rec.'_1')]['name'];
                        $pImgURL = $data[('personalized_'.$rec).'_1']['imgURL'];
                        $pIngredients = $data[('personalized_'.$rec.'_1')]['ingredients'];
                        //$pDescription = $data[('personalized_'.$rec.'_1')]['description'];
                        $pURL = $data[('personalized_'.$rec.'_1')]['url'];
                        $pIngredients = createIngText($pIngredients);


                        $recipeName = $data[('personalized_'.$rec.'_2')]['name'];
                        $imgURL = $data[('personalized_'.$rec.'_2')]['imgURL'];
                        $ingredients = $data[('personalized_'.$rec.'_2')]['ingredients'];
                        //$description = $data[('personalized_'.$rec.'_2')]['description'];
                        $URL = $data[('personalized_'.$rec.'_2')]['url'];
                        $ingredients = createIngText($ingredients);
                    } else {
                        $pRecipeName = $data[('personalized_'.$dish.'_1')]['name'];
                        $pImgURL = $data[('personalized_'.$dish.'_1')]['imgURL'];
                        $pIngredients = $data[('personalized_'.$dish.'_1')]['ingredients'];
                        //$pDescription = $data[('personalized_'.$dish.'_1')]['description'];
                        $pURL = $data[('personalized_'.$dish.'_1')]['url'];
                        $pIngredients = createIngText($pIngredients);


                        $recipeName = $data[('personalized_'.$dish.'_2')]['name'];
                        $imgURL = $data[('personalized_'.$dish.'_2')]['imgURL'];
                        $ingredients = $data[('personalized_'.$dish.'_2')]['ingredients'];
                        //$description = $data[('personalized_'.$dish.'_2')]['description'];
                        $URL = $data[('personalized_'.$dish.'_2')]['url'];
                        $ingredients = createIngText($ingredients);
                    }

                    $explanations = $_SESSION['explanations'];
                    $mainTypeExpl = $_SESSION['mainTypeExpl'];
                    $secondTypeExpl = $_SESSION['secondTypeExpl'];
                    $dessertTypeExpl = $_SESSION['dessertTypeExpl'];

                    $typeOfExp = "";
                    switch ($dish){
                        case "main_exp":
                            $typeOfExp = $mainTypeExpl;
                            break;
                        case "second_exp":
                            $typeOfExp = $secondTypeExpl;
                            break;
                        case "dessert_exp":
                            $typeOfExp = $dessertTypeExpl;
                            break;
                    }
                    ?>
                    <!-- <a href="<?= $pURL ?>" target="_blank" class="col-md-6 blog-item-wrapper"> -->
                    <div class="col-lg-6 blog-item-wrapper recipe">
                        <div class="blog-item recipe-content">
                            <div class="blog-img">
                                <img src="<?= $pImgURL ?>" alt="">
                            </div>
                            <div class="blog-text">
                                <div id="titleA" class="blog-title text-center">
                                    <h4><?= $pRecipeName ?></h4>
                                </div>

                                <!-- Here descr-->

                                <div class="blog-author">
                                    <button data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                        Click to show ingredients
                                    </button>
                                    <div id="collapseOne" class="collapse ingredients"><p><?= $pIngredients ?></p></div>
                                </div>
                            </div>
                        </div>
                        <?php /* if($exp) : ?>
									<div class="blog-item explanation">
										<div id="expA" class="blog-text">
											<div class="blog-desc">
												<p><font color="black"><?= $explanations["main_exp"][0] ?></font></p>
											</div>
										</div>
									</div>
								<?php endif; */ ?>
                    </div>

                    <!-- <a href="<?= $URL ?>" target="_blank" class="col-md-6 blog-item-wrapper"> -->
                    <div class="col-lg-6 blog-item-wrapper recipe">
                        <div class="blog-item recipe-content">
                            <div class="blog-img">
                                <img src="<?= $imgURL ?>" alt="">
                            </div>
                            <div class="blog-text">
                                <div id="titleB" class="blog-title text-center">
                                    <h4><?= $recipeName ?></h4>
                                </div>

                                <!-- Here descr-->

                                <div class="blog-author">
                                    <button data-toggle="collapse" data-target="#collapseTwo" aria-expanded="true" aria-controls="collapseOne">
                                        Click to show ingredients
                                    </button>
                                    <div id="collapseTwo" class="collapse"><p><?= $ingredients ?></p></div>
                                </div>
                            </div>
                        </div>
                        <?php /* if($exp) : ?>
									<div class="blog-item explanation">
										<div class="blog-text">
											<div id="expB" class="blog-desc">
												<p><font color="black"><?= $explanations["main_exp"][1] ?></font></p>
											</div>
										</div>
									</div>
								<?php endif; */ ?>
                    </div>
                </div>

                <?php if($exp) : ?>
                    <div class="row explanationComb">
                        <div class="col-lg-12">
                            <div class="blog-item">
                                <div class="blog-text">
                                    <div id="expB" class="blog-desc">
                                        <p><font color="black">"popularity_two":<?= $explanations[$dish]["popularity_two"] ?>
                                                <br> "descriptions":<?= $explanations[$dish]["descriptions"] ?>
                                                <br>"foodGoals_two":<?= $explanations[$dish]["foodGoals_two"] ?>
                                                <br> "userLifestyle_two":<?= $explanations[$dish]["userLifestyle_two"] ?>
                                                <br> "foodFeatureHealthRisk_two":<?= $explanations[$dish]["foodFeatureHealthRisk_two"] ?>
                                                <br> "foodFeatureHealthBenefits_two":<?= $explanations[$dish]["foodFeatureHealthBenefits_two"] ?>
                                                <br> "userFeatureHealthRisk_two":<?= $explanations[$dish]["userFeatureHealthRisk_two"] ?>
                                                <br> "userFeatureHealthBenefits_two":<?= $explanations[$dish]["userFeatureHealthBenefits_two"] ?>
                                                <br><br> Explanations for recipe A:
                                                <br>"popularity_one":<?= $explanations[$dish]["popularity_oneA"] ?>
                                                <br> "description":<?= $explanations[$dish]["descriptionA"] ?>
                                                <br>"foodGoals_one":<?= $explanations[$dish]["foodGoals_oneA"] ?>
                                                <br> "userLifestyle_one":<?= $explanations[$dish]["userLifestyle_oneA"] ?>
                                                <br> "foodFeatureHealthRisk_one":<?= $explanations[$dish]["foodFeatureHealthRisk_oneA"] ?>
                                                <br> "foodFeatureHealthBenefits_one":<?= $explanations[$dish]["foodFeatureHealthBenefits_oneA"] ?>
                                                <br> "userFeatureHealthRisk_one":<?= $explanations[$dish]["userFeatureHealthRisk_oneA"] ?>
                                                <br> "userFeatureHealthBenefits_one":<?= $explanations[$dish]["userFeatureHealthBenefits_oneA"] ?>
                                                <br><br> Explanations for recipe B:
                                                <br>"popularity_one":<?= $explanations[$dish]["popularity_oneB"] ?>
                                                <br> "description":<?= $explanations[$dish]["descriptionB"] ?>
                                                <br>"foodGoals_one":<?= $explanations[$dish]["foodGoals_oneB"] ?>
                                                <br> "userLifestyle_one":<?= $explanations[$dish]["userLifestyle_oneB"] ?>
                                                <br> "foodFeatureHealthRisk_one":<?= $explanations[$dish]["foodFeatureHealthRisk_oneB"] ?>
                                                <br> "foodFeatureHealthBenefits_one":<?= $explanations[$dish]["foodFeatureHealthBenefits_oneB"] ?>
                                                <br> "userFeatureHealthRisk_oneA":<?= $explanations[$dish]["userFeatureHealthRisk_oneB"] ?>
                                                <br> "userFeatureHealthBenefits_one":<?= $explanations[$dish]["userFeatureHealthBenefits_oneB"] ?></font></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endif; ?>

                <div class='row'>
                    <div class="col-lg-12">
                        <form id="recipeForm" method="post" <?= $postPage ?> >
                            <input type="hidden" name="prevDish" id="prevDish" value="<?= $dish ?>" />

                            <?php if($exp): ?>
                                <input type="hidden" name="prevChoice" id="prevChoice" value='<?= $_POST["Q1"] ?>' />
                            <?php endif; ?>

                            <?php include("php/questionnaire".($exp==false ? ".php" : "_exp.php")); ?>

                            <?php
                            switch($dish) {
                                case "main":
                                    $dish = "main_exp";
                                    break;
                                case "main_exp":
                                    $dish = "second";
                                    break;
                                case "second":
                                    $dish = "second_exp";
                                    break;
                                case "second_exp":
                                    $dish = "dessert";
                                    break;
                                case "dessert":
                                    $dish = "dessert_exp";
                                    break;
                            }
                            ?>
                            <input type="hidden" name="dish" id="hiddenField" value="<?= $dish ?>" />

                            <div class="col-lg-12 text-center">
                                <button id="btnForm" class="btn btn-block btn-secondary btn-red col-md-4 offset-md-4 " type="submit" >Continue</button>
                            </div>
                        </form>
                    </div>

                </div>
            </div>
        </div>
    </section>
    <?php include "php/footer.php"; ?>
</div>

<script>
    $(document).ready(function(){
        if($(window).width()>991) {
            var h1 = $("#titleA").height();
            var h2 = $("#titleB").height();
            var hMax = Math.max(h1,h2);
            $("#titleA").height(hMax);
            $("#titleB").height(hMax);

            h1 = $("#descA").height();
            h2 = $("#descB").height();
            hMax = Math.max(h1,h2);
            $("#descA").height(hMax);
            $("#descB").height(hMax);

        }
    });

    $(window).resize(function(){
        if($(window).width()>991) {
            var h1 = $("#titleA").height();
            var h2 = $("#titleB").height();
            var hMax = Math.max(h1,h2);
            $("#titleA").height(hMax);
            $("#titleB").height(hMax);

            h1 = $("#descA").height();
            h2 = $("#descB").height();
            hMax = Math.max(h1,h2);
            $("#descA").height(hMax);
            $("#descB").height(hMax);

        }
    });
</script>

<!-- <script src="js/app.min.js "></script> -->
<!-- <script src="//localhost:35729/livereload.js"></script> -->
</body>
</html>