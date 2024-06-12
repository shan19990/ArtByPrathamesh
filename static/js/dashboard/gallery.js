
function showImageForm() {
    document.getElementById('imageForm').style.display = 'block';
    document.getElementById('galleryRow').style.marginTop = '500px'; // Adjust this value as needed
    document.getElementById('ImageButton').classList.add('d-none');
}

function closeImageForm() {
    document.getElementById('imageForm').style.display = 'none';
    document.getElementById('galleryRow').style.marginTop = '0';
    document.getElementById('ImageButton').classList.remove('d-none');
}

function clearImageForm() {
    document.getElementById('title').value = '';
    document.getElementById('image').value = '';
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('imagePreview').src = '#';
}

function previewImage() {
    var file = document.getElementById('image').files[0];
    var reader = new FileReader();

    reader.onload = function (e) {
        var imagePreview = document.getElementById('imagePreview');
        imagePreview.src = e.target.result;
        imagePreview.style.display = 'block';
    };

    if (file) {
        reader.readAsDataURL(file);
    }
}
