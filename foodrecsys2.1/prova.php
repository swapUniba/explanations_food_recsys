<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$url = "http://localhost:5003/exp/?mood=neutral&stress=no&depression=no&bmi=over&activity=low&goal=lose&sleep=low&restr=glutenfree&imgurl1=https%3A%2F%2Fwww.giallozafferano.it%2Fimages%2Fricette%2F201%2F20113%2Ffoto_hd%2Fhd650x433_wm.jpg&imgurl2=https%3A%2F%2Fwww.giallozafferano.it%2Fimages%2Fricette%2F176%2F17635%2Ffoto_hd%2Fhd650x433_wm.jpg&difficulty=5";

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

echo($url);

echo("<hr />");
var_dump($result);

echo("<hr />");
echo(json_decode($result));

echo("<hr />");
$varAppo = json_decode(json_decode($result),true);
print_r($varAppo['explanation']);

?>