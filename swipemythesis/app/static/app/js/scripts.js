let currentStep = 1;
const totalSteps = 4;

function updateDots() {
    document.querySelectorAll('.dot').forEach((dot, index) => {
        dot.classList.toggle('active', index + 1 === currentStep);
    });
}

function showStep(step) {
    document.querySelectorAll('.form-step').forEach(el => {
        el.classList.remove('active');
    });
    document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');
    
    document.getElementById('prevBtn').style.display = step === 1 ? 'none' : 'block';
    document.getElementById('nextBtn').textContent = step === totalSteps ? 'Submit' : 'Next';
    
    updateDots();
}

function adjustTime(amount) {
    const display = document.querySelector('.time-display');
    let currentTime = parseInt(display.textContent);
    currentTime = Math.max(15, Math.min(120, currentTime + amount));
    display.textContent = currentTime;
    document.getElementById('reading_time').value = currentTime;
}

// Handle interest button clicks
document.querySelectorAll('.interest-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        this.classList.toggle('selected');
        
        if (this.parentElement.classList.contains('recency-options')) {
            // For recency, only allow one selection
            document.querySelectorAll('.recency-options .interest-btn').forEach(other => {
                if (other !== this) other.classList.remove('selected');
            });
            document.getElementById('paper_recency').value = this.dataset.value;
            document.getElementById('paper_recency').textContent = this.dataset.value;
        } else if (this.parentElement.classList.contains('research-interests')) {
            // For research interests, only allow one selection
            document.querySelectorAll('.research-interests .interest-btn').forEach(other => {
                other.classList.remove('selected');
            });
            this.classList.add('selected');
            document.getElementById('research_interests').value = this.dataset.value;
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const difficultySlider = document.getElementById('difficulty_level');
    const difficultyLevelHiddenInput = document.getElementById('difficulty_level_hidden');
    const difficultyLevelLabel = document.querySelector('.difficulty-labels');

    if (difficultySlider && difficultyLevelHiddenInput) {
        difficultySlider.addEventListener('input', function() {
            const value = parseInt(difficultySlider.value);
            const difficultyText = value <= 50 ? 'Basic' : 'Advanced';
            difficultyLevelHiddenInput.value = difficultyText;
            difficultyLevelHiddenInput.textContent = difficultyText;

            // Update labels for visual feedback                                          
            difficultyLevelLabel.querySelectorAll('span').forEach((label, index) => {
                label.style.fontWeight = index === (difficultyText === 'Basic' ? 0 : 1) ? 'bold' : 'normal';
            });
        });
    }
});



// Navigation button handlers
document.getElementById('nextBtn').addEventListener('click', function() {
    if (currentStep === totalSteps) {
        document.getElementById('preferencesForm').submit();
    } else {
        currentStep++;
        showStep(currentStep);
    }
});

document.getElementById('prevBtn').addEventListener('click', function() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
});

// Initialize
showStep(1);
