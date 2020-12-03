<?php
	//setta l'expiration date del cookie con un ora nel passato, eliminandolo nel caso sia settato (login con myrror)
	setcookie('myrror', '', time() - 3600);
	setcookie('myrrorDish', '', time() - 3600);
	
	$answers = "";
	
	if(isset($_POST['Q1']))
		$answers = $answers . $_POST['Q1'] . ',';
	
	if(isset($_POST['Q2']))
		$answers = $answers . $_POST['Q2'] . ',';
	else 
		$answers = $answers . ',';

	if(isset($_POST['Q3']))
		$answers = $answers . $_POST['Q3'] . ',';
	else 
		$answers = $answers . ',';

	if(isset($_POST['Q4']))
		$answers = $answers . $_POST['Q4'] . ',';
	else 
		$answers = $answers . ',';

	if(isset($_POST['Q5']))
		$answers = $answers . $_POST['Q5'] . ',';
	else 
		$answers = $answers . ',';
									 
	if(isset($_POST['Q6']))
		$answers = $answers . $_POST['Q6'] . ',';
	else 
		$answers = $answers . ',';

	if(isset($_POST['Q7']))
		$answers = $answers . str_replace(",", " ", $_POST['Q7']);
	
	if(isset($_POST['prevDish']))
		$_SESSION['answers'][$_POST['prevDish']] = $answers;
    
	$tocsv = $_SESSION['profile'];
	
	foreach($_SESSION['answers'] as $answer) {
		$tocsv = $tocsv . $answer;
	}
	
    
	$randomNumber = rand(1000000,9999999);
	$tocsv = $tocsv . "," . $randomNumber;
        
	if(file_put_contents('results/explResults.csv', $tocsv.PHP_EOL , FILE_APPEND | LOCK_EX)){
		session_destroy();
	}
	
?>