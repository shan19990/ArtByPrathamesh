document.addEventListener('DOMContentLoaded', () => {
    const fadeText = document.querySelector('.fade-text');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                fadeText.classList.add('visible');
            } else {
                fadeText.classList.remove('visible');
            }
        });
    }, {
        threshold: 0.1   // Adjust this threshold as needed
    });

    observer.observe(fadeText);
});

document.addEventListener('DOMContentLoaded', function() {
    updateCartCounter();
});

function updateCartCounter() {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var cartItemsCount = cart.reduce((acc, item) => acc + item.quantity, 0);
    document.getElementById('lblCartCount').textContent = cartItemsCount;
}
