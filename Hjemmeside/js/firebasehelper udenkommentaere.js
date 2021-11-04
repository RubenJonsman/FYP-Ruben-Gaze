
  var firebaseConfig = {
    apiKey: "AIzaSyBi1tESo_D2t7EuggM0SapHL-VJMNXdHwI",
    authDomain: "eyetracking-1e270.firebaseapp.com",
    databaseURL: "https://eyetracking-1e270.firebaseio.com",
    projectId: "eyetracking-1e270",
    storageBucket: "eyetracking-1e270.appspot.com",
    messagingSenderId: "559260982105",
    appId: "1:559260982105:web:cec01c79bf2c0ba99f0a48"
  };

  firebase.initializeApp(firebaseConfig);


  var firebaseValue = firebase.database().ref();

  function SetWord(){

    firebaseValue.on('value', function(snapshot){

    var message = snapshot.child("MessageData").val();


    var messageZero = snapshot.child("MessageData/0").val();


    if(message.length != 0){

      console.log(message)

      document.getElementById("wordTxt").innerHTML = message.replace(/\-/g, "&nbsp").replace(/\'/g, "").replace(/\[/g, "").replace(/\]/g, "").toString();


    }

    else{

      console.log(messageZero)

      document.getElementById("wordTxt").innerHTML = messageZero.replace(/\-/g, "&nbsp").replace(/\'/g, "").replace(/\[/g, "").replace(/\]/g, "").toString();

    }

    })
}


function SetList(){

  var firebaseValue = firebase.database().ref();

  firebaseValue.on('value', function(snapshot){

  var word_list = snapshot.child("WordListData").val();

  console.log(word_list)

  if(word_list.length != 0){
    document.getElementById("wl1Txt").innerHTML = word_list.slice(0, Math.round(word_list.length/2));
    document.getElementById("wl2Txt").innerHTML = word_list.slice(Math.round(word_list.length/2), word_list.length);
  }
  })
}

SetWord();
SetList();

