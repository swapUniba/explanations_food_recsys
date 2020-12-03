$(".messages").animate({
    scrollTop: $(document).height()
}, "fast");
var timestamp;
var imageURL;
var email;
var flagcitta = false;

function getEmail() {
    return email;
}

function getTimestampStart() {
    return timestampStart;
}

$("#profile-img").click(function() {
    $("#status-options").toggleClass("active");
});
/*
  $(".expand-button").click(function() {
    $("#profile").toggleClass("expanded");
  	$("#contacts").toggleClass("expanded");
  });

  $("#status-options ul li").click(function() {
  	$("#profile-img").removeClass();
  	$("#status-online").removeClass("active");
  	$("#status-away").removeClass("active");
  	$("#status-busy").removeClass("active");
  	$("#status-offline").removeClass("active");
  	$(this).addClass("active");

  	if($("#status-online").hasClass("active")) {
  		$("#profile-img").addClass("online");
  	} else if ($("#status-away").hasClass("active")) {
  		$("#profile-img").addClass("away");
  	} else if ($("#status-busy").hasClass("active")) {
  		$("#profile-img").addClass("busy");
  	} else if ($("#status-offline").hasClass("active")) {
  		$("#profile-img").addClass("offline");
  	} else {
  		$("#profile-img").removeClass();
  	};

  	$("#status-options").removeClass("active");
  });

   $("#toggle").unbind().click(function(){

var text = $(this).html();
if (text == "Disattiva modalità di debug"){
    $(this).css("background-color","red");
  $(this).html("Attiva modalità di debug");
  debug = false;
}else{
  $(this).css("background-color","green");
  $(this).html("Disattiva modalità di debug");
  debug = true;
}
//$(this).attr("disabled", true);

});
   */

$("#logout").click(function() {
    $.cookie("myrror" + getEmail(), null, {
        path: '/'
    });
    $.removeCookie('myrror' + getEmail(), {
        path: '/'
    });

});

function newMessage() {
    message = $(".message-input input").val();
    if ($.trim(message) == '') {
        return false;
    } else {
        timestamp = new Date().getUTCMilliseconds();

        timestampStart = Date.now(); //Utente invia il messaggio

        $('<li class="sent"><img src="' + imageURL + '" alt="" /><p id="quest' + timestamp + '"">' + message + '</p></li>').appendTo($('.messages ul'));
        $('.message-input input').val(null);
        $('.contact.active .preview').html('<span>Tu: </span>' + message);

        //Scroll verso il basso quando viene inviata una domanda
        $(".messages").animate({
            scrollTop: ($(document).height() * 100)
        }, "fast");

        return message;
    }

};

$(document).on("click", "button.submit", function() {
    //all the action
    $('button.submit').off('click');
    var query = newMessage();
    if (query == false) {
        return false;
    } else {
        send(query);
        return true;
    }

});

//Quando viene premuto 'invio' sulla tastiera
$(window).on('keydown', function(e) {
    if (e.which == 13) {
        let query = newMessage();
        send(query);

        return false;
    }
});

function send(query) {
    var text = query;

    if (flagcitta == true) {
        flagcitta = false;
        temp = $('#contesto').val();
        temp += " a " + text;
        text = temp;
    }
    var citta = getCity();
    var name = "myrror";

    var value = "; " + document.cookie;
    if (value.match(/myrror/)) {
        var parts = value.split("; " + name + "=");
        var tempStr = null;
        while (tempStr == null) {
            tempStr = parts.pop().split(";").shift();
            if (tempStr.match(/@/)) {
                //alert(tempStr);
            }
        }

    } else {
        window.location.href = 'index.html';
    }

    email = tempStr;

    if (text.match(/perchè/) || text.match(/spiegami/)) {
        var testo = $("#spiegazione").val();
        $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >' + testo + '</p></li>');

    } else if($('#intent').val() == 'Cibo' && (text.match == 'va bene'|| text.includes('procedimento') || text == 'consultare il procedimento' || text == "consultare")){
		
		
		
		var testo = $("#procedimento").val();
		$(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >' + testo + '</p></li>');

	}
    else if($('#intent').val() == 'Cibo' && (text.includes("un'altra ricetta") || text.includes("un altra ricetta") || text.includes("un'altra") ||text.includes("un altra") || text.includes("un altro"))){
        count = $("#count_ric").val();
        val = JSON.parse(decodeURIComponent($("#ric").val()));
        max = Object.keys( val.answer.recipes ).length
        
        if(count<max-1){
            count = parseInt(count, 10) + 1;
            $("#count_ric").val(count);
            
            procedimento = val.answer.recipes[count][26];
            $("#procedimento").val(procedimento);

            ingredients = val.answer.recipes[count][24];
            ingredients = ingredients.replace('[', '');
            ingredients = ingredients.replace(']', '');
            ingredients = ingredients.replace(/, /g, '<br>');

           // spiegazione = val.answer[0].explain;
           // $("#spiegazione").val(spiegazione);

            $(".chat").append(
                '<li class="replies">' + 
                    '<img src="immagini/chatbot.png" alt=""/>' +
                        '<p>Ti consiglio: <br>' +
                            '<b><a href="' + val.answer.recipes[count][0] + '" target="_blank">' + val.answer.recipes[count][1] + '</a></b><br>' +
                            val.answer.recipes[count][5] + '<br>' +
                            '<img style="width: 100%;height: 100%;" src="' + val.answer.recipes[count][4] + '">' +
                        '<br><br><b>Ingredienti:</b><br>' + ingredients +
                        "<br><br>Vuoi consultare il procedimento o guardare un'altra ricetta?" +
                        '</p>'+
                '</li>');
            
        }
        else{
            $("#intent").val("");
            $(".chat").append(
					'<li class="replies">' + 
						'<img src="immagini/chatbot.png" alt=""/>' +
							'<p>Non ci sono altre ricette</p>'+
					'</li>');
        }
        
        
    }
	  else {

        $("#intent").val("");
        if (text.match(/cambia/) || text.match(/cambio/) || text.match(/dammi un'altra/) || text.match(/leggi un'altra/) || text.match(/dammene un'altra/) || text.match(/leggine un'altra/) || text.match(/leggi altra news/) || text.match(/altra canzone/) || text.match(/dimmi un'altra/) || text.match(/riproducine un'altra/) || text.match(/cambia video/) || text.match(/fammi vedere un altro/) || text.match(/dammi un altro/) || text.match(/altro video/) || text.match(/altra canzone/) || text.match(/altra news/)) {

            text = $('#contesto').val();
        } else {
            if (flagcitta == false) {
                $('#contesto').val(text);
            }

        }
        $.ajax({
            type: "POST",
            url: "php/intentDetection.php",
            data: {
                testo: text,
                city: citta,
                mail: email
            },
            success: function(data) {
                setResponse(data);
            }
        });
    }

}

function setResponse(val) {

	$("#intent").val("");
    var string = val;
    console.log(val);

    if (/^[\],:{}\s]*$/.test(val.replace(/\\["\\\/bfnrtu]/g, '@').replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) {

        //the json is ok
        val = JSON.parse(val);

        var musicaSpotify = "Ecco qui la tua richiesta!";
        var spiegazione = "";
		var procedimento = "";
        var canzoneNomeSpotify = "Ecco qui la canzone richiesta!";
        var canzoneArtistaSpotify = "Ecco qui la canzone dell'artista richiesto!";
        var canzoneGenereSpotify = "Ecco una playlist di canzoni del genere richiesto!";
        var playlistEmozioniSpotify = "Ecco qui una playlist di canzoni raccomandata in base al tuo umore";
        var canzoneEmozioniSpotify = "Ecco qui un brano consigliato in base al tuo umore";
        var canzoniPersonalizzateSpotify = "Ecco qui un brano consigliato che potrebbe piacerti";
        var video = "Ecco qui il video richiesto";
        var ricetta = "Ecco una ricetta per te";

        if (val["intentName"] == "Interessi" || val["intentName"] == "Contatti" || val["intentName"] == "Esercizio fisico" || val["intentName"] == "Personalita") {

            $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p id="par' + timestamp + '">' + val["answer"] + '</p></li>');

        } else if (val["intentName"] == "attiva debug") {

            setDebug(true);
            $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >' + val["answer"] + '</p></li>');

        } else if (val["intentName"] == "disattiva debug") {
            setDebug(false);
            $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >' + val["answer"] + '</p></li>');

        } else if (val['intentName'] == "Musica") {

            if (val['answer']['explain'] != "") {
                spiegazione = val['answer']['explain'];
                $("#spiegazione").val(spiegazione);
                //$(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p id="par'+timestamp+'"> "<br>"' + musicaSpotify + '&#x1F603;' +'<br>'+ '<iframe src="' + val['answer']['url'] + '" width="250" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe></p></li>');
            }
            $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p id="par' + timestamp + '">' + musicaSpotify + '&#x1F603;' + '<br>' + '<iframe src="' + val['answer']['url'] + '" width="250" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe></p></li>');

        } else if (val["intentName"] == "News") {

            if (val['answer'] == "") {
                $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p> sfortunatamente non sono stati trovati articoli a riguardo</p></li>');
            } else {
                if (val['answer']['explain'] != undefined && val['answer']['explain'] != null) {
                    spiegazione = val['answer']['explain'];
                    $("#spiegazione").val(spiegazione);
                    // $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p id="par'+timestamp+'"> ' + spiegazione + '<br><img style="width: 100%;height: 100%;" src= "'+val['answer']['image']+'"/><a href="'+val['answer']['url']+'">'+val["answer"]['title']+'</a></p></li>');

                }
                $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p id="par' + timestamp + '"><img style="width: 100%;height: 100%;" src= "' + val['answer']['image'] + '"/><a id="nw' + timestamp + '" class="news" target="_blank" href="' + val['answer']['url'] + '">"' + val["answer"]['title'] + '"</a></p></li>');
                $(".chat").append('<input value="false" type="hidden" id= "flagNews' + timestamp + '" >')
            }

        } else if (val["intentName"] == "Video in base alle emozioni" || val["intentName"] == "Ricerca Video") {

            $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p id="par' + timestamp + '">' + video + ' &#x1F603; <br>' + '<iframe id="ytplayer" type="text/html" width="260" height="260" src="' + val['answer']['ind'] + '" frameborder="0" allowfullscreen/></iframe></p></li>');
            if (val['answer']['explain'] != undefined && val['answer']['explain'] != null) {
                $('#spiegazione').val(val['answer']['explain']);

            }

        } else if (val["intentName"] == "meteo binario") {

            if (val['answer']['city'] == undefined) {
                $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >Inserisci la città</p></li>');
                flagcitta = true;
                $(".messages").animate({
                    scrollTop: ($(document).height() * 100)
                }, "fast");
            } else {
                $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >' + val['answer']['res'] + '</p></li>');
            }

        } else if ((val["intentName"] == "Meteo") && val['confidence'] > 0.60) {

            if (val['answer']['city'] == undefined) {
                $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >Inserisci la città</p></li>');
                flagcitta = true;
                $(".messages").animate({
                    scrollTop: ($(document).height() * 100)
                }, "fast");
            }
            var json = val['answer']['res'];

            if (json == "") {
                $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >Sfortunatamente non sono disponibili dati riguardanti il periodo indicato</p></li>');

            } else {
                var res = json.split("<br>");
                var str = res[0].split(";");

                var imglink = "";

                switch (str[3]) {

                    case 'cielo sereno':
                        imglink = "icon-2.svg";
                        break;

                    case 'poco nuvoloso':
                        imglink = "icon-1.svg";
                        break;

                    case 'parzialmente nuvoloso':
                        imglink = "icon-7.svg";
                        break;

                    case 'nubi sparse':
                        imglink = "icon-6.svg";
                        break;

                    case 'pioggia leggera':
                        imglink = "icon-4.svg";
                        break;

                    case 'nuvoloso':
                        imglink = "icon-5.svg";
                        break;

                    case 'piogge modeste':
                        imglink = "icon-9.svg";
                        break;

                    case 'pioggia pesante':
                        imglink = "icon-11.svg";
                        break;

                    case 'neve leggera':
                        imglink = "icon-13.svg";
                        break;

                    case 'neve':
                        imglink = "icon-14.svg";
                        break;

                }

                $(".chat").append( //'<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'+
                    '<li id="par' + timestamp + '" class="replies"><img src="immagini/chatbot.png" alt="" /><div class="container">' +
                    '<div class="forecast-container" id= "f' + timestamp + '"><div class="today forecast">' +
                    '<div class="forecast-header"><div class="day">' + str[0] + '</div></div>' +
                    '<div class="forecast-content"><div class="location">' + val['answer']['city'] + ' Ore ' + str[1] + '</div><div class="degree">' +
                    '<div class="num">' + Math.trunc(str[2]) + '<sup>o</sup>C</div><div class="forecast-icon">' +
                    '<img src="immagini/icons/' + imglink + '" alt="" style="width:90px;"> </div></div>' +
                    '</div></div></div></div></li>'
                    //+'<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'
                );

                str = null;
                for (var i = 1; i < res.length - 1; i++) {

                    var str = res[i].split(";");
                    var imglink = "";

                    switch (str[3]) {

                        case 'cielo sereno':
                            imglink = "icon-2.svg";
                            break;

                        case 'poco nuvoloso':
                            imglink = "icon-1.svg";
                            break;

                        case 'parzialmente nuvoloso':
                            imglink = "icon-7.svg";
                            break;

                        case 'nubi sparse':
                            imglink = "icon-6.svg";
                            break;

                        case 'pioggia leggera':
                            imglink = "icon-4.svg";
                            break;

                        case 'nuvoloso':
                            imglink = "icon-5.svg";
                            break;

                        case 'piogge modeste':
                            imglink = "icon-9.svg";
                            break;

                        case 'pioggia pesante':
                            imglink = "icon-11.svg";
                            break;

                        case 'neve leggera':
                            imglink = "icon-13.svg";
                            break;

                        case 'neve':
                            imglink = "icon-14.svg";
                            break;

                    }

                    $('#f' + timestamp).append('<div class="forecast">' +
                        '<div class="forecast-header"><div class="day">' + str[1] + '</div>' +
                        '</div><div class="forecast-content"> <div class="forecast-icon">' +
                        '<img src="immagini/icons/' + imglink + '" alt="" style="width:40px;"></div>' +
                        '<div class="degree">' + Math.trunc(str[2]) + '<sup>o</sup>C</div></div></div>');

                }
            }
        } else if (val["intentName"] == "Cibo") {
            $("#intent").val("Cibo");
            $("#count_ric").val(1);
            
			if(typeof val['answer']['name'] !== 'undefined'){
                $(".chat").append(
					'<li class="replies">' + 
						'<img src="immagini/chatbot.png" alt=""/>' +
							'<p>' + val['answer']['name'] +
							'</p>'+
					'</li>');
            }
            else{
                $("#ric").val(encodeURIComponent(JSON.stringify(val)));
                
				procedimento = val.answer.recipes[0][26];
				$("#procedimento").val(procedimento);
				
				ingredients = val.answer.recipes[0][24];
				ingredients = ingredients.replace('[', '');
				ingredients = ingredients.replace(']', '');
				ingredients = ingredients.replace(/, /g, '<br>');
                
                spiegazione = val.answer.explain;
                $("#spiegazione").val(spiegazione);
				
				$(".chat").append(
					'<li class="replies">' + 
						'<img src="immagini/chatbot.png" alt=""/>' +
							'<p>Ti consiglio: <br>' +
								'<b><a href="' + val.answer.recipes[0][0] + '" target="_blank">' + val.answer.recipes[0][1] + '</a></b><br>' +
								val.answer.recipes[0][5] + '<br>' +
								'<img style="width: 100%;height: 100%;" src="' + val.answer.recipes[0][4] + '">' +
							'<br><br><b>Ingredienti:</b><br>' + ingredients +
							"<br><br>Vuoi consultare il procedimento o guardare un'altra ricetta?" +
							'</p>'+
					'</li>');
                
                
			}
			
        } else {
            $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p id="par' + timestamp + '">' + val["answer"] + '</p></li>');
        }

        if (val['intentName'] == "Default Welcome Intent") {

        } else if (isDebugEnabled()) {
            var risposta = val['answer'];
            risposta = risposta.toString().toLowerCase();
            if (val['confidence'] < 0.6 || risposta.includes('riprova') || risposta.includes('sfortunatamente') || risposta.includes('purtroppo') || risposta == "") {

                var testo = $("#hide" + timestamp).text();
                var mail = getEmail();
                var question = $("#quest" + timestamp).text();
                //var timestampStart = getTimestampStart();
                var timestampEnd = Date.now();
                rating(testo, question, 'no', mail, timestampStart, timestampEnd, "");
            } else {
                $('#par' + timestamp).append('<div class="rating-box"><h4>Sei soddisfatto della risposta?</h4><button id="yes' + timestamp + '" class="btn-yes">SI</button>' +
                    '<button id="no' + timestamp + '" class="btn-no">NO</button></div>');

            }

            $(".chat").append('<p hidden id="hide' + timestamp + '" >' + string + '<p/>');
        }

    } else {
        //the json is not ok
        $(".chat").append('<li class="replies"><img src="immagini/chatbot.png" alt="" /><p >Non ho capito cosa vuoi dire. Prova a riformulare la tua domanda!</p></li>');

    }

    $(".messages").animate({
        scrollTop: ($(document).height() * 100)
    }, "fast");

}

//Intent avviato all'inizio del dialogo per mostrare la frase di benvenuto e per impostare il nome dell'utente nella schermata
function welcomeIntent() {
    send("aiuto");
    var value = "; " + document.cookie;
    if (value.match(/myrror/)) {
        var parts = value.split("; " + name + "=");
        var tempStr = null;
        while (tempStr == null) {
            tempStr = parts.pop().split(";").shift();
            if (tempStr.match(/@/)) {
                //alert(tempStr);
            }
        }

    } else {
        window.location.href = 'index.html';
    }
    setProfileImg(tempStr);
    setNominativo(tempStr); //Nome per la grafica del sito

}

function setProfileImg(email) {

    $.ajax({
        type: "POST",
        url: "php/getProfileImage.php",
        data: {
            mail: email
        },
        success: function(data) {
            imageURL = data;
            $('#profile-img').attr('src', imageURL);
        }
    });

}

//Funzione usata per impostare il nome dell'utente nella schermata
function setNominativo(tempStr) {
    $.ajax({
        type: "POST",
        url: "php/setNominativo.php",
        data: {
            mail: tempStr
        },
        success: function(data) {
            console.log(data);
            $(".nomeUtente").append(data);
        }
    });
}

$("ul.chat").on("click", "a.news", function(evnt) {

    var id = $(this).attr("id");
    id = id.substr(2, timestamp.length);

    $("#flagNews" + id).val("true");
    //alert("clicked");
    //return false;
});

$("#logout").click(function() {
    window.location.href = 'index.html';
});