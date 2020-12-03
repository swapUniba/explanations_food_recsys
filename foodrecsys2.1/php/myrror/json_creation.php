<?php 

	$email     = trim($_POST['email']);
    $password  = trim($_POST['password']);
    $token  = trim($_POST['token']);

    //Salvo il token nei cookie
    $cookie_name = "myrror";
	$cookie_email = $email;
	setcookie($cookie_name, $cookie_email, time() + (86400 * 30), "/"); // 86400 = 1 day

    $credenziali = "email=" . $email . "&password=" . $password;

	$response = queryMyrror("", $credenziali);
	$fp = fopen('fileMyrror/past_'. $email . ".json", 'w+');
	fwrite($fp, json_encode($response));
	fclose($fp);

	$today = date('Y-m-d');
	$response = queryMyrror("?fromDate=".$today,  $credenziali);
	$fp = fopen('fileMyrror/today_'. $email . ".json", 'w+');
	fwrite($fp, json_encode($response));
	fclose($fp);

	echo "ok";	//Risposta per identificare l'avvenuta creazione dei file



    function queryMyrror($param, $credenziali){

        $ch = curl_init();
        $json_data = null;

        curl_setopt($ch, CURLOPT_URL,"http://90.147.102.243:5000/auth/login");
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $credenziali);

        // Receive server response ...
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $server_output = curl_exec($ch);
        $result = json_decode($server_output,true);
        curl_close ($ch);

        // Further processing ...
        if ($server_output) {
             $token = $result['token'];
             $ch = curl_init();

            $headers =[
                "x-access-token:".$token
            ];

            curl_setopt($ch, CURLOPT_URL, "http://90.147.102.243:5000/api/profile/".$result['username'].$param);

            curl_setopt($ch, CURLOPT_POST, 0);
            curl_setopt($ch, CURLOPT_HEADER, 0);
            curl_setopt($ch, CURLOPT_HTTPHEADER,$headers);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);          

            $result2 = curl_exec($ch);
            //Decode JSON
            $json_data = json_decode($result2,true);

            curl_close ($ch);

            return $json_data;
        }

    }

?> 