document.addEventListener('DOMContentLoaded', () => {
    // Simulate loading for 10 seconds
    setTimeout(() => {
        document.querySelector('.loader-container').style.display = 'none';
        document.getElementById('content').style.display = 'block';
    }, 3000); // 10 seconds
});