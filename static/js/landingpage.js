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
