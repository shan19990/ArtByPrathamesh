
function showFilter(){
    var filters = document.querySelector('.filter-div');
    if (filters.style.display === 'none' || filters.style.display === '') {
        filters.style.display = 'block';
    } else {
        filters.style.display = 'none';
    }
}

function addToCartFunction(imageUrl, title, description, cost) {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);
    
    if (itemIndex !== -1) {
        cart[itemIndex].quantity += 1;
    } else {
        cart.push({ imageUrl: imageUrl, title: title, description: description, cost: cost, quantity: 1 });
    }
    
    localStorage.setItem('cart_' + username, JSON.stringify(cart));
    updateCartCounter();
}

function incrementItem(imageUrl) {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);
    
    if (itemIndex !== -1) {
        cart[itemIndex].quantity += 1;
    }
    
    localStorage.setItem('cart_' + username, JSON.stringify(cart));
    updateCartCounter();
}

function decrementItem(imageUrl) {
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
}

function clearItem(imageUrl) {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    cart = cart.filter(item => item.imageUrl !== imageUrl);
    
    localStorage.setItem('cart_' + username, JSON.stringify(cart));
    updateCartCounter();
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

// Check if there are more items to load
function checkMoreItems() {
    var moreItems = true; 

    var scrollMessage = document.getElementById("scroll-message");

    if (!moreItems) {
        scrollMessage.style.display = "none";
    }
}

window.onload = function() {
    checkMoreItems();
};

$(document).ready(function() {
    var page = 1;
    var loading = false;
    var threshold = 100;
    var timeout;
    var currentStyleFilter = null;
    var currentSortOption = null;
    var currentPath = window.location.pathname;
    var isPaintingForSalePage = currentPath.startsWith('/painting_for_sale/');
    var isMerchForSalePage = currentPath.startsWith('/merch/');
    var isGalleryPage = currentPath.startsWith('/gallery/');

    if (isPaintingForSalePage || isMerchForSalePage || isGalleryPage) {
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

        function debounceScroll() {
            if (timeout) {
                clearTimeout(timeout);
            }
            timeout = setTimeout(function() {
                if ($(window).scrollTop() + $(window).height() >= $(document).height() - threshold) {
                    loadPaintings(currentStyleFilter, currentSortOption);
                }
            }, 100);
        }

        loadPaintings();

        $(window).on('scroll', debounceScroll);

        document.getElementById("submit-filters").addEventListener("click", function() {
            console.log("Filtering...");
            var styleFilter = document.getElementById("painting-filter").value || null;
            var sortOption = document.querySelector('input[name="sort"]:checked') ? document.querySelector('input[name="sort"]:checked').value : null;
            loadPaintings(styleFilter, sortOption, true);
        });

        function clearFilters() {
            document.getElementById("painting-filter").selectedIndex = 0;
            var sortOptions = document.getElementsByName("sort");
            for (var i = 0; i < sortOptions.length; i++) {
                sortOptions[i].checked = false;
            }
        }

        document.getElementById("clear-filters").addEventListener("click", function() {
            clearFilters();
            loadPaintings(null, null, true);
        });
    }
});

function showDetails(imageUrl, title, description, cost, addToCart) {
    var username = document.getElementById('username').value;
    document.getElementById('modalImage').src = imageUrl;
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalDescription').textContent = description;
    document.getElementById('modalCost').textContent = "Cost: " + cost;

    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var item = cart.find(item => item.imageUrl === imageUrl);
    var quantity = item ? item.quantity : 0;

    var buttonContainer = document.getElementById('buttonContainer');
    buttonContainer.innerHTML = '';

    if (addToCart && quantity === 0) {
        var addToCartButton = document.createElement('button');
        addToCartButton.textContent = 'Add to Cart';
        addToCartButton.id = 'addToCartButton';
        addToCartButton.className = 'btn btn-dark';
        buttonContainer.appendChild(addToCartButton);

        addToCartButton.onclick = function() {
            addToCartFunction(imageUrl, title, description, cost);
            showDetails(imageUrl, title, description, cost, addToCart);
        };
    } else if (quantity > 0) {
        var incrementButton = document.createElement('button');
        incrementButton.textContent = '+';
        incrementButton.id = 'incrementButton';
        incrementButton.className = 'btn btn-secondary';
        buttonContainer.appendChild(incrementButton);

        var quantityInput = document.createElement('input');
        quantityInput.type = 'number';
        quantityInput.value = quantity;
        quantityInput.id = 'quantityInput';
        quantityInput.className = 'quantity-input';
        buttonContainer.appendChild(quantityInput);

        var decrementButton = document.createElement('button');
        decrementButton.textContent = '-';
        decrementButton.id = 'decrementButton';
        decrementButton.className = 'btn btn-secondary';
        buttonContainer.appendChild(decrementButton);

        var clearButton = document.createElement('button');
        clearButton.textContent = 'Clear';
        clearButton.id = 'clearButton';
        clearButton.className = 'btn btn-dark-brown';
        buttonContainer.appendChild(clearButton);

        incrementButton.onclick = function() {
            incrementItem(imageUrl);
            showDetails(imageUrl, title, description, cost, addToCart);
        };

        decrementButton.onclick = function() {
            decrementItem(imageUrl);
            showDetails(imageUrl, title, description, cost, addToCart);
        };

        clearButton.onclick = function() {
            clearItem(imageUrl);
            showDetails(imageUrl, title, description, cost, addToCart);
        };

        quantityInput.onchange = function() {
            var newQuantity = parseInt(quantityInput.value, 10);
            if (newQuantity >= 0) {
                updateItemQuantity(imageUrl, newQuantity);
                showDetails(imageUrl, title, description, cost, addToCart);
            }
        };
    }

    jQuery('#pictureModal').modal('show');
}

function updateItemQuantity(imageUrl, newQuantity) {
    var username = document.getElementById('username').value;
    var cart = JSON.parse(localStorage.getItem('cart_' + username)) || [];
    var itemIndex = cart.findIndex(item => item.imageUrl === imageUrl);

    if (itemIndex !== -1) {
        if (newQuantity > 0) {
            cart[itemIndex].quantity = newQuantity;
        } else {
            cart.splice(itemIndex, 1);
        }
    }

    localStorage.setItem('cart_' + username, JSON.stringify(cart));
    updateCartCounter();
}