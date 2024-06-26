function showAddressForm() {
    document.getElementById('addressForm').style.display = 'block';
    document.getElementById('AddressButton').classList.add('d-none');
}

function closeAddressForm() {
    document.getElementById('addressForm').style.display = 'none';
    document.getElementById('AddressButton').classList.remove('d-none');
}

function editAddress(street, city, state, postalCode, phoneNumber, id) {
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

    // Get the top position of the form
    var formTop = document.getElementById('addressForm').getBoundingClientRect().top;

    // Scroll to a bit above the form
    window.scrollBy({ top: formTop - 50, behavior: 'smooth' }); // Adjust the offset as needed
}

function clearAddress() {
    document.getElementById('street').value = '';
    document.getElementById('city').value = '';
    document.getElementById('state').value = '';
    document.getElementById('postal_code').value = '';
    document.getElementById('phone_number').value = '';
    document.getElementById('form-id').value = '';
}

document.addEventListener('DOMContentLoaded', checkQueryParams);

function checkQueryParams() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('showForm')) {
        showAddressForm();
    }
}