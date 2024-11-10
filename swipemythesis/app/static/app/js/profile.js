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

function toggleLike(event, icon) {
    event.stopPropagation(); // Prevent parent click event
    icon.classList.toggle('liked');
}

// function generateSummary(event, title) {
//     event.stopPropagation(); // Prevent parent click event
//     alert(⁠ Generating summary for: ${title} ⁠);
// }


// document.addEventListener('DOMContentLoaded', () => {
//     const menuBtn = document.getElementById('menu-btn');
//     const sidebar = document.getElementById('sidebar');

//     // Toggle sidebar open/close
//     menuBtn.addEventListener('click', (e) => {
//         e.stopPropagation(); // Prevent the click from bubbling up
//         if (sidebar.classList.contains('open')) {
//             sidebar.classList.remove('open');
//             sidebar.style.visibility = 'hidden'; // Completely hide when collapsed
//         } else {
//             sidebar.classList.add('open');
//             sidebar.style.visibility = 'visible'; // Show when expanded
//         }
//     });

//     // Close sidebar when clicking outside of it
//     document.addEventListener('click', (e) => {
//         if (!sidebar.contains(e.target) && e.target !== menuBtn) {
//             sidebar.classList.remove('open');
//             sidebar.style.visibility = 'hidden'; // Completely hide when collapsed
//         }
//     });
// });

function generateSummary(event, title) {
    event.stopPropagation(); // Prevent parent click event

    // Get the modal and content elements
    const modal = document.getElementById('popup-modal');
    const modalContent = document.querySelector('.modal-content p');
    const modalTitle = document.querySelector('.modal-content h2');

    // Update modal content with the summary
    modalTitle.innerText = `Summary for: ${title}`;
    modalContent.innerText = `When there exists uncertainty, Al machines are designed to make decisions so as to reach the best expected outcomes.
    Expectations are based on true facts about the objective environment the machines interact with, and those facts can be encoded into Al models in the form of true objective probability functions. Accordingly, Al models involve probabilistic machine learning in which the probabilities should be objectively interpreted. We prove under some basic assumptions when machines can learn the true objective probabilities, if any, and when machines cannot learn them.`;

    // Display the modal
    modal.style.display = 'block';
}

// Close modal functionality
document.addEventListener('DOMContentLoaded', () => {
    // Generate summary and display the modal
    function generateSummary(event, title) {
        event.stopPropagation(); // Prevent parent click event

        // Get the modal and content elements
        const modal = document.getElementById('popup-modal');
        const modalContent = modal.querySelector('p');
        const modalTitle = modal.querySelector('h2');

        // Update modal content with the summary
        modalTitle.innerText = `Summary for: ${title}`;
        modalContent.innerText = `When there exists uncertainty, Al machines are designed to make decisions so as to reach the best expected outcomes.
        Expectations are based on true facts about the objective environment the machines interact with, and those facts can be encoded into Al models in the form of true objective probability functions. Accordingly, Al models involve probabilistic machine learning in which the probabilities should be objectively interpreted. We prove under some basic assumptions when machines can learn the true objective probabilities, if any, and when machines cannot learn them.`;

        // Display the modal
        modal.style.display = 'block';
    }

    // Close modal functionality
    const modal = document.getElementById('popup-modal');
    const closeModal = document.getElementById('close-modal');

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Expose generateSummary globally (if needed for inline onclick attributes)
    window.generateSummary = generateSummary;
});