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


session_start();

?>

<!DOCTYPE html>
<html lang="en">
    <?php include "php/head.php"; ?>
    <body data-spy="scroll" data-target="#navbar-nav-header" class="single-layout">		
        <?php
			
			include "php/requestFunctions.php";
			
			$postPage = 'action="recipes.php"';
			$answers = '';
					
			//Se nel Post e' presente la variabile dish, vuol dire che non e' stato effettuato l'accesso con myrror, oppure le ricette sono state gia' salvate in $data (quindi stiamo visualizzando un secondo o un dolce)
			if(isset($_POST['dish'])){
				include "php/noMirrorLogin.php";
			}
			//se non si trova la variabile dish vuol dire che abbiamo effettuato l'accesso con myrror, quindi dobbiamo caricare le ricette personalizzate
			else{
				include "php/mirrorLogin.php";
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
												<p><font color="black"><?= $explanations[$dish][$typeOfExp] ?></font></p>
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