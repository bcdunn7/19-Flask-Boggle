class BoggleGame {
    // make a new Boogle Game

    constructor() {
        this.startTimer();

        this.score = 0;
        this.words = new Set();

        $('#guess-btn').on('click', this.handleGuess.bind(this));
            //alternatievly to binding, I could just not pass in the event to handgleGuess or is GuessValid
        $('#restart-btn').on('click', this.reloadPage);
    }


    // test whether guess is valid
    async isGuessValid(e) {
        e.preventDefault();
        // get guess from from
        let $guess = $('#guess').val();
        if (!$guess) return;

        if (this.words.has($guess)) {
            $('#result-display').text("Already Found!");
            $('#guess').val('');
            return;
        }

        const resp = await axios.get('/check-guess', { params: {word: $guess}});

        let guessResponce = [resp.data.result, $guess]

        $('#guess').val('')

        return guessResponce
    }

    //display guess result depending on answer given
    showGuessResult(answer, guess) {
        if (answer === "not-word") {
            $('#result-display').text("That is not a valid word!");
            $('#adding-score').text('');
        }
        else if (answer === "not-on-board") {
            $('#result-display').text("That word is not on the board!");
            $('#adding-score').text('');
        }
        else if (answer === "ok") {
            $('#result-display').text("Great Guess!");

            //add word to words set
            this.words.add(guess);

            //update score
            this.score += guess.length;

            $('#current-score').html(`${this.score}<div id="adding-score"></div>`);
            $('#adding-score').text(`+${guess.length}`);
        }

    }

    // handle guess
    async handleGuess(e) {
        e.preventDefault();

        let resp = await this.isGuessValid(e);

        let answer = resp[0]
        let guess = resp[1]

        this.showGuessResult(answer, guess);
    }


    //on game start, start timer
    async startTimer(){
        //hide restart button
        $('#restart-container').hide();

        let count = 59
        let $timer = $('#timer')

        let timerID = window.setInterval(
            async function(){
                $timer.text(count);
                count -= 1
                if (count > -1 && count < 5) {
                    $('#timer-container').addClass('timer-running-out');
                }
                else if (count === -1) {
                    clearInterval(timerID);
                    $('#timer-container').addClass('timer-finished');
                    await this.gameOver();
                } 
        }.bind(this),
        1000);
    }


    // game over
    async gameOver() {
        $('#guess-btn').off('click');
        $('#guess-form').hide();
        $('#restart-container').show();

        //data for play count and high score
        const resp = await axios.post('/store-score', {"score": this.score});

        if (resp.data === true) {
            $('#score-result').text(`!!New High Score: ${this.score}!!`)
        }
        else {
            $('#score-result').text(`Round Score: ${this.score}`)
        }
    }

    // restart game
    reloadPage() {
        location.reload(true);
    }

}

let game = new BoggleGame();

