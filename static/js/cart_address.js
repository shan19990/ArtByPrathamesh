function selectAddress(addressId) {
    // Remove 'selected' class from all address cards
    document.querySelectorAll('.address-card').forEach(function(card) {
        card.classList.remove('selected');
    });
    // Add 'selected' class to the clicked address card
    document.getElementById('address_' + addressId).classList.add('selected');
    // Enable the pay button
    document.getElementById('payButton').disabled = false;
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
