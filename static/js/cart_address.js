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
