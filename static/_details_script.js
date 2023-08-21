var prediction_button= document.getElementById("prediction");
var pred_form= document.getElementById("pred_form");

prediction_button.addEventListener("click", function(){
    pred_form.toggleAttribute("hidden")
});


let scrollInterval;

function startScroll(scrollAmount) {
    const container = document.querySelector(".scroll-container");

    scrollInterval = setInterval(() => {
        container.scrollTop += scrollAmount;
    }, 5);
}

function stopScroll() {
    clearInterval(scrollInterval);
}

// JavaScript code to set the day text
var today = new Date().getDay();
var days = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
];

// Set the day text for each row
var dayElements = document.querySelectorAll('[id^="day"]');
dayElements.forEach(function (element, index) {
    if (index === 0) {
        element.textContent = "Today";
    } else if (index === 1) {
        element.textContent = days[(today + index) % 7];
    } else {
        element.textContent = days[(today + index) % 7];
    }
});
function changeBackgroundColor() {
    var element = document.getElementById("body");
    var currentTime = new Date().getHours();

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

function getTimeOfDay() {
    var currentDate = new Date();
    var currentHour = currentDate.getHours();

    if (currentHour >= 6 && currentHour < 19) {
        // Daytime images
        return "ico_day";
    } else {
        // Nighttime images
        return "ico_night";
    }
}

function updateImageSources() {
    var timeOfDay = getTimeOfDay();

    document.getElementById("real_feel").src =
        "/static/ico/" + timeOfDay + "/celsius.png";
    document.getElementById("max_temp").src =
        "/static/ico/" + timeOfDay + "/high-temperature.png";
    document.getElementById("min_temp").src =
        "/static/ico/" + timeOfDay + "/low-temperature.png";
    document.getElementById("wind").src =
        "/static/ico/" + timeOfDay + "/wind.png";
    document.getElementById("pressure").src =
        "/static/ico/" + timeOfDay + "/pressure.png";
    document.getElementById("cloudcover").src =
        "/static/ico/" + timeOfDay + "/cloudcover.png";
    document.getElementById("dew").src =
        "/static/ico/" + timeOfDay + "/dew.png";
    document.getElementById("preci").src =
        "/static/ico/" + timeOfDay + "/precipitation.png";
    document.getElementById("humidity").src =
        "/static/ico/" + timeOfDay + "/humidity.png";
    document.getElementById("vis").src =
        "/static/ico/" + timeOfDay + "/visibility.png";
    document.getElementById("sunrise").src =
        "/static/ico/" + timeOfDay + "/sunrise.png";
    document.getElementById("sunset").src =
        "/static/ico/" + timeOfDay + "/sunset.png";
}

// Call the updateImageSources function when the page loads
window.onload = updateImageSources;

function updateFontColor() {
    var date = new Date();
    var currentHour = date.getHours();
    var element = document.getElementById("body");

    if (currentHour >= 19 || currentHour < 4) {
        element.style.color = "white";
    }
}
updateFontColor();