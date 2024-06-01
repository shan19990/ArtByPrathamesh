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

function showAddressForm() {
    document.getElementById('addressForm').style.display = 'block';
    document.getElementById('AddressButton').classList.add('d-none');
}

function closeAddressForm() {
    document.getElementById('addressForm').style.display = 'none';
    document.getElementById('AddressButton').classList.remove('d-none');
}

function editAddress(street, city, state, postalCode, phoneNumber, id) {
    console.log("Edit Address");
    // Populate the form fields with the provided address details
    document.getElementById('street').value = street;
    document.getElementById('city').value = city;
    document.getElementById('state').value = state;
    document.getElementById('postal_code').value = postalCode;
    document.getElementById('phone_number').value = phoneNumber;
    document.getElementById('form-id').value = id;

    // Display the address form
    document.getElementById('addressForm').style.display = 'block';
    document.getElementById('AddressButton').classList.add('d-none');
}

function clearAddress() {
    document.getElementById('street').value = '';
    document.getElementById('city').value = '';
    document.getElementById('state').value = '';
    document.getElementById('postal_code').value = '';
    document.getElementById('phone_number').value = '';
    document.getElementById('form-id').value = '';
}



// JavaScript to hide the loading overlay when the page is fully loaded
window.addEventListener('load', function() {
    var loadingOverlay = document.getElementById('loading-overlay');
    loadingOverlay.style.display = 'none';
});

  
$(document).ready(function() {
    var page = 1;  // Initial page number
    var loading = false; // Flag to prevent multiple AJAX requests
    var threshold = 100; // Threshold for triggering the AJAX call (in pixels)
    var timeout; // Variable to store timeout ID
    var currentStyleFilter = null;
    var currentSortOption = null;
    var currentPath = window.location.pathname;
    var isPaintingForSalePage = currentPath.startsWith('/painting_for_sale/');
    var isMerchForSalePage = currentPath.startsWith('/merch/');
    var isGalleryPage = currentPath.startsWith('/gallery/');

    if (isPaintingForSalePage || isMerchForSalePage || isGalleryPage) {
        // Function to load paintings
        function loadPaintings(styleFilter = null, sortOption = null, resetPage = false) {
            if (resetPage) {
                page = 1;
                $('#paintings-grid').empty();
                currentStyleFilter = styleFilter;
                currentSortOption = sortOption;
            }
        
            if (!loading) {
                loading = true;
                jQuery.noConflict();
                $.ajax({
                    url: "/load_paintings_filters/",
                    type: "GET",
                    data: {
                        'page': page,
                        'style': currentStyleFilter,
                        'sort_option': currentSortOption,
                    },
                    dataType: "json",
                    success: function(response) {
                        var paintings = response.paintings;
                        var html = '';
                        var addToCart = !isGalleryPage;
        
                        paintings.forEach(function(painting) {
                            html += '<div class="painting-card" data-image-url="' + painting.image_url + '" data-title="' + painting.title + '" data-description="' + painting.description + '" data-cost="' + painting.cost + '" onclick="showDetails(\'' + painting.image_url + '\', \'' + painting.title + '\', \'' + painting.description + '\', \'' + painting.cost + '\', ' + addToCart + ')">';
                            html += '<img src="' + painting.image_url + '" alt="' + painting.title + '">';
                            html += '</div>';
                        });
        
                        $('#paintings-grid').append(html);
                        page++;
                        loading = false;
        
                        if (paintings.length === 0) {
                            $('#scroll-message').hide();
                        } else {
                            $('#scroll-message').show();
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error("Failed to load paintings:", error);
                        loading = false;
                    }
                });
            }
        }        

        

        // Function to debounce scroll event
        function debounceScroll() {
            if (timeout) {
                clearTimeout(timeout);
            }
            timeout = setTimeout(function() {
                if ($(window).scrollTop() + $(window).height() >= $(document).height() - threshold) {
                    loadPaintings(currentStyleFilter, currentSortOption);
                }
            }, 100); // Adjust debounce delay as needed
        }

        // Load initial paintings when the page is ready
        loadPaintings();

        // Bind debounce function to scroll event
        $(window).on('scroll', debounceScroll);

        // Event listener for the Apply Filters button
        document.getElementById("submit-filters").addEventListener("click", function() {
            console.log("Filtering...");
            var styleFilter = document.getElementById("painting-filter").value || null;
            var sortOption = document.querySelector('input[name="sort"]:checked') ? document.querySelector('input[name="sort"]:checked').value : null;
            loadPaintings(styleFilter, sortOption, true);
        });

        function clearFilters() {
            // Reset the dropdown and radio buttons to their default values
            document.getElementById("painting-filter").selectedIndex = 0;
            var sortOptions = document.getElementsByName("sort");
            for (var i = 0; i < sortOptions.length; i++) {
                sortOptions[i].checked = false;
            }
            loadPaintings(null, null, true);
        }

        // Event listener for the Clear Filters button
        document.getElementById("clear-filters").addEventListener("click", function() {
            clearFilters();
        });
    }
});


function showDetails(imageUrl, title, description, cost, addToCart) {
    // Set modal content with picture details
    document.getElementById('modalImage').src = imageUrl;
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalDescription').textContent = description;
    document.getElementById('modalCost').textContent = "Cost: " + cost;

    // Get current quantity from cart
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var item = cart.find(item => item.imageUrl === imageUrl);
    var quantity = item ? item.quantity : 0;

    // Display current quantity
    var modalBody = document.querySelector('.modal-body');
    var quantityElement = document.getElementById('itemQuantity');
    if (!quantityElement) {
        quantityElement = document.createElement('p');
        quantityElement.id = 'itemQuantity';
        modalBody.appendChild(quantityElement);
    }
    quantityElement.textContent = "Quantity in cart: " + quantity;

    // Remove any existing buttons
    var existingAddToCartButton = document.getElementById('addToCartButton');
    var existingIncrementButton = document.getElementById('incrementButton');
    var existingDecrementButton = document.getElementById('decrementButton');
    var existingClearButton = document.getElementById('clearButton');

    if (existingAddToCartButton) {
        modalBody.removeChild(existingAddToCartButton);
    }
    if (existingIncrementButton) {
        modalBody.removeChild(existingIncrementButton);
    }
    if (existingDecrementButton) {
        modalBody.removeChild(existingDecrementButton);
    }
    if (existingClearButton) {
        modalBody.removeChild(existingClearButton);
    }

    // Show "Add to Cart" button if addToCart is true and item is not in cart
    if (addToCart && quantity === 0) {
        var addToCartButton = document.createElement('button');
        addToCartButton.textContent = 'Add to Cart';
        addToCartButton.id = 'addToCartButton';
        addToCartButton.className = 'btn btn-primary';
        modalBody.appendChild(addToCartButton);

        addToCartButton.onclick = function() {
            addToCartFunction(imageUrl, title, description, cost);
            showDetails(imageUrl, title, description, cost, addToCart); // Update modal with new quantity
        };
    } else if (quantity > 0) {
        // Show increment, decrement, and clear buttons if item is in cart
        var incrementButton = document.createElement('button');
        incrementButton.textContent = '+';
        incrementButton.id = 'incrementButton';
        incrementButton.className = 'btn btn-secondary';
        modalBody.appendChild(incrementButton);

        var decrementButton = document.createElement('button');
        decrementButton.textContent = '-';
        decrementButton.id = 'decrementButton';
        decrementButton.className = 'btn btn-secondary';
        modalBody.appendChild(decrementButton);

        var clearButton = document.createElement('button');
        clearButton.textContent = 'Clear';
        clearButton.id = 'clearButton';
        clearButton.className = 'btn btn-danger';
        modalBody.appendChild(clearButton);

        incrementButton.onclick = function() {
            incrementItem(imageUrl);
            showDetails(imageUrl, title, description, cost, addToCart); // Update modal with new quantity
        };

        decrementButton.onclick = function() {
            decrementItem(imageUrl);
            showDetails(imageUrl, title, description, cost, addToCart); // Update modal with new quantity
        };

        clearButton.onclick = function() {
            clearItem(imageUrl);
            showDetails(imageUrl, title, description, cost, addToCart); // Update modal with new quantity
        };
    }

    // Open Bootstrap modal
    jQuery('#pictureModal').modal('show');
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

function clearItem(imageUrl) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => item.imageUrl !== imageUrl);
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter();
}

function updateCartCounter() {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    document.getElementById('cart-counter').textContent = cart.reduce((acc, item) => acc + item.quantity, 0);
}

// Initialize cart counter on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartCounter();
});




function showFilter(){
    var filters = document.querySelector('.filter-div');
    if (filters.style.display === 'none' || filters.style.display === '') {
        filters.style.display = 'block';
    } else {
        filters.style.display = 'none';
    }
}

// script.js

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

// Check if there are more items to load
function checkMoreItems() {
    // Check your logic here to determine if there are more items to load
    var moreItems = true; // Change this based on your logic

    // Get the scroll message element
    var scrollMessage = document.getElementById("scroll-message");

    // If there are no more items, hide the scroll message
    if (!moreItems) {
        scrollMessage.style.display = "none";
    }
}

// Call the function when the page loads
window.onload = function() {
    checkMoreItems();
};


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

function incrementItemCart(imageUrl) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);
    
    if (itemIndex !== -1) {
        cart[itemIndex].quantity += 1;
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter();
    renderCartItems();
}

function decrementItemCart(imageUrl) {
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
    renderCartItems();
    renderCartActions()
}

function clearItemCart(imageUrl) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart = cart.filter(item => item.imageUrl !== imageUrl);
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCounter();
    renderCartItems();
}

function deleteItemCart(imageUrl) {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var updatedCart = cart.filter(item => item.imageUrl !== imageUrl);
    localStorage.setItem('cart', JSON.stringify(updatedCart)); // Update the local storage
    updateCartCounter();
    renderCartItems();
    renderCartActions()
}

document.addEventListener('DOMContentLoaded', function() {
    renderCartItems();
    renderCartActions();
});

function renderCartItems() {
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
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
    var cart = JSON.parse(localStorage.getItem('cart')) || [];
    var cartActionsContainer = document.getElementById('cart-actions');

    if (cart.length > 0) {
        // Render Proceed to Select Address button
        cartActionsContainer.innerHTML = '<a href="#" class="btn btn-primary">Proceed to Select Address</a>';
    } else {
        // Render Empty Cart message
        cartActionsContainer.innerHTML = '<p>Empty Cart. <a href="/painting_for_sale/">Return to Shop</a></p>';
    }
}
