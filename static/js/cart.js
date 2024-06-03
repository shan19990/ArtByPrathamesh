function incrementItemCart(imageUrl) {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);
    
    if (itemIndex !== -1) {
        cart[itemIndex].quantity += 1;
    }
    
    localStorage.setItem('cart_' + username, JSON.stringify(cart));
    updateCartCounter();
    renderCartItems();
}

function decrementItemCart(imageUrl) {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);
    
    if (itemIndex !== -1) {
        if (cart[itemIndex].quantity > 1) {
            cart[itemIndex].quantity -= 1;
        } else {
            cart.splice(itemIndex, 1);
        }
    }
    
    localStorage.setItem('cart_' + username, JSON.stringify(cart));
    updateCartCounter();
    renderCartItems();
    renderCartActions()
}

function clearItemCart(imageUrl) {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    cart = cart.filter(item => item.imageUrl !== imageUrl);
    
    localStorage.setItem('cart_' + username, JSON.stringify(cart));
    updateCartCounter();
    renderCartItems();
}

function deleteItemCart(imageUrl) {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var updatedCart = cart.filter(item => item.imageUrl !== imageUrl);
    localStorage.setItem('cart_' + username, JSON.stringify(updatedCart)); // Update the local storage
    updateCartCounter();
    renderCartItems();
    renderCartActions()
}

document.addEventListener('DOMContentLoaded', function() {
    renderCartItems();
    renderCartActions();
});

function renderCartItems() {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var cartItemsContainer = document.getElementById('cart-items');
    var cartTotalContainer = document.getElementById('cart-total');
    cartItemsContainer.innerHTML = ''; // Clear previous items
    cartTotalContainer.innerHTML = ''; // Clear previous total

    var totalValue = 0;

    cart.forEach(function(item) {
        // Retrieve the quantity for the current item
        var quantity = item ? item.quantity : 0;
        var itemCost = item.cost * quantity; // Calculate the cost for the current item
        totalValue += itemCost; // Accumulate the total value

        var itemHtml = `
            <div class="card mb-3 col-12">
                <div class="card-body d-flex align-items-center justify-content-between">
                    <div class="d-flex align-items-center">
                        <img src="${item.imageUrl}" class="img-thumbnail mr-3" style="width: 80px; height: 80px; object-fit: cover;" alt="${item.title}">
                        <div class="d-flex flex-column">
                            <h5 class="card-title mb-0">${item.title}</h5>
                            <p class="card-title mb-0">Cost: ${item.cost}</p>
                            <p class="card-title">Quantity: <span id="quantity-${item.imageUrl}">${quantity}</span></p>
                        </div>
                    </div>
                    <div class="btn-group" role="group" aria-label="Cart item controls">
                        <button class="btn btn-secondary" onclick="incrementItemCart('${item.imageUrl}')">+</button>
                        <button class="btn btn-secondary" onclick="decrementItemCart('${item.imageUrl}')">-</button>
                        <button class="btn btn-dark-brown" onclick="deleteItemCart('${item.imageUrl}')">Remove</button>
                    </div>
                </div>
            </div>
        `;

        cartItemsContainer.innerHTML += itemHtml;
    });

    // Display the total cart value
    var totalHtml = `
        <div class="card-top">
            <div class="card-body d-flex justify-content-between">
                <h5>Total Cart Value:</h5>
                <h5>${totalValue}</h5>
            </div>
        </div>
    `;

    cartTotalContainer.innerHTML = totalHtml;
}


function renderCartActions() {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var cartActionsContainer = document.getElementById('cart-actions');

    // Check if cartActionsContainer exists
    if (cartActionsContainer) {
        if (cart.length > 0) {
            // Render Proceed to Select Address button
            cartActionsContainer.innerHTML = "<a href='/select_address/' class='btn btn-transparent' style='border:solid;border-width:thin;' id='submitButton'>Proceed to Select Address</a>";
        } else {
            // Render Empty Cart message
            cartActionsContainer.innerHTML = "<p>Empty Cart. <a href='/painting_for_sale/'>Return to Shop</a></p>";
        }
    } else {
        console.error("cart-actions container not found");
    }
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
