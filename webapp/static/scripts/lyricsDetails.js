var lyricsId =
  window.location.pathname.split("/")[
    window.location.pathname.split("/").length - 1
  ];

function loadLyricsDetailsFromDetails(lyricsId) {
  db.collection("lyrics")
    .doc(lyricsId)
    .get()
    .then((doc) => {
      if (doc.exists) {
        var lyricsData = doc.data();
        $("#lyricsTitle").text(lyricsData.title);
        $("#lyricsContent").text(lyricsData.lyrics);
        $("#lyricsRating").text(`Rating: ${lyricsData.rating}`);
        $("#lyricsRating").html(`${generateStarRating(lyricsData.rating)}`);

        $("#lyricsCreatedAt").text(
          `${formatDateString(
            new Date(lyricsData.createdAt.toDate()).toISOString()
          )}`
        );

        var favoriteButton = $("#markAsFavoriteButton");
        favoriteButton.html(
          lyricsData.favorite
            ? '<i class="fa fa-heart" style="font-size:20px; color: crimson; cursor: pointer;"></i>'
            : '<i class="fa fa-heart-o" style="font-size:20px; cursor: pointer;"></i>'
        );
        favoriteButton.off("click").on("click", function () {
          markAsFavoriteFromDetails(lyricsId, !lyricsData.favorite);
        });
      } else {
        alert("No such lyrics found!");
      }
    })
    .catch((error) => {
      console.error("Error getting lyrics: ", error);
    });
}

function markAsFavoriteFromDetails(docId, favoriteStatus) {
  var user = firebase.auth().currentUser;
  if (!user) return;

  db.collection("lyrics")
    .doc(docId)
    .update({
      favorite: favoriteStatus,
    })
    .then(() => {
      loadLyricsDetailsFromDetails(docId);
    })
    .catch((error) => {
      console.error("Error updating favorite status: ", error);
    });
}

function favoriteHandler() {
  db.collection("lyrics")
    .doc(lyricsId)
    .get()
    .then((doc) => {
      if (doc.exists) {
        var lyricsData = doc.data();
        markAsFavoriteFromDetails(lyricsId, !lyricsData.favorite);
      }
    })
    .catch((error) => {
      console.error("Error getting document:", error);
    });
}

function rateLyricsFromDetails() {
  var user = firebase.auth().currentUser;
  if (!user) return;

  var rating = prompt("Rate this song (1-5):", "5");
  rating = parseInt(rating);
  if (isNaN(rating) || rating < 1 || rating > 5) {
    alert("Invalid rating");
    return;
  }

  db.collection("lyrics")
    .doc(lyricsId)
    .update({
      rating: rating,
    })
    .then(() => {
      loadLyricsDetailsFromDetails(lyricsId);
    })
    .catch((error) => {
      console.error("Error rating lyrics: ", error);
    });
}

function deleteLyricsFromDetails() {
  var user = firebase.auth().currentUser;
  if (!user) return;

  db.collection("lyrics")
    .doc(lyricsId)
    .delete()
    .then(() => {
      alert("Lyrics deleted successfully!");
      window.location.href = "/generate_page";
    })
    .catch((error) => {
      console.error("Error deleting lyrics: ", error);
    });
}

function translateFromDetails(lang) {
  var lyrics = $("#lyricsContent").text().replace("Generated Lyrics:\n", "");
  var data = {
    lyrics: lyrics,
    target_lang: lang,
  };
  $.ajax({
    url: "/translate",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function (response) {
      $("#translatedLyrics").text(response.translated_lyrics);
    },
  });
  return false;
}
