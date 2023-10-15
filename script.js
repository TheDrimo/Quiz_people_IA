//const SERVER_URL = "http://127.0.0.1:5000";
const SERVER_URL = "http://87.106.121.103:5000";
//const SERVER_URL = "http://192.168.1.52:5000";

// Fetch data from the server
async function fetchData() {
    console.log("appel server")
    try {
        let response = await fetch(`${SERVER_URL}/api`);
        let data = await response.json();
        return data;
        console.log("get response")
    } catch (error) {
        console.error("Error fetching data:", error);
        console.log("no response")
    }
}

// Variables to keep track of current question data and the correct answer
let currentData = null;
let correctAnswerIndex = null;
let imageClicked = false;

// Display the question and answers on the page
async function displayQuestion() {
    currentData = await fetchData();

    let questionElement = document.getElementById("question");
    let answersElements = document.querySelectorAll(".answer");

    let randomCountry = Math.floor(Math.random() * 2) + 1;
    correctAnswerIndex = randomCountry === 1 ? 0 : 1;

    questionElement.textContent = `Who is the ${currentData['country' + randomCountry]}?`;

    answersElements[0].style.backgroundImage = `url(data:image/png;base64,${currentData.image1})`;
    answersElements[1].style.backgroundImage = `url(data:image/png;base64,${currentData.image2})`;

    resetAnswerStyles();
}

// Reset answer styles for next question
function resetAnswerStyles() {
    let answersElements = document.querySelectorAll(".answer");
    answersElements.forEach(el => {
        el.style.opacity = "1";
    });
}

// Check if the user's answer is correct
function checkAnswer(index) {
    if (imageClicked) {
        nextQuestion(); // Go to the next question on the second click
        return;
    }

    let answersElements = document.querySelectorAll(".answer");
    let selectedAnswer, correctAnswer, wrongAnswer;

    if (index === correctAnswerIndex) {
        answersElements[index].style.opacity = "1";
        answersElements[1 - index].style.opacity = "0.1";

        answersElements[1 - index].style.backgroundColor = "rgba(255, 0, 0, 0.5)"; // Red for wrong answer

        selectedAnswer = answersElements[index].style.backgroundImage;
        correctAnswer = answersElements[index].style.backgroundImage;
        wrongAnswer = answersElements[1 - index].style.backgroundImage;
    } else {
        answersElements[index].style.opacity = "0.1";
        answersElements[correctAnswerIndex].style.opacity = "1";

        answersElements[index].style.backgroundColor = "rgba(255, 0, 0, 0.5)"; // Red for wrong answer
        answersElements[correctAnswerIndex].style.backgroundColor = "rgba(0, 255, 0, 0.5)"; // Green for correct answer

        selectedAnswer = answersElements[index].style.backgroundImage;
        correctAnswer = answersElements[correctAnswerIndex].style.backgroundImage;
        wrongAnswer = answersElements[index].style.backgroundImage;
    }

    // Optionally, disable the click event after the user has made a choice
    answersElements[0].removeEventListener("click", checkAnswer);
    answersElements[1].removeEventListener("click", checkAnswer);

    imageClicked = true;

    // Sending data to server
    sendDataToServer(selectedAnswer, correctAnswer, wrongAnswer);
}

function sendDataToServer(selected, correct, wrong) {
    fetch(`${SERVER_URL}/api/response`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            selectedAnswer: selected,
            correctAnswer: correct,
            wrongAnswer: wrong
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // handle response from server if needed
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

// Move to the next question
function nextQuestion() {
    displayQuestion();
    imageClicked = false;
}

// Display the first question when the page loads
displayQuestion();
