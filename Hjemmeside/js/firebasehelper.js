// Konfiguration af firebase database
  var firebaseConfig = {
    apiKey: "AIzaSyBi1tESo_D2t7EuggM0SapHL-VJMNXdHwI",
    authDomain: "eyetracking-1e270.firebaseapp.com",
    databaseURL: "https://eyetracking-1e270.firebaseio.com",
    projectId: "eyetracking-1e270",
    storageBucket: "eyetracking-1e270.appspot.com",
    messagingSenderId: "559260982105",
    appId: "1:559260982105:web:cec01c79bf2c0ba99f0a48"
  };


  // Initatilisering af firebase
  firebase.initializeApp(firebaseConfig);

  // Definere databasen
  var firebaseValue = firebase.database().ref();


// Funktion: henter de bogstaver, som brugeren har indtastet, ned fra databasen og viser dem på hjemmesiden.
  function SetWord(){

    // Fortæller, at vi skal hente dataene ned fra databasen
    firebaseValue.on('value', function(snapshot){
      
    // Henter dataene fra kolonnen ved navn MessageData
    var message = snapshot.child("MessageData").val();
    // Henter dataene fra kolonnen 0 der ligger inden under databasen
    var messageZero = snapshot.child("MessageData/0").val();

    /*
    Grunden til, at vi har to variabler, der henter data ned fra to forskellige kolonner er,
    at de første bogstav som brugeren skriver ikke kommer som en liste, men derimod en String.
    Grunden til dette er, at firebase laver listen om til en string
    Dog ændre dette sig, når brugeren har skrevet to bogstaver, da vi her har en liste med 2 lister indeni.
    */

    // Hvis brugeren har skrevet 2 eller flere bogstaver indsættes i på hjemmesiden.
    if(message.length != 0){

      // printer bogstaverne i konsollen
      console.log(message)
      


      // Vi fjerner alle tilfælde af [, ] og ' da bogstaverne kommer som en liste og ikke en string. KILDE: //https://v8.dev/features/string-replaceall 
      // Da vi har valgt, at "-" skal symbolisere mellemrum, erstattes dette tegn med mellemrum(&nbsp)
      document.getElementById("wordTxt").innerHTML = message.replace(/\-/g, "&nbsp").replace(/\'/g, "").replace(/\[/g, "").replace(/\]/g, "").toString();


    }

    else{
      // Printer bogstavet i konsollen
      console.log(messageZero)

      // Vi fjerner alle tilfælde af "[", "]" og "'" da bogstaverne kommer som en liste og ikke en string.
      // Da vi har valgt, at "-" skal symbolisere mellemrum, erstattes dette tegn med mellemrum(&nbsp)
      document.getElementById("wordTxt").innerHTML = messageZero.replace(/\-/g, "&nbsp").replace(/\'/g, "").replace(/\[/g, "").replace(/\]/g, "").toString();

    }

    })
}


// Funktion: henter ordlisten ned fra databasen og viser den på hjemmesiden.
function SetList(){
  // Definere, hvilken database vi referere til
  var firebaseValue = firebase.database().ref();

  // Fortæller, at vi skal hente dataene ned fra databasen
  firebaseValue.on('value', function(snapshot){

  // Henter dataene fra kolonnen ved navn WorldListData
  var word_list = snapshot.child("WordListData").val();

  // Printer ordlisten
  console.log(word_list)

  // Hvis længden på listen ikke er 0, opdeles listen i to, og indsættes på hjemmesiden.
  if(word_list.length != 0){
    document.getElementById("wl1Txt").innerHTML = word_list.slice(0, Math.round(word_list.length/2));
    document.getElementById("wl2Txt").innerHTML = word_list.slice(Math.round(word_list.length/2), word_list.length);
  }
  })
}

// Kører funktionerne
SetWord();
SetList();

