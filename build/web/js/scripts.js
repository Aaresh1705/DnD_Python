// Example scripts.js content

// Function to validate form input
function validateForm() {
    var input = document.getElementById('text_input').value;
    if (input.trim() == '') {
        alert('Input cannot be empty!');
        return false;
    }
    return true;
}

// Function to toggle visibility of elements
function toggleVisibility(elementId) {
    var element = document.getElementById(elementId);
    if (element.style.display === 'none') {
        element.style.display = 'block';
    } else {
        element.style.display = 'none';
    }
}

// Function to send data using AJAX
function sendData() {
    var xhr = new XMLHttpRequest();
    var input = document.getElementById('text_input').value;
    xhr.open('POST', '/some-endpoint', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            console.log(this.responseText); // Handle response here
        }
    };
    xhr.send('input=' + encodeURIComponent(input));
}

// Add event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Example event listener for a form submission
    var form = document.getElementById('myForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!validateForm()) {
                event.preventDefault(); // Prevent form from submitting if validation fails
            }
        });
    }

    // Event listener for toggle button
    var toggleButton = document.getElementById('toggleButton');
    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            toggleVisibility('toggleElement');
        });
    }

    // More event listeners as needed
});
