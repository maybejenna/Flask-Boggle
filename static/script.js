$(document).ready(function() {
    let score = 0;
    let timeLeft;
    let foundWords = [];
    let timer;

    // Hide the game-over popup initially
    $('#game-over-popup').hide();

    $('#start-game').on('click', function() {
        $(this).hide(); // Hide the start button
        $('#game-container').show();// Show the game elements
        $('#score-container').show(); // Show the game elements
        initializeGame(); // Function to start the game
    });

    function initializeGame() {
        score = 0; // Reset score
        timeLeft = 60; // Reset time
        foundWords = []; // Reset found words
        $('#score').text('Score: ' + score); // Reset displayed score
        $('#time').text(timeLeft + ' seconds left'); // Display initial time
        $('#found-words').empty(); // Clear the found words list

        // Start or reset the timer
        if (timer) {
            clearInterval(timer);
        }
        timer = setInterval(function() {
            timeLeft--;
            $('#time').text(timeLeft + ' seconds left');
        
            if (timeLeft <= 0) {
                clearInterval(timer); // Stop the timer
                endGame();
            }
        }, 1000);

        // Enable inputs if they were previously disabled
        $('input[type="submit"], input[name="guess"]').prop('disabled', false);
    }

    function endGame() {
        $('#time').text('Time is up!');
        $('#final-score').text(score); // Display final score in the popup
        $('#game-over-popup').show(); // Show the game over popup
        $('input[type="submit"], input[name="guess"]').prop('disabled', true); // Disable inputs
        sendGameStatistics(score); // Send the final score to the server
    }

    $('form').on('submit', function(event) {
        event.preventDefault(); // Prevent form from causing page refresh
        if (timeLeft <= 0) return; // Do not process guess if time is up

        var guess = $('input[name="guess"]').val(); // Get the guess from the input
        if (foundWords.includes(guess)) {
            $('#result').text('Already found: ' + guess); // Notify already found
            return; // Skip already found words
        }

        axios.post('/guess', { guess: guess })
            .then(function(response) {
                var result = response.data.result;
                $('#result').text('Result: ' + result); // Display the result
                if (result === 'Nice find!') {
                    score += guess.length; // Increase score by word length
                    $('#score').text('Score: ' + score); // Display updated score
                    foundWords.push(guess); // Add word to found list
                    updateFoundWordsList(foundWords); // Update the list in the DOM
                }
                $('input[name="guess"]').val(''); // Clear the input
            })
            .catch(function(error) {
                console.log(error);
            });
    });
    
    $('#play-again').on('click', function() {
        window.location.reload(); // Reload the page to start a new game
    });
    
    // Cancel button (hides the popup)
    $('#cancel').on('click', function() {
        $('#game-over-popup').hide(); // Hide the popup
    });

    $('input[name="guess"]').on('input', function() {
        var currentGuess = $(this).val().toUpperCase();
        highlightLetters(currentGuess);
    });


});

function updateFoundWordsList(words) {
    var listHtml = words.join(', '); // Create a string of words separated by commas
    $('#found-words').text(listHtml); // Update the DOM with the found words list
}

function sendGameStatistics(score) {
    axios.post('/game-statistics', { score: score })
        .then(function(response) {
            // You can use response data to show updated stats or confirm the update
            console.log('Updated stats:', response.data);
        })
        .catch(function(error) {
            console.log(error);
        });
}