
// JavaScript to hide the loading overlay when the page is fully loaded
window.addEventListener('load', function() {
    var loadingOverlay = document.getElementById('loading-overlay');
    loadingOverlay.style.display = 'none';
});

  



$(document).ready(function() {
    var navbar = $(".navbar-container");
    var sticky = navbar.offset().top;

    $(window).scroll(function() {
        if ($(window).scrollTop() >= sticky) {
            navbar.addClass("sticky-navbar");
        } else {
            navbar.removeClass("sticky-navbar");
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    updateCartCounter();
});

function updateCartCounter() {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var cartItemsCount = cart.reduce((acc, item) => acc + item.quantity, 0);
    document.getElementById('lblCartCount').textContent = cartItemsCount;
}

function addToCartFunction(imageUrl, title, description, cost) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);
    
    if (itemIndex !== -1) {
        // Item already in cart, increment quantity
        cart[itemIndex].quantity += 1;
    } else {
        // New item, add to cart with quantity 1
        cart.push({ imageUrl: imageUrl, title: title, description: description, cost: cost, quantity: 1 });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter();
}

function incrementItem(imageUrl) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);
    
    if (itemIndex !== -1) {
        cart[itemIndex].quantity += 1;
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter();
}

function decrementItem(imageUrl) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);
    
    if (itemIndex !== -1) {
        if (cart[itemIndex].quantity > 1) {
            cart[itemIndex].quantity -= 1;
        } else {
            cart.splice(itemIndex, 1);
        }
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter();
}

