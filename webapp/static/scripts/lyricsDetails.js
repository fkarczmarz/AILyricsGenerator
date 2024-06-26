// $(document).ready(function () {
//   var lyricsId = "{{ lyrics_id }}";
//   console.log(lyricsId);

//   var user = firebase.auth().currentUser;
//   if (user) {
//     loadLyricsDetailsFromDetails(lyricsId);
//   } else {
//     firebase.auth().onAuthStateChanged(function (user) {
//       if (user) {
//         loadLyricsDetailsFromDetails(lyricsId);
//       }
//     });
//   }
// });

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
          $("#lyricsFavorite").text(`Favorite: ${lyricsData.favorite}`);
          $("#lyricsCreatedAt").text(
            `Created At: ${new Date(
              lyricsData.createdAt.toDate()
            ).toISOString()}`
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

  function saveLyricsFromDetails() {
    var user = firebase.auth().currentUser;
    if (!user) return;

    var lyrics = $("#lyricsContent").text();
    var title = $("#lyricsTitle").text();

    if (title !== null) {
      db.collection("lyrics")
        .doc(lyricsId)
        .update({
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
        })
        .catch((error) => {
          console.error("Error saving lyrics: ", error);
        });
    }
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
        alert("Lyrics rated successfully!");
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

