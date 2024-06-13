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

function handleProfileUpdateResponse(data) {
    if (data.toastr_level && data.toastr_content) {
        toastr[data.toastr_level](data.toastr_content);
        window.location.href = "{% url 'profile' %}";
    }
}

function sortTable(header) {
    const table = document.getElementById('userTable');
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);
    const field = header.getAttribute('data-field');
    const currentSort = header.getAttribute('data-sort');
    let newOrder = 'asc';

    // Determine the new sort order
    if (currentSort === 'asc') {
        newOrder = 'desc';
    }

    // Clear existing sort indicators
    document.querySelectorAll('th.sortable').forEach(th => {
        th.removeAttribute('data-sort');
        th.innerHTML = th.innerHTML.replace(/ ▲| ▼/, '');
    });

    // Update the header to show the current sort order
    header.setAttribute('data-sort', newOrder);
    header.innerHTML += newOrder === 'asc' ? ' ▲' : ' ▼';

    // Sort the rows based on the clicked header
    rows.sort((a, b) => {
        const cellA = a.querySelector(`td:nth-child(${header.cellIndex + 1})`).innerText.toLowerCase();
        const cellB = b.querySelector(`td:nth-child(${header.cellIndex + 1})`).innerText.toLowerCase();

        if (cellA < cellB) {
            return newOrder === 'asc' ? -1 : 1;
        } else if (cellA > cellB) {
            return newOrder === 'asc' ? 1 : -1;
        } else {
            return 0;
        }
    });

    // Re-append the sorted rows to the tbody
    rows.forEach(row => tbody.appendChild(row));
}