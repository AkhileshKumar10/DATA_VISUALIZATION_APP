// static/script.js

function getRandomColor() {
    // Generate a random color in hexadecimal format
    return '#' + Math.floor(Math.random()*16777215).toString(16);
}

function setMixedBackgroundColor() {
    // Generate two random colors
    const color1 = getRandomColor();
    const color2 = getRandomColor();

    // Apply a gradient background
    document.body.style.background = `linear-gradient(to right, ${color1}, ${color2})`;
}

// Call the function to set the mixed background color when the page loads
window.onload = setMixedBackgroundColor;
