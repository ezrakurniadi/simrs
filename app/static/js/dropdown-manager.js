console.log('Dropdown manager script loaded');

// Main initialization function
function initializeDropdowns() {
    console.log('Dropdown manager initialized');
    console.log('jQuery loaded:', typeof $ !== 'undefined');
    
    // Check if jQuery is properly loaded
    if (typeof $ === 'undefined') {
        console.error('jQuery is not loaded');
        return;
    }
    
    console.log('jQuery is loaded, proceeding with initialization');
    
    // Accessibility enhancements
    const form = document.querySelector('form');
    form.setAttribute('novalidate', '');
    
    // Add ARIA attributes to form controls
    const formControls = form.querySelectorAll('input, select, textarea');
    formControls.forEach(control => {
        if (!control.hasAttribute('aria-label') && !control.hasAttribute('aria-labelledby')) {
            const label = form.querySelector(`label[for="${control.id}"]`);
            if (label) {
                control.setAttribute('aria-labelledby', label.id);
            }
        }
    });

    // Fetch ID types from API
    fetch('/api/id-types')
        .then(response => response.json())
        .then(data => {
            const idTypeSelect = document.getElementById('id_type');
            // Clear existing options except the first one
            while (idTypeSelect.options.length > 1) {
                idTypeSelect.remove(1);
            }
            // Add ID types from API
            data.forEach(function(idType) {
                const option = document.createElement('option');
                option.value = idType.name;
                option.textContent = idType.name;
                idTypeSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching ID types:', error);
        });

    // Fetch nationalities from API
    fetch('/api/nationalities')
        .then(response => response.json())
        .then(data => {
            const nationalitySelect = document.getElementById('nationality_id');
            // Clear existing options except the first one
            while (nationalitySelect.options.length > 1) {
                nationalitySelect.remove(1);
            }
            // Add nationalities from API
            data.forEach(function(nationality) {
                const option = document.createElement('option');
                option.value = nationality.id;
                option.textContent = nationality.name;
                nationalitySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching nationalities:', error);
        });

    // Enhanced conditional field visibility with ARIA
    function toggleFieldVisibility(field, targetField) {
        if (field.value === 'True') {
            targetField.style.display = 'block';
            targetField.setAttribute('aria-hidden', 'false');
            // Focus the first input in the revealed field
            const firstInput = targetField.querySelector('input, select, textarea');
            if (firstInput) {
                firstInput.focus();
            }
        } else {
            targetField.style.display = 'none';
            targetField.setAttribute('aria-hidden', 'true');
        }
    }

    // Initialize conditional fields
    const conditionalFields = [
        { field: 'problematic_patient', target: 'problematic_patient_reason_field' },
        { field: 'loyalty_member', target: 'loyalty_member_number_field' },
        { field: 'chronic_condition', target: 'chronic_condition_details_field' },
        { field: 'allergy_alert', target: 'allergy_alert_details_field' }
    ];

    conditionalFields.forEach(config => {
        const field = document.querySelector(`select[name="${config.field}"]`);
        const targetField = document.getElementById(config.target);

        if (field && targetField) {
            // Set initial state
            toggleFieldVisibility(field, targetField);

            // Add event listener
            field.addEventListener('change', function() {
                toggleFieldVisibility(field, targetField);
            });

            // Enhanced keyboard navigation
            field.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    field.value = field.value === 'True' ? 'False' : 'True';
                    toggleFieldVisibility(field, targetField);
                }
            });
        }
    });

    // Enhanced keyboard navigation for the form
    const formGroups = form.querySelectorAll('.mb-3');
    formGroups.forEach(group => {
        const inputs = group.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    // Find the next focusable element
                    const focusableElements = form.querySelectorAll('input, select, textarea, button, a');
                    const currentIndex = Array.from(focusableElements).indexOf(this);
                    if (currentIndex < focusableElements.length - 1) {
                        e.preventDefault();
                        focusableElements[currentIndex + 1].focus();
                    }
                }
            });
        });
    });

    // Dynamic payor dropdowns
    const payorTypeSelect = document.getElementById('payor-type');
    const payorDetailSelect = document.getElementById('payor-detail');

    // Fetch payor types from API
    fetch('/api/payor-types')
        .then(response => response.json())
        .then(data => {
            // Clear existing options except the first one
            while (payorTypeSelect.options.length > 1) {
                payorTypeSelect.remove(1);
            }

            // Add payor types from API
            data.forEach(function(payorType) {
                const option = document.createElement('option');
                option.value = payorType.name;
                option.textContent = payorType.name;
                payorTypeSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching payor types:', error);
        });

    // Handle payor type selection
    payorTypeSelect.addEventListener('change', function() {
        const selectedType = this.value;
        
        // Set initial state of payor detail dropdown
        if (selectedType === '') {
            payorDetailSelect.disabled = true;
            // Clear existing options
            payorDetailSelect.innerHTML = '';
            // Add default option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Select Payor Type First';
            payorDetailSelect.appendChild(defaultOption);
        } else {
            payorDetailSelect.disabled = false;
        
            // Clear existing options
            payorDetailSelect.innerHTML = '';

            // Add default option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Select ' + selectedType + ' Detail';
            payorDetailSelect.appendChild(defaultOption);

            // Fetch payor details based on selected payor type
            // Get payor type ID from the selected type name
            fetch(`/api/payor-types`)
                .then(response => response.json())
                .then(payorTypes => {
                    const payorType = payorTypes.find(pt => pt.name === selectedType);
                    if (payorType) {
                        return fetch(`/api/payor-details/${payorType.id}`);
                    }
                    return Promise.reject('Payor type not found');
                })
                .then(response => response.json())
                .then(data => {
                    // Add payor details from API
                    data.forEach(function(detail) {
                        const option = document.createElement('option');
                        option.value = detail.name;
                        option.textContent = detail.name;
                        payorDetailSelect.appendChild(option);
                    });
                    
                    // Focus the payor detail field when enabled and data is loaded
                    payorDetailSelect.focus();
                })
                .catch(error => {
                    console.error('Error fetching payor details:', error);
                });
        }
    });
}

// Ensure initialization happens after DOM is ready and libraries are loaded
if (document.readyState === 'loading') {
    console.log('DOM is still loading, will initialize on DOMContentLoaded');
    document.addEventListener('DOMContentLoaded', initializeDropdowns);
} else {
    // DOM is already ready
    console.log('DOM is already ready, initializing immediately');
    initializeDropdowns();
}
