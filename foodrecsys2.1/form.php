<!DOCTYPE html>
<?php
@session_start();
//type of explanation
//decide to show expl [ 0 ==> no explanation - 1 ==> single recipe explanations - 2 == double expl]
$showExpl = rand(0, 2);
$_SESSION['showExpl'] = $showExpl;
$_SESSION['mainTypeExpl'] = "";
$_SESSION['secondTypeExpl'] = "";
$_SESSION['dessertTypeExpl'] = "";

$_SESSION['mainTypeExplA'] = "";
$_SESSION['secondTypeExplA'] = "";
$_SESSION['dessertTypeExplA'] = "";

$_SESSION['mainTypeExplB'] = "";
$_SESSION['secondTypeExplB'] = "";
$_SESSION['dessertTypeExplB'] = "";

?>
<html lang="en">
    <?php include "php/head.php"; ?>
    <body data-spy="scroll" data-target="#navbar-nav-header" class="single-layout">
        <div class="boxed-page">
            <?php include "php/header.php"; ?>
            <section id="gtco-single-content" class="bg-white">
                <div class="container">
                    <div class="section-content blog-content">
                        
                        <!-- Section Title -->
                        <div class="title-wrap">
                            <h2 class="section-title">Profile builder</h2>
                            <p class="section-sub-title">Please answer the following questions</p>

                        </div>
                        <!-- End of Section Title -->

                        <div class="row mx-auto">
                            <!-- form -->
                            <div class="col-md-10 offset-md-1 contact-form-holder mt-4">
                                <form id="form" method="post" action="recipes.php">
                                    <!-- Sex and age -->
                                    <div class="form-group row">
                                        <label for="sexOption" class="col-sm-2 col-form-label">You are a:</label>
                                        <div class="col-sm-3">
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="sexOption" id="male" value="m" required>
                                                <label class="form-check-label" for="male">Male</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="sexOption" id="female" value="f" required>
                                                <label class="form-check-label" for="female">Female</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="sexOption" id="notsay" value="na" required>
                                                <label class="form-check-label" for="notsay">Prefer not to say</label>
                                            </div>
                                        </div>

                                        <label for="age" class="col-sm-2 col-form-label offset-sm-1">Your age is:</label>
                                        <div class="col-sm-2" style="padding-right : 0px; margin-right : 0px;">
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="age" id="U20" value="U20" required>
                                                <label class="form-check-label" for="U20">&lt;20</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="age" id="U40" value="U40" required>
                                                <label class="form-check-label" for="U40">30-39</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="age" id="U60" value="U60" required>
                                                <label class="form-check-label" for="U60">50-59</label>
                                            </div>
                                        </div>
                                        <div class="col-sm-2" style="padding-left:0px; margin-left:0px;">
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="age" id="U30" value="U30" required>
                                                <label class="form-check-label" for="U30">20-29</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="age" id="U50" value="U50" required>
                                                <label class="form-check-label" for="U50">40-49</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="age" id="O60" value="O60" required>
                                                <label class="form-check-label" for="O60">&gt;60</label>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="form-group row">
                                        <div class="col-sm-6" style="padding-right : 0px; margin-right : 0px;">
                                            <label class="col-form-label">In your opinion, to have a healthy lifestyle is:</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <select class="form-control" id="HLselector" name="HS">
                                                <option hidden disabled selected value></option>
                                                <option value="1">Absolutely not important</option>
                                                <option value="2">Not important</option>
                                                <option value="3">Poorly important</option>
                                                <option value="4">Important</option>
                                                <option value="5">Very important</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- health conditions -->
                                    <div class="form-group row">
                                        <div class="col-sm-6" style="padding-right : 0px; margin-right : 0px;">
                                            <label class="col-form-label">How do you consider your lifestyle:</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <select class="form-control" id="HCselector" name="HC">
                                                <option hidden disabled selected value></option>
                                                <option value="1">Absolutely not healthy</option>
                                                <option value="2">Not healthy</option>
                                                <option value="3">Quite healty</option>
                                                <option value="4">Healty</option>
                                                <option value="5">Very healty</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- healthy food choice -->
                                    <div class="form-group row">
                                        <div class="col-sm-6" style="padding-right : 0px; margin-right : 0px;">
                                            <label class="col-form-label">I try to make healthy food choices every day:</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <select class="form-control" id="HFCselector" name="HFC">
                                                <option hidden disabled selected value></option>
                                                <option value="5">Always</option>
                                                <option value="4">Often</option>
                                                <option value="3">Usually</option>
                                                <option value="2">Rarely</option>
                                                <option value="1">Never</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- Nutritional value -->
                                    <div class="form-group row">
                                        <div class="col-sm-6" style="padding-right : 0px; margin-right : 0px;">
                                            <label class="col-form-label">I look at the nutritional value of food products I buy:</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <select class="form-control" id="HNVselector" name="HNV">
                                                <option hidden disabled selected value></option>
                                                <option value="5">Always</option>
                                                <option value="4">Often</option>
                                                <option value="3">Usually</option>
                                                <option value="2">Rarely</option>
                                                <option value="1">Never</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- BMI -->
                                    <div class="form-group row">
                                        <label for="height" class="col-sm-6 col-form-label">Height(cm):
                                            <input type="number" id="height" name="height" min="100" max="220" step="1">
                                        </label>
                                        <label for="weight" class="col-sm-6 col-form-label">Weight(kg):
                                            <input type="number" id="weight" name="weight" min="15" max="200" step="1">
                                        </label>
                                    </div>

                                    <!-- Employment -->
                                    <div class="form-group row">
                                        <label for="occupationSelector" class="col-sm-6 col-form-label">Employment:</label>
                                        <div class="col-sm-5">
                                            <select class="form-control" id="occupationSelector" name="occupation" required>
                                                <option hidden disabled selected value></option>
                                                <option>Student</option>
                                                <option>Private company staff</option>
                                                <option>Public company staff</option>
                                                <option>Self employed</option>
                                                <option>Unemployed</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- Recipe website usage -->
                                    <div class="form-group row">
                                        <label for="websiteUsageSelector" class="col-sm-6 col-form-label">Recipe website usage:</label>
                                        <div class="col-sm-5">
                                            <select class="form-control" id="websiteUsageSelector" name="websiteUsage" required>
                                                <option hidden disabled selected value></option>
                                                <option>Daily</option>
                                                <option>Weekly</option>
                                                <option>Monthly</option>
                                                <option>Rarely</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- cooking freq -->
                                    <div class="form-group row">
                                        <label for="CookingFreqSelector" class="col-sm-6 col-form-label">Frequency of preparing home-cooked meals:</label>
                                        <div class="col-sm-5">
                                            <select class="form-control" id="CookingFreqSelector" name="cookingFreq" required>
                                                <option hidden disabled selected value></option>
                                                <option>Daily</option>
                                                <option>Weekly</option>
                                                <option>Monthly</option>
                                                <option>Rarely</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- cooking exp -->
                                    <div class="form-group row ">
                                        <label for="difficulty" class="col-sm-4 col-form-label">Cooking experience:</label>
                                        <div class="col-sm-7">
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="difficulty" id="1" value="1" required>
                                                <label class="form-check-label" for="1">Very low</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="difficulty" id="2" value="2" required>
                                                <label class="form-check-label" for="2">Low</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="difficulty" id="3" value="3" required>
                                                <label class="form-check-label" for="3">Medium</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="difficulty" id="4" value="4" required>
                                                <label class="form-check-label" for="4">High</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="difficulty" id="5" value="5" required>
                                                <label class="form-check-label" for="5">Very High</label>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- user_cost -->
                                    <div class="form-group row ">
                                        <label for="user_cost" class="col-sm-4 col-form-label">Maximum cost of the recipe:</label>
                                        <div class="col-sm-7">
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="user_cost" id="user_cost1" value="1" required>
                                                <label class="form-check-label" for="1">Very low</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="user_cost" id="user_cost2" value="2" required>
                                                <label class="form-check-label" for="2">Low</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="user_cost" id="user_cost3" value="3" required>
                                                <label class="form-check-label" for="3">Medium</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="user_cost" id="user_cost4" value="4" required>
                                                <label class="form-check-label" for="4">High</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="user_cost" id="user_cost5" value="5" required>
                                                <label class="form-check-label" for="5">Not Important</label>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- user_time -->
                                    <div class="form-group row ">
                                        <label for="user_time" class="col-sm-6 col-form-label">Time Available for Cooking (max time in min. 0 = no constraints):
                                        </label>
                                        <div class="col-sm-5">
                                            <input type="number" value="0" id="user_time" name="user_time" min="0" max="200" step="10">
                                        </div>
                                    </div>

                                    <!-- goal -->
                                    <div class="form-group row">
                                        <label for="goalSelector" class="col-sm-6 col-form-label">What is your goal?</label>
                                        <div class="col-sm-5">
                                            <select class="form-control" id="goalSelector" name="goal" required>
                                                <option hidden disabled selected value></option>
                                                <option value="-1">Lose weight</option>
                                                <option value="1">Gain weight</option>
                                                <option value="0">No goals</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- Mood -->
                                    <div class="form-group row">
                                        <label for="moodSelector" class="col-sm-6 col-form-label">What is your mood right now?</label>
                                        <div class="col-sm-5">
                                            <select class="form-control" id="moodSelector" name="mood" required>
                                                <option hidden disabled selected value></option>
                                                <option>Good</option>
                                                <option>Neutral</option>
                                                <option>Bad</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- Activity -->
                                    <div class="form-group row">
                                        <label for="activitySelector" class="col-sm-6 col-form-label">How much physical activity do you do in a week?</label>
                                        <div class="col-sm-5">
                                            <select class="form-control" id="activitySelector" name="activity" required>
                                                <option hidden disabled selected value></option>
                                                <option value="high">A lot (> 9h)</option>
                                                <option value="medium">Average (&#x22cd; 6h)</option>
                                                <option value="low">Not enough (&lt; 3h)</option>
                                            </select>
                                        </div>
                                    </div>

                                    <!-- Sleep -->
                                    <div class="form-group row">
                                        <label for="sleepOption" class="col-sm-6 col-form-label">How many hours of sleep do you usually get?</label>
                                        <div class="col-sm-5">
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="sleepOption" id="sleepLow" value="low" required>
                                                <label class="form-check-label" for="sleepLow">&lt;8h</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="sleepOption" id="sleepHigh" value="high" required>
                                                <label class="form-check-label" for="sleepHigh">&ge;8h</label>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Stress -->
                                    <div class="form-group row">
                                        <label for="stressOption" class="col-sm-6 col-form-label">Do you feel stressed?</label>
                                        <div class="col-sm-5">
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="stressOption" id="stressYes" value="yes" required>
                                                <label class="form-check-label" for="stressYes">Yes</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="stressOption" id="stressNo" value="no" required>
                                                <label class="form-check-label" for="stressNo">No</label>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Depression -->
                                    <div class="form-group row">
                                        <label for="depressionOption" class="col-sm-6 col-form-label">Do you feel depressed?</label>
                                        <div class="col-sm-5">
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="depressionOption" id="depressionYes" value="yes" required>
                                                <label class="form-check-label" for="depressionYes">Yes</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input class="form-check-input" type="radio" name="depressionOption" id="depressionNo" value="no" required>
                                                <label class="form-check-label" for="depressionNo">No</label>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Restriction -->
                                    <!--
                                    <div class="form-group row">
                                        <label for="restriction" class="col-sm-6 col-form-label">Select your restriction</label>
                                        <div class="col-sm-5">
                                            <div class="form-check form-check-inline">
                                                <input id="vegetarian" name="vegetarian" type="checkbox">
                                                <label for="vegetarian">Vegetarian</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input id="lactose" name="lactose" type="checkbox">
                                                <label for="lactose">Lactose-free</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input id="gluten" name="gluten" type="checkbox">
                                                <label for="gluten">Gluten-free</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input id="nickel" name="nickel" type="checkbox">
                                                <label for="nickel">Low-Nickel</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                                <input id="light" name="light" type="checkbox">
                                                <label for="light">Light recipe</label>
                                            </div>
                                        </div>
                                    </div>
                                    -->

                                    <div class="form-group row">
                                        <label for="restriction" class="col-sm-6 col-form-label">Select your restriction</label>
                                        <div class="col-sm-5">
                                            <div class="form-check">
                                                <input id="diabetes" name="diabetes" type="checkbox">
                                                <label for="diabetes">Diabetes</label>
                                            </div>
                                            <div class="form-check">
                                                <input id="pregnant" name="pregnant" type="checkbox">
                                                <label for="pregnant">Pregnant or breastfeeding</label>
                                            </div>
                                            <div class="form-check">
                                                <input id="vegetarian" name="vegetarian" type="checkbox">
                                                <label for="vegetarian">Vegetarian</label>
                                            </div>
                                            <div class="form-check">
                                                <input id="lactose" name="lactose" type="checkbox">
                                                <label for="lactose">Lactose-free</label>
                                            </div>
                                            <div class="form-check">
                                                <input id="gluten" name="gluten" type="checkbox">
                                                <label for="gluten">Gluten-free</label>
                                            </div>
                                            <div class="form-check">
                                                <input id="nickel" name="nickel" type="checkbox">
                                                <label for="nickel">Low-Nickel</label>
                                            </div>
                                            <div class="form-check">
                                                <input id="light" name="light" type="checkbox">
                                                <label for="light">Light recipe</label>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Ingredients -->
                                    <div class="form-group row ">
                                        <div class="col-sm-6" style="padding-right : 0px; margin-right : 0px;">
                                            <label class="col-form-label">Write your favorite ingredients in max 50 characters(separated by a comma if there are more than one, for example "chicken, rice")</label>
                                        </div>
                                        <div class="col-sm-6">
                                            <input type="text" id="user_ingredients" name="user_ingredients" maxlength="40" size="40">
                                        </div>
                                    </div>

                                    <?php
                                    /* If the value of show expl show not 0 => start whith dish with explanations
                                    in recipes.php */
                                    if ($showExpl != 0)
                                    {
                                        $value = "main_exp";
                                    }
                                    else
                                    {
                                        $value = "main";
                                    }
                                    ?>
                                    <input type="hidden" name="dish" id="hiddenField" value="<?= $value ?>" />

                                    <br>
                                    <div class="col-md-8 offset-md-2 form-btn text-center">
                                        <button id="btnForm" class="btn btn-block btn-secondary btn-red col-md-4 offset-md-4 " type="submit" name="submit" >Build Profile</button>
                                        <small id="disclaimer" class="form-text text-muted">We'll use this data only for the purpose of the experiment</small>
                                    </div>
                                </form>

                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <?php include "php/footer.php"; ?>
        </div>
    </body>
</html>