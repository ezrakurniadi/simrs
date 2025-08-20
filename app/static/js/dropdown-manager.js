console.log('Dropdown manager script loaded');
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dropdown manager initialized');
    console.log('jQuery loaded:', typeof $ !== 'undefined');
    console.log('Select2 loaded:', typeof $.fn.select2 !== 'undefined');
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
    // Initialize Select2 for ethnicity dropdown with AJAX search
    console.log('Initializing Select2 for ethnicity dropdown');
    const ethnicityElement = $('#ethnicity');
    console.log('Ethnicity element found:', ethnicityElement.length > 0);
    if (ethnicityElement.length === 0) {
        console.error('Ethnicity dropdown element not found');
    }
    ethnicityElement.select2({
        placeholder: 'Select Ethnicity',
        allowClear: true,
        width: '100%',
        dropdownAutoWidth: true,
        ajax: {
            url: '/api/ethnicities',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                console.log('Ethnicity search term:', params.term);
                return {
                    search: params.term
                };
            },
            processResults: function (data) {
                console.log('Ethnicity results received:', data);
                return data;
            },
            cache: true
        },
        minimumInputLength: 0
    });

    // Initialize Select2 for preferred language dropdown with AJAX search
    console.log('Initializing Select2 for preferred language dropdown');
    const languageElement = $('#preferred_language');
    console.log('Language element found:', languageElement.length > 0);
    if (languageElement.length === 0) {
        console.error('Language dropdown element not found');
    }
    languageElement.select2({
        placeholder: 'Select Preferred Language',
        allowClear: true,
        width: '100%',
        dropdownAutoWidth: true,
        ajax: {
            url: '/api/languages',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                console.log('Language search term:', params.term);
                return {
                    search: params.term
                };
            },
            processResults: function (data) {
                console.log('Language results received:', data);
                return data;
            },
            cache: true
        },
        minimumInputLength: 0
    });
    
    // Test API endpoints directly
    console.log('Testing API endpoints...');
    fetch('/api/ethnicities')
        .then(response => response.json())
        .then(data => {
            console.log('Direct API call to /api/ethnicities:', data);
        })
        .catch(error => {
            console.error('Error fetching ethnicities:', error);
        });
    
    fetch('/api/languages')
        .then(response => response.json())
        .then(data => {
            console.log('Direct API call to /api/languages:', data);
        })
        .catch(error => {
            console.error('Error fetching languages:', error);
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

    payorTypeSelect.addEventListener('change', function() {
        const selectedType = this.value;
        // Clear existing options
        payorDetailSelect.innerHTML = '';

        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select ' + (selectedType ? selectedType + ' Detail' : 'Payor Type First');
        payorDetailSelect.appendChild(defaultOption);

        // Fetch payor details based on selected payor type
        if (selectedType) {
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
                })
                .catch(error => {
                    console.error('Error fetching payor details:', error);
                });
        }
    });

    // Set initial state of payor detail dropdown
    if (payorTypeSelect.value === '') {
        payorDetailSelect.disabled = true;
    } else {
        payorDetailSelect.disabled = false;
    }

    // Enable payor detail dropdown when payor type is selected
    payorTypeSelect.addEventListener('change', function() {
        if (this.value) {
            payorDetailSelect.disabled = false;
            // Focus the payor detail field when enabled
            payorDetailSelect.focus();
        } else {
            payorDetailSelect.disabled = true;
        }
    });
});
