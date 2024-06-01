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
    cartItemsContainer.innerHTML = ''; // Clear previous items

    // Add flex and flex-wrap style to the container
    cartItemsContainer.style.display = 'flex';
    cartItemsContainer.style.flexWrap = 'nowrap';

    cart.forEach(function(item) {
        // Retrieve the quantity for the current item
        var quantity = item ? item.quantity : 0;

        var itemHtml = `
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body d-flex align-items-center justify-content-between">
                        <div>
                            <h5 class="card-title">${item.title}</h5>
                            <p class="card-text">Cost: ${item.cost}</p>
                            <p class="card-text">Quantity: <span id="quantity-${item.imageUrl}">${quantity}</span></p>
                        </div>
                        <div>
                            <button class="btn btn-success mr-1" onclick="incrementItemCart('${item.imageUrl}')">+</button>
                            <button class="btn btn-warning mx-1" onclick="decrementItemCart('${item.imageUrl}')">-</button>
                            <button class="btn btn-danger" onclick="deleteItemCart('${item.imageUrl}')">Delete</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        cartItemsContainer.innerHTML += itemHtml;
    });
}


function renderCartActions() {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var cartActionsContainer = document.getElementById('cart-actions');

    if (cart.length > 0) {
        // Render Proceed to Select Address button
        cartActionsContainer.innerHTML = '<a href="/select_address/" class="btn btn-transparent" style="border:solid;border-width:thin;" id="submitButton" >Proceed to Select Address</a>';
    } else {
        // Render Empty Cart message
        cartActionsContainer.innerHTML = '<p>Empty Cart. <a href="/painting_for_sale/">Return to Shop</a></p>';
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
