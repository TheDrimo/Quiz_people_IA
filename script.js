// script.js

const messageDiv = document.getElementById("responseMessage");
const messageright = document.getElementById("subbannerMessageright");
const messageleft = document.getElementById("subbannerMessageleft");
const imageElement1 = document.getElementById("responseImage1");
const imageElement2 = document.getElementById("responseImage2");


function sendRequestToServer(){
    // Send a POST request to the server
    fetch("http://127.0.0.1:5000/api", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: "are you ok ?" }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Server not available");
            }
            return response.json();
        })
        .then((data) => {
            // Display the server's response
            messageDiv.textContent = data.message;
            messageright.textContent = data.country2;
            messageleft.textContent = data.country1;
            const base64ImageData1 = data.image_string1;
            const base64ImageData2 = data.image_string2;
            const imgElement = new Image();

            imageElement1.src = `data:image/jpeg;base64,${base64ImageData1}`;
            imageElement2.src = `data:image/jpeg;base64,${base64ImageData2}`;
        })
        .catch((error) => {
            console.error(error);
            messageDiv.textContent = "nobody alive there";
        });
};


window.addEventListener("load", sendRequestToServer);


imageElement1.addEventListener("click", sendRequestToServer);
imageElement2.addEventListener("click", sendRequestToServer);
