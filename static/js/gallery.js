$(document).ready(function() {
    var page = 1;  // Initial page number
    var loading = false; // Flag to prevent multiple AJAX requests
    var threshold = 100; // Threshold for triggering the AJAX call (in pixels)
    var timeout; // Variable to store timeout ID
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
            }
        
            if (!loading) {
                loading = true;
                jQuery.noConflict();
                $.ajax({
                    url: "/load_paintings_filters/",
                    type: "GET",
                    data: {
                        'page': page,
                    },
                    dataType: "json",
                    success: function(response) {
                        var paintings = response.paintings;
                        var html = '';
                        
                        paintings.forEach(function(painting) {
                            html += '<div class="painting-card" data-image-url="' + painting.image_url + '" data-title="' + painting.title + '" data-description="' + painting.description + '" data-cost="' + painting.cost + '" onclick="showDetails(\'' + painting.image_url + '\', \'' + painting.title + '\', \'' + painting.description + '\', \'' + painting.cost + '\')">';
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
                    loadPaintings();
                }
            }, 100); // Adjust debounce delay as needed
        }

        // Load initial paintings when the page is ready
        loadPaintings();

        // Bind debounce function to scroll event
        $(window).on('scroll', debounceScroll);
    }
});


function showDetails(imageUrl, title, description, cost) {
    // Set modal content with picture details
    document.getElementById('modalImage').src = imageUrl;
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalDescription').textContent = description;
    document.getElementById('modalCost').textContent = "Cost: " + cost;

    // Open Bootstrap modal
    jQuery('#pictureModal').modal('show');
}


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
