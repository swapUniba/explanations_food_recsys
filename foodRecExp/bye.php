<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

/*
if(empty($_POST))
	header("location:index.php");

if(session_status() === PHP_SESSION_NONE)
	header("location:index.php");
*/

@session_start();
?>

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
                            <h2 class="section-title">Thank you!</h2>
                            <p class="section-sub-title">The experiment is ended, enjoy your meal! &#x1F355;</p>
							
							<?php 
								include "php/SaveToCsv.php";
								echo "This is the code to complete your experiment:<br />".$randomNumber;
							?>
                        </div>
                        <!-- End of Section Title -->
                        
                        <div class="col-md-12 contact-form-holder mt-4">
                            <a href="index.php">
								<button type="button" id="btnForm" class="btn btn-block btn-secondary btn-red col-md-4 offset-md-4" >Exit</button>
							</a>
                        </div>
                    </div>                    
                </div>
            </section>
            <?php include "php/footer.php"; ?>
        </div>
    </body>
</html>