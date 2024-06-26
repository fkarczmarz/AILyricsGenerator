// Initialize Firebase
var firebaseConfig = {
  apiKey: "AIzaSyC4CclwR1NAHNU4HFxuFAC7URg7msWhBBU",
  authDomain: "ai-lyrics-generator-v1.firebaseapp.com",
  projectId: "ai-lyrics-generator-v1",
  storageBucket: "ai-lyrics-generator-v1.appspot.com",
  messagingSenderId: "221274510140",
  appId: "1:221274510140:web:d8fb0cd157b53b6ff08439",
  measurementId: "G-TYCG4RSKBK",
};

firebase.initializeApp(firebaseConfig);

var db = firebase.firestore();
var ui = new firebaseui.auth.AuthUI(firebase.auth());

var uiConfig = {
  callbacks: {
    signInSuccessWithAuthResult: function (authResult, redirectUrl) {
      $("#loginSection").hide();
      $("#generateSection").show();
      $("#userDetails").text(`Logged in as: ${authResult.user.email}`);
      renderSavedLyrics(authResult.user.uid);
      return false;
    },
    uiShown: function () {
      document.getElementById("loader").style.display = "none";
    },
  },
  signInFlow: "popup",
  signInOptions: [firebase.auth.GoogleAuthProvider.PROVIDER_ID],
  tosUrl: "https://www.example.com/terms-of-service",
  privacyPolicyUrl: "https://www.example.com/privacy-policy",
};

ui.start("#firebaseui-auth-container", uiConfig);

function renderSavedLyrics(userId) {
  firebase
    .firestore()
    .collection("lyrics")
    .where("userId", "==", userId)
    .get()
    .then((querySnapshot) => {
      var savedLyricsList = $("#savedLyricsList");
      savedLyricsList.empty();
      querySnapshot.forEach((doc) => {
        var lyricsData = doc.data();
        var listItem = `
                    <li style="display: flex; align-items: center; justify-content: space-between;">

                        <a href="javascript:goToLyricsDetails('${
                          doc.id
                        }')" class="lyrics-link">${lyricsData.title}</a>

                        <div style="display: flex; gap: 7px;"> <div onclick="markAsFavorite('${
                          doc.id
                        }', ${!lyricsData.favorite})">${
          lyricsData.favorite
            ? ' <i class="fa fa-star" style="font-size:20px; color: gold; cursor: pointer;"></i>'
            : ' <i class="fa fa-star-o" style="font-size:20px; cursor: pointer;"></i>'
        }</div>
         
                     <i class="fa fa-trash-o" onclick="deleteLyrics('${
                       doc.id
                     }')" style="font-size:20px; cursor: pointer;"></i></div>



                       


                    </li>`;
        savedLyricsList.append(listItem);
      });
    });
}

function goToLyricsDetails(docId) {
  window.location.href = `/lyrics/${docId}`;
}

function markAsFavorite(docId, favoriteStatus) {
  var user = firebase.auth().currentUser;
  if (!user) {
    return;
  }

  db.collection("lyrics")
    .doc(docId)
    .update({
      favorite: favoriteStatus,
    })
    .then(() => {
      renderSavedLyrics(user.uid);
    })
    .catch((error) => {
      console.error("Error updating favorite status: ", error);
    });
}

firebase.auth().onAuthStateChanged(function (user) {
  if (user) {
    renderSavedLyrics(user.uid);
  }
});

function saveLyrics() {
  var user = firebase.auth().currentUser;
  if (!user) {
    alert("You need to be logged in to save lyrics.");
    return;
  }

  var lyrics = $("#generatedLyrics").text().replace("Generated Lyrics:\n", "");
  var title = prompt("Enter a title for your lyrics:", "New Song");

  if (title !== null) {
    db.collection("lyrics")
      .add({
        userId: user.uid,
        title: title,
        lyrics: lyrics,
        translations: {},
        createdAt: firebase.firestore.FieldValue.serverTimestamp(),
        favorite: false,
        rating: 0,
      })
      .then(() => {
        alert("Lyrics saved successfully!");
        renderSavedLyrics(user.uid);
      })
      .catch((error) => {
        console.error("Error saving lyrics: ", error);
      });
  }
}

function sortLyrics() {
  var sortOption = $("#sortOption").val();
  var user = firebase.auth().currentUser;
  if (!user) {
    alert("You need to be logged in to sort lyrics.");
    return;
  }

  var query = db.collection("lyrics").where("userId", "==", user.uid);

  if (sortOption === "favorite") {
    query = query.orderBy("favorite", "desc");
  } else if (sortOption === "alphabetical") {
    query = query.orderBy("title");
  } else if (sortOption === "date") {
    query = query.orderBy("createdAt", "desc");
  }

  query.get().then((querySnapshot) => {
    var savedLyricsList = $("#savedLyricsList");
    savedLyricsList.empty();
    querySnapshot.forEach((doc) => {
      var lyricsData = doc.data();
      var listItem = `
                <li>
                    <a href="javascript:goToLyricsDetails('${
                      doc.id
                    }')" class="lyrics-link">${lyricsData.title}</a>
                    <button onclick="markAsFavorite('${
                      doc.id
                    }', ${!lyricsData.favorite})">${
        lyricsData.favorite ? "Unfavorite" : "Favorite"
      }</button>
                    <button onclick="deleteLyrics('${doc.id}')">Delete</button>
                </li>`;
      savedLyricsList.append(listItem);
    });
  });
}

$(document).ready(function () {
  ui.start("#firebaseui-auth-container", uiConfig);

  firebase.auth().onAuthStateChanged(function (user) {
    console.log(user); // Dodane logowanie użytkownika
    if (user) {
      $("#loginSection").hide();
      $("#generateSection").show();
      $("#sideMenu").show();
      $("#userDetails")
        .text(`${user.providerData[0].displayName.split(" ")[0]}`)
        .show();
      $("#userPhoto").attr("src", user.providerData[0].photoURL).show();
      $("#logoutButton").show();
      $("#loginButton").hide();
      loadSavedLyrics(user.uid);
    } else {
      $("#loginSection").show();
      $("#generateSection").hide();
      $("#sideMenu").hide();
      $("#userDetails").hide();
      $("#userPhoto").hide();
      $("#logoutButton").hide();
      $("#loginButton").show();
    }
  });

  $("#generateButton").click(function () {
    var prompt = $("#prompt").val();
    var data = {
      prompt: prompt,
    };
    $.ajax({
      url: "/generate",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        $("#generatedLyrics").text(
          "Generated Lyrics:\n" + response.generated_lyrics
        );
        $("#melodySection").show();
      },
    });
    return false;
  });

  $("#generateMelodyButton").click(function () {
    var lyrics = $("#generatedLyrics")
      .text()
      .replace("Generated Lyrics:\n", "");
    var data = {
      lyrics: lyrics,
    };
    $.ajax({
      url: "/generate_melody",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        $("#melodyLink").attr("href", response.melody_url);
        $("#melodyLink").show();
      },
    });
    return false;
  });

  $("#downloadOriginalPdfButton").click(function () {
    var lyrics = $("#generatedLyrics")
      .text()
      .replace("Generated Lyrics:\n", "");
    var data = {
      lyrics: lyrics,
    };
    $.ajax({
      url: "/download_pdf",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        var blob = new Blob([response], { type: "application/pdf" });
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = "original_lyrics.pdf";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      },
    });
    return false;
  });

  $("#translateButton").click(function () {
    var lyrics = $("#generatedLyrics")
      .text()
      .replace("Generated Lyrics:\n", "");
    var targetLang = $("#targetLang").val();
    var data = {
      lyrics: lyrics,
      target_lang: targetLang,
    };
    $.ajax({
      url: "/translate",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        $("#translatedLyrics").text(
          "Translated Lyrics:\n" + response.translated_lyrics
        );
        $("#translatedSection").show();
        $("#downloadTranslatedPdfButton").show();
        $("#downloadBothPdfButton").show();
      },
    });
    return false;
  });

  $("#downloadTranslatedPdfButton").click(function () {
    var translatedLyrics = $("#translatedLyrics")
      .text()
      .replace("Translated Lyrics:\n", "");
    var data = {
      lyrics: translatedLyrics,
    };
    $.ajax({
      url: "/download_pdf",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        var blob = new Blob([response], { type: "application/pdf" });
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = "translated_lyrics.pdf";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      },
    });
    return false;
  });

  $("#downloadBothPdfButton").click(function () {
    var originalLyrics = $("#generatedLyrics")
      .text()
      .replace("Generated Lyrics:\n", "");
    var translatedLyrics = $("#translatedLyrics")
      .text()
      .replace("Translated Lyrics:\n", "");
    var data = {
      original_lyrics: originalLyrics,
      translated_lyrics: translatedLyrics,
    };
    $.ajax({
      url: "/download_both_pdf",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        var blob = new Blob([response], { type: "application/pdf" });
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = "lyrics_both_versions.pdf";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      },
    });
    return false;
  });

  $("#saveLyricsButton").click(function () {
    saveLyrics();
  });
});

// Wylogowywanie użytkownika Firebase po kliknięciu przycisku "Logout"
$(document).ready(function () {
  $("#logoutButton").click(function () {
    firebase
      .auth()
      .signOut()
      .then(() => {
        // Wylogowano pomyślnie
        alert("Logged out successfully!");
        window.location.href = "/"; // Przekierowanie do strony głównej
      })
      .catch((error) => {
        // Wystąpił błąd podczas wylogowywania
        console.error("Error logging out: ", error);
      });
  });

  $("#loginButton").click(function () {
    firebase
      .auth()
      .signInWithPopup(new firebase.auth.GoogleAuthProvider())
      .then((result) => {
        // Pomyslnie zalogowano
        $("#loginSection").hide();
        $("#generateSection").show();
        $("#userDetails")
          .text(`${result.user.displayName.split(" ")[0]}`)
          .show();
        $("#userPhoto").attr("src", result.user.photoURL).show();
        $("#logoutButton").show();
        $("#loginButton").hide();
        loadSavedLyrics(result.user.uid);
      })
      .catch((error) => {
        // Wystapil blad podczas logowania
        console.error("Error during login: ", error);
      });
  });
});
