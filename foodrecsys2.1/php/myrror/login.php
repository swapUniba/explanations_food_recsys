<?php

    //Recupero email e password
    $email      = trim($_POST['email']);
    $password  = trim($_POST['password']);

    //Url per inviare la richiesta POST
    $url = 'http://90.147.102.243:5000/auth/login';

    //Dati da inviare nella richiesta
    $fields = [
        'email' => $email,
        'password' => $password
    ];

    //url-ify the data for the POST
    $fields_string = http_build_query($fields);

    //open connection
    $ch = curl_init();

    //set the url, number of POST vars, POST data
    curl_setopt($ch,CURLOPT_URL, $url);
    curl_setopt($ch,CURLOPT_POST, true);
    curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);

    //So that curl_exec returns the contents of the cURL; rather than echoing it
    curl_setopt($ch,CURLOPT_RETURNTRANSFER, true); 

    //Esecuzione post
    $result = curl_exec($ch);

    //Decodifico il json
    $json = json_decode($result);

    $auth = $json -> auth; //Flag per verificare se si è ottenuto l'accesso

    if ($auth == 1) {//Credenziali corrette
        $token = $json -> token;
        echo $token;
    }else{
        echo ""; //Credenziali errate
    }


?>

					