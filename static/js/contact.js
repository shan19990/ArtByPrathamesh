function onCaptchaSuccess() {
    document.getElementById('submitButton').removeAttribute('disabled');
};

function onCaptchaExpired() {
    document.getElementById('submitButton').setAttribute('disabled', 'disabled');
};
