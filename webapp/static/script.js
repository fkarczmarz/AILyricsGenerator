    // Initialize Firebase
    var firebaseConfig = {
        apiKey: "AIzaSyC4CclwR1NAHNU4HFxuFAC7URg7msWhBBU",
        authDomain: "ai-lyrics-generator-v1.firebaseapp.com",
        projectId: "ai-lyrics-generator-v1",
        storageBucket: "ai-lyrics-generator-v1.appspot.com",
        messagingSenderId: "221274510140",
        appId: "1:221274510140:web:d8fb0cd157b53b6ff08439",
        measurementId: "G-TYCG4RSKBK"
    };

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

        var ui = new firebaseui.auth.AuthUI(firebase.auth());

        var uiConfig = {
            callbacks: {
                signInSuccessWithAuthResult: function(authResult, redirectUrl) {
                    $('#loginSection').hide();
                    $('#generateSection').show();
                    $('#userDetails').text(`Logged in as: ${authResult.user.email}`);
                    return false;
                },
                uiShown: function() {
                    document.getElementById('loader').style.display = 'none';
                }
            },
            signInFlow: 'popup',
            signInOptions: [
                firebase.auth.GoogleAuthProvider.PROVIDER_ID
            ],
            tosUrl: 'https://www.example.com/terms-of-service',
            privacyPolicyUrl: 'https://www.example.com/privacy-policy'
        };

        $(document).ready(function() {
            ui.start('#firebaseui-auth-container', uiConfig);

            $('#generateButton').click(function() {
                var prompt = $('#prompt').val();
                var data = {
                    prompt: prompt
                };
                $.ajax({
                    url: '/generate',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function(response) {
                        $('#generatedLyrics').text("Generated Lyrics:\n" + response.generated_lyrics);
                        $('#melodySection').show();
                    }
                });
                return false;
            });

            $('#generateMelodyButton').click(function() {
                var lyrics = $('#generatedLyrics').text().replace("Generated Lyrics:\n", "");
                var data = {
                    lyrics: lyrics
                };
                $.ajax({
                    url: '/generate_melody',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function(response) {
                        $('#melodyLink').attr('href', response.melody_url);
                        $('#melodyLink').show();
                    }
                });
                return false;
            });

            $('#downloadOriginalPdfButton').click(function() {
                var lyrics = $('#generatedLyrics').text().replace("Generated Lyrics:\n", "");
                var data = {
                    lyrics: lyrics
                };
                $.ajax({
                    url: '/download_pdf',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function(response) {
                        var blob = new Blob([response], { type: 'application/pdf' });
                        var url = window.URL.createObjectURL(blob);
                        var a = document.createElement('a');
                        a.href = url;
                        a.download = 'original_lyrics.pdf';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    }
                });
                return false;
            });

            $('#translateButton').click(function() {
                var lyrics = $('#generatedLyrics').text().replace("Generated Lyrics:\n", "");
                var targetLang = $('#targetLang').val();
                var data = {
                    lyrics: lyrics,
                    target_lang: targetLang
                };
                $.ajax({
                    url: '/translate',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function(response) {
                        $('#translatedLyrics').text("Translated Lyrics:\n" + response.translated_lyrics);
                        $('#translatedSection').show();
                        $('#downloadTranslatedPdfButton').show();
                        $('#downloadBothPdfButton').show();
                    }
                });
                return false;
            });

            $('#downloadTranslatedPdfButton').click(function() {
                var translatedLyrics = $('#translatedLyrics').text().replace("Translated Lyrics:\n", "");
                var data = {
                    lyrics: translatedLyrics
                };
                $.ajax({
                    url: '/download_pdf',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function(response) {
                        var blob = new Blob([response], { type: 'application/pdf' });
                        var url = window.URL.createObjectURL(blob);
                        var a = document.createElement('a');
                        a.href = url;
                        a.download = 'translated_lyrics.pdf';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    }
                });
                return false;
            });

            $('#downloadBothPdfButton').click(function() {
                var originalLyrics = $('#generatedLyrics').text().replace("Generated Lyrics:\n", "");
                var translatedLyrics = $('#translatedLyrics').text().replace("Translated Lyrics:\n", "");
                var data = {
                    original_lyrics: originalLyrics,
                    translated_lyrics: translatedLyrics
                };
                $.ajax({
                    url: '/download_both_pdf',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data),
                    success: function(response) {
                        var blob = new Blob([response], { type: 'application/pdf' });
                        var url = window.URL.createObjectURL(blob);
                        var a = document.createElement('a');
                        a.href = url;
                        a.download = 'lyrics_both_versions.pdf';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                    }
                });
                return false;
            });
        });
