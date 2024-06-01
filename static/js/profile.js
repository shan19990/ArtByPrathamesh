$(document).ready(function() {
    $('#editButton').click(profileEditOnClick);
    $('#cross-close').click(closeProfileForm);
});

function profileEditOnClick() {
    var editbutton = document.getElementById('editButton');
    var submitbutton = document.getElementById('submitButton');
    var closebutton = document.getElementById('cross-close');

    // Enable input fields
    document.getElementById('firstname').removeAttribute('disabled');
    document.getElementById('lastname').removeAttribute('disabled');

    // Hide edit button
    editbutton.classList.add('d-none');

    // Show submit button and close button
    submitbutton.classList.remove('d-none');
    closebutton.style.display = 'block';
}

function closeProfileForm() {
    var editbutton = document.getElementById('editButton');
    var submitbutton = document.getElementById('submitButton');
    var closebutton = document.getElementById('cross-close');

    // Disable input fields
    document.getElementById('firstname').setAttribute('disabled', 'disabled');
    document.getElementById('lastname').setAttribute('disabled', 'disabled');

    // Show the Edit button
    editbutton.classList.remove('d-none');

    // Hide the submit button and close button
    submitbutton.classList.add('d-none');
    closebutton.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    updateCartCounter();
});

function updateCartCounter() {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var cartItemsCount = cart.reduce((acc, item) => acc + item.quantity, 0);
    document.getElementById('lblCartCount').textContent = cartItemsCount;
}
