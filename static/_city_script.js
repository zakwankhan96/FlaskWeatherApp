var prediction_button= document.getElementById("prediction");
var pred_form= document.getElementById("pred_form");

prediction_button.addEventListener("click", function(){
    pred_form.toggleAttribute("hidden")
});
//Scrolling Function
let scrollInterval;

function startScroll(scrollAmount) {
    const container = document.querySelector(".card-container");

    scrollInterval = setInterval(() => {
        container.scrollTop += scrollAmount;
    }, 10);
}

function stopScroll() {
    clearInterval(scrollInterval);
}
//function to show or hide scroll button
function toggleScrollButton() {
    const container = document.querySelector(".card-container");
    const upButton = document.querySelector(".up-button");
    const downButton = document.querySelector(".down-button");

    const isOverflowing = container.scrollHeight > container.clientHeight;

    upButton.style.display = isOverflowing ? "block" : "none";
    downButton.style.display = isOverflowing ? "block" : "none";
}

window.addEventListener("DOMContentLoaded", toggleScrollButton);

//function to change body background depending upon time of day
function changeBackgroundColor() {
    var element = document.getElementById("body");
    var currentTime = new Date().getHours();
    //set time periods and background color
    if (currentTime >= 4 && currentTime < 6) {
        // Dawn
        element.style.background =
            "radial-gradient(at top right, rgb(243,144,79), rgb(59,67,113))";
    } else if (currentTime >= 6 && currentTime < 8) {
        // Sunrise
        element.style.background =
            "radial-gradient(at top right, rgb(179,90,38), rgb(252,190,109))";
    } else if (currentTime >= 8 && currentTime < 12) {
        // Day
        element.style.background =
            "radial-gradient(at top right, rgb(156,236,251), rgb(101,199,247), rgb(0,82,212))";
    } else if (currentTime >= 12 && currentTime < 16) {
        // Afternoon
        element.style.background =
            "radial-gradient(at top right, rgb(252,234,187), rgb(248,181,0))";
    } else if (currentTime >= 16 && currentTime < 19) {
        // Dusk
        element.style.background =
            "radial-gradient(at top right, rgb(251,176,59), rgb(237,28,36))";
    } else if (currentTime >= 19 && currentTime < 23) {
        // Twilight
        element.style.background =
            "radial-gradient(at top right, rgb(171,0,125), rgb(73,0,199))";
    } else if (currentTime >= 23 || currentTime < 4) {
        // Night
        element.style.background =
            "radial-gradient(at top right, rgb(28,32,82), rgb(65,14,107), rgb(80,37,112))";
    }
}
changeBackgroundColor();

//function to change font color when background color gets darker
function updateFontColor() {
    var date = new Date();
    var currentHour = date.getHours();
    var element = document.getElementById("body");

    if (currentHour >= 19 || currentHour < 4) {
        element.style.color = "white";
    }
}
updateFontColor();

//function to show the form when the add button is clicked
function showForm() {
    var formContainer = document.getElementById("formContainer");
    formContainer.style.display = "block";

    var addButton = document.getElementById("add_button");
    addButton.classList.add("clicked");
}
function hideForm() {
    var formContainer = document.getElementById("formContainer");
    formContainer.style.display = "none";
}
document.addEventListener("click", function (event) {
    var addButton = document.getElementById("add_button");
    var formContainer = document.getElementById("formContainer");

    if (
        !addButton.contains(event.target) &&
        !formContainer.contains(event.target)
    ) {
        hideForm();
    }
});

//funxtion to send City name to route handler when remove button is clicked
function removeCity(cityName) {
    $.ajax({
        url: "/remove_city",
        type: "POST",
        data: { city_name: cityName },
        success: function () {
            location.reload();
        },
        error: function () {
            console.log("Error occurred while removing city.");
        },
    });
}

