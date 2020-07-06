<!DOCTYPE html>
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
                                        <label for="sexOption" class="col-sm-6 col-form-label"><b>You are a:</b></label>
                                        <div class="col-sm-6">
                                            <div class="table-rdb">
												<div class="row-rdb">
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="sexOption" id="male" value="m" required>
														<label class="form-check-label" for="male">Male</label>
													</div>
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="sexOption" id="female" value="f" required>
														<label class="form-check-label" for="female">Female</label>
													</div>
												</div>
												<div class="row-rdb">
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="sexOption" id="notsay" value="na" required>
														<label class="form-check-label" for="notsay">Prefer not to say</label>
													</div>
													<div class="cell-rdb">
													</div>
												</div>
											</div>
                                        </div>                                        
									</div>                                        
									<div class="form-group row">
                                        <label for="age" class="col-sm-6 col-form-label"><b>Your age is:</b></label>
                                        <div class="col-sm-6" style="padding-right : 0px; margin-right : 0px;">
                                            <div class="table-rdb">
												<div class="row-rdb">
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="age" id="<25" value="<25" required>
														<label class="form-check-label" for="<25">&lt;25</label>
													</div>
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="age" id="25-35" value="25-35" required>
														<label class="form-check-label" for="25-35">25-35</label>
													</div>
												</div>
												<div class="row-rdb">
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="age" id="35-45" value="35-45" required>
														<label class="form-check-label" for="35-45">36-45</label>
													</div>
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="age" id="45-55" value="45-55" required>
														<label class="form-check-label" for="45-55">46-55</label>
													</div>
												</div>
												<div class="row-rdb">
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="age" id="55-65" value="55-65" required>
														<label class="form-check-label" for="55-65">56-65</label>
													</div>
													<div class="cell-rdb">
														<input class="form-check-input" type="radio" name="age" id=">65" value=">65" required>
														<label class="form-check-label" for=">65">&gt;65</label>
													</div>
												</div>
											</div>
										</div>
									</div>
									
									<!-- Health lifestyle -->
                                    <div class="form-group row">
										<div class="col-sm-6">
											<label class="col-form-label"><b>In your opinion, to have a healthy lifestyle is:</b></label>
										</div>
										<div class="col-sm-6">
											<select class="form-control" id="HLselector" name="HS">
												<option hidden disabled selected value></option><option>Not important</option>
												<option>Poorly important</option>
												<option>Important</option>
												<option>Very important</option>
											</select>
										</div>
									</div>
									
									<!-- health conditions -->
									<div class="form-group row">
										<div class="col-sm-6">
											<label class="col-form-label"><b>How do you consider your lifestyle:</b></label>
										</div>
										<div class="col-sm-6">
											<select class="form-control" id="HCselector" name="HC">
												<option hidden disabled selected value></option>
												<option>Absolutely not healthy</option>
												<option>Not healthy</option>
												<option>Quite healty</option>
												<option>Healty</option>
												<option>Very healty</option>
											</select>
										</div>
									</div>
									
									<!-- healthy food choice -->
									<div class="form-group row">
										<div class="col-sm-6">
											<label class="col-form-label"><b>I try to make healthy food choices every day:</b></label>
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
										<div class="col-sm-6">
											<label class="col-form-label"><b>I look at the nutritional value of food products I buy:</b></label>
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
                                        <label for="BMIselector" class="col-sm-6 col-form-label"><b>Your fat class is:</b></label>
                                        <div class="col-sm-6">
                                            <select class="form-control" id="BMIselector" name="BMI" required>
                                                <option hidden disabled selected value></option>
                                                <option >Underweight (BMI &lt;19&#46;0)</option>
                                                <option >Standard Weight (BMI 19&#45;22&#46;9)</option>
                                                <option >Overweight (BMI 23&#46;0&#45;24&#46;9)</option>
                                                <option >Class I obesity (BMI 25&#46;0&#45;29&#46;9)</option>
                                                <option >Class II obesity (BMI &ge;30&#46;0)</option>
                                            </select>
                                        </div>
                                    </div>
                                   
                                   <!-- Employment -->
                                    <div class="form-group row">
                                        <label for="occupationSelector" class="col-sm-6 col-form-label"><b>Employment:</b></label>
                                        <div class="col-sm-6">
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
                                        <label for="websiteUsageSelector" class="col-sm-6 col-form-label"><b>Recipe website usage:</b></label>
                                        <div class="col-sm-6">
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
                                        <label for="CookingFreqSelector" class="col-sm-6 col-form-label"><b>Frequency of preparing home-cooked meals:</b></label>
                                        <div class="col-sm-6">
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
                                        <label for="exp" class="col-lg-5 col-form-label"><b>Cooking experience:</b></label>
                                        <div class="col-lg-7 rdb-cook-exp">
                                            <div class="form-check form-check-inline">
                                              <input class="form-check-input" type="radio" name="exp" id="1" value="1" required>
                                              <label class="form-check-label" for="1">Very low</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                              <input class="form-check-input" type="radio" name="exp" id="2" value="2" required>
                                              <label class="form-check-label" for="2">Low</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                              <input class="form-check-input" type="radio" name="exp" id="3" value="3" required>
                                              <label class="form-check-label" for="3">Medium</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                              <input class="form-check-input" type="radio" name="exp" id="4" value="4" required>
                                              <label class="form-check-label" for="4">High</label>
                                            </div>
                                            <div class="form-check form-check-inline">
                                              <input class="form-check-input" type="radio" name="exp" id="5" value="5" required>
                                              <label class="form-check-label" for="5">Very High</label>
                                            </div>
                                        </div>
                                   </div>
                                   
                                   <!-- goal -->
                                    <div class="form-group row">
                                        <label for="goalSelector" class="col-sm-6 col-form-label"><b>What is your goal?</b></label>
                                        <div class="col-sm-6">
                                            <select class="form-control" id="goalSelector" name="goal" required>
                                                <option hidden disabled selected value></option>
                                                <option>Lose weight</option>
                                                <option>Gain weight</option>
                                                <option>No goals</option>
                                            </select>
                                        </div>
                                    </div>

                                   

                                    <!-- Mood -->
                                    <div class="form-group row">
                                        <label for="moodSelector" class="col-sm-6 col-form-label"><b>What is your mood right now?</b></label>
                                        <div class="col-sm-6">
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
                                        <label for="activitySelector" class="col-sm-6 col-form-label"><b>How much physical activity do you do in a week?</b></label>
                                        <div class="col-sm-6">
                                            <select class="form-control" id="activitySelector" name="activity" required>
                                                <option hidden disabled selected value></option>
                                                <option value="high">A lot (> 9h)</option>
                                                <option value="no">Average (&#x22cd; 6h)</option>
                                                <option value="low">Not enough (&lt; 3h)</option>
                                            </select>
                                        </div>
                                    </div>
                                    
                                    <!-- Sleep -->
                                    <div class="form-group row">
                                        <label for="sleepOption" class="col-sm-6 col-form-label"><b>How many hours of sleep do you usually get?</b></label>
                                        <div class="col-sm-6">
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
                                        <label for="stressOption" class="col-sm-6 col-form-label"><b>Do you feel stressed?</b></label>
                                        <div class="col-sm-6">
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
                                        <label for="depressionOption" class="col-sm-6 col-form-label"><b>Do you feel depressed?</b></label>
                                        <div class="col-sm-6">
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
									
									<!-- health conditions lists -->
									<div class="form-group row">
										<div class="col-lg-5">
											<label class="col-form-label"><b>Indicate your health conditions:</b></label>
										</div>
										<div class="col-lg-7">
											<div class="table-chkbox">
												<div class="row-chkbox">
													<div class="cell-chkbox">
														<input id="heart" name="heart" type="checkbox">
														<label for="heart">Heart Problems</label>
													</div>
													<div class="cell-chkbox">
														<input id="pressure" name="pressure" type="checkbox">
														<label for="pressure">High blood pressure</label>
													</div>
												</div>
												<div class="row-chkbox">
													<div class="cell-chkbox">
														<input id="diabete" name="diabete" type="checkbox">
														<label for="diabete">Diabete</label>
													</div>
													<div class="cell-chkbox">
														<input id="cholesterol" name="cholesterol" type="checkbox">
														<label for="cholesterol">High cholesterol</label>
													</div>
												</div>
												<div class="row-chkbox">
													<div class="cell-chkbox">
														<input id="joint" name="joint" type="checkbox">
														<label for="joint">Joint Pains (articulations)</label>
													</div>
												</div>
											</div>
										</div>
									</div>
                                    
                                    <!-- Restriction -->
                                    <div class="form-group row">
                                        <label for="restriction" class="col-lg-5 col-form-label"><b>Select your restriction</b></label>
                                        <div class="col-lg-7">
                                            <div class="table-chkbox">
												<div class="row-chkbox">
													<div class="cell-chkbox">
														<input id="vegetarian" name="vegetarian" type="checkbox">
														<label for="vegetarian">Vegetarian</label>
													</div>
													<div class="cell-chkbox">
														<input id="lactose" name="lactose" type="checkbox">
														<label for="lactose">Lactose-free</label>
													</div>
												</div>
												<div class="row-chkbox">
													<div class="cell-chkbox">
															<input id="gluten" name="gluten" type="checkbox">
															<label for="gluten">Gluten-free</label>
													</div>
													<div class="cell-chkbox">
															<input id="nickel" name="nickel" type="checkbox">
															<label for="nickel">Low-Nickel</label>
													</div>
												</div>
												<div class="row-chkbox">
													<div class="cell-chkbox">
														<input id="light" name="light" type="checkbox">
														<label for="light">Light recipe</label>
													</div>
												</div>
											</div>
                                        </div>
                                    </div>
                                   
                                   <input type="hidden" name="dish" id="hiddenField" value="main" />

                                    <br>
                                    <div class="col-md-8 offset-md-2 form-btn text-center">
                                        <button id="btnForm" class="btn btn-block btn-secondary btn-red col-md-4 offset-md-4 " type="submit">Build Profile</button>
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