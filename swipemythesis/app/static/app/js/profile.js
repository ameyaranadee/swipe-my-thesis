document.addEventListener('DOMContentLoaded', function() {
    const readMoreLinks = document.querySelectorAll('.read-more');

    readMoreLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); 
            const paperTitle = this.closest('.paper-item').querySelector('h3').innerText;
            alert(`You're about to read more about: ${paperTitle}`);
            window.open(this.href, '_blank');
        });
    });
});

// Toggle paper list visibility
function togglePapers(element) {
    const papersList = element.querySelector('.papers-list');
    papersList.style.display = (papersList.style.display === 'none') ? 'block' : 'none';

    // Rotate the arrow icon
    const arrowIcon = element.querySelector('.arrow-icon');
    arrowIcon.classList.toggle('rotated');
}

// function toggleLike(event, icon) {
//     event.stopPropagation(); // Prevent parent click event
//     icon.classList.toggle('liked');
// }

function generateSummary(event, title) {
    event.stopPropagation(); // Prevent parent click event
    alert(`Generating summary for: ${title}`);
}

function toggleLike(icon) {
    icon.classList.toggle('liked');
}
