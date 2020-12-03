$("#login").submit(function() {
    var email = $("#email").val();
    var password = $("#pass").val();


    $.ajax({
        type: "POST",
        url: "php/myrror/login.php",
        data: "email=" + email + "&password=" + password,
        dataType: "html",
        success: function(risposta) {
            console.log(risposta);

            //Quando le credenziali sono errate, viene rilasciata un token con 7 spazi vuoti
            if (risposta.length != 7) {
                var token = risposta; //Token utilizzato per effettuare le richieste

                caricaPagina(); //Inizia il caricamento della pagina fino a quando i file non sono stati creati

                //Se le credenziali sono corrette, creo i file json per la lettura
                $.ajax({
                    type: 'POST',
                    url: 'php/myrror/json_creation.php',
                    data: "email=" + email + "&password=" + password + "&token=" + token,
                    dataType: "html",
                    success: function(response) {
                        document.cookie = "myrror=" + email;
                        document.cookie = "myrrorDish=main";
                        if (response.localeCompare("ok") == 1) {
                            showPage(); //Termino il caricmaneto e mostro la pagina
                        }
                    }
                });


            } else {
                window.alert("Email o password errata");
            }


        },
        error: function() {
            alert("Chiamata fallita!");
        }
    });
    return false;
});

function caricaPagina() {
	  document.getElementById("loader").style.display = "inline";
	  //myVar = setTimeout(showPage, 3000);
}

function showPage() {
    document.getElementById("loader").style.display = "none";
    window.location.href = 'myrrorForm.php';
}