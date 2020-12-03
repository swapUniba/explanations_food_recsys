<?php

function queryMyrror($param){

	$json = null;

	if (isset($_COOKIE['myrror'])) {
	  	$email = $_COOKIE['myrror'];
    
        if($param == "today"){
            $json = file_get_contents("fileMyrror/today_" . $email . ".json", FILE_USE_INCLUDE_PATH);
        }else{
            $json = file_get_contents("fileMyrror/past_" . $email . ".json", FILE_USE_INCLUDE_PATH);
        }
        $result = json_decode($json,true);

        return $result;

	}else{
		echo "<script>location.href='index.html';</script>";

	}
	

}


?>