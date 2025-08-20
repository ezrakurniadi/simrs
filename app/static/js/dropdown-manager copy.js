/**
 * Unified Dropdown Manager
 * Standardizes the population and behavior of all dropdown fields in the application
 * 
 * This module provides a consistent interface for loading dropdown data from APIs,
 * handling both simple and complex dropdowns with search capabilities.
 */

class DropdownManager {
    /**
     * Initialize the dropdown manager
     */
    constructor() {
        this.dropdowns = new Map();
        this.initAllDropdowns();
    }

    /**
     * Initialize all dropdowns on the page
     */
    initAllDropdowns() {
        // Standard dropdowns (ID Type, Race, Payor Type, etc.)
        this.initStandardDropdown('id_type', '/api/id-types');
        this.initStandardDropdown('race', '/api/races');
        this.initStandardDropdown('payor-type', '/api/payor-types');
        
        // Dropdowns with search capabilities (Ethnicity, Language, etc.)
        this.initSearchDropdown('ethnicity', '/api/ethnicities');
        this.initSearchDropdown('preferred_language', '/api/languages');
        
        // Payor detail dropdown (depends on payor type)
        this.initPayorDetailDropdown();
    }

    /**
     * Initialize a standard dropdown that loads all options from an API
     * @param {string} elementId - The ID of the select element
     * @param {string} apiUrl - The API endpoint to fetch data from
     */
    initStandardDropdown(elementId, apiUrl) {
        const element = document.getElementById(elementId);
        if (!element) return;

        // Store dropdown configuration
        this.dropdowns.set(elementId, {
            element: element,
            apiUrl: apiUrl,
            type: 'standard'
        });

        // Load data
        this.loadDropdownData(elementId);
    }

    /**
     * Initialize a dropdown with search capabilities using Select2
     * @param {string} elementId - The ID of the select element
     * @param {string} apiUrl - The API endpoint to fetch data from
     */
    initSearchDropdown(elementId, apiUrl) {
        console.log(`Initializing search dropdown for ${elementId}`);
        const element = document.getElementById(elementId);
        if (!element) {
            console.error(`Dropdown element with ID '${elementId}' not found`);
            return;
        }
        
        if (typeof $ === 'undefined') {
            console.error('jQuery is not defined');
            return;
        }
        
        if (typeof $.fn.select2 === 'undefined') {
            console.error('Select2 is not defined');
            return;
        }

        // Store dropdown configuration
        this.dropdowns.set(elementId, {
            element: element,
            apiUrl: apiUrl,
            type: 'search'
        });

        console.log(`Initializing Select2 for ${elementId}`);
        try {
            $(`#${elementId}`).select2({
            placeholder: `Select ${this.formatLabel(elementId)}`,
            allowClear: true,
            width: '100%',
            dropdownAutoWidth: true,
            dropdownParent: $(`#${elementId}`).parent(),
            ajax: {
                url: apiUrl,
                dataType: 'json',
                delay: 250,
                transport: function(params, success, failure) {
                    console.log(`Fetching data from ${params.url}`);
                    const xhr = $.ajax(params);
                    xhr.then(success);
                    xhr.fail(failure);
                    return xhr;
                },
                data: function (params) {
                    return {
                        search: params.term
                    };
                },
                processResults: function (data) {
                    // If data already has a results property, return it directly
                    // Otherwise, wrap the data in a results property
                    return data.results ? data : { results: data };
                },
                cache: true
            },
            minimumInputLength: 1,
            templateResult: this.formatSelect2Result.bind(this),
            templateSelection: this.formatSelect2Selection.bind(this)
            });
            console.log(`Select2 initialized successfully for ${elementId}`);
        } catch (error) {
            console.error(`Error initializing Select2 for ${elementId}:`, error);
        }
    }

    /**
     * Initialize the payor detail dropdown which depends on the payor type
     */
    initPayorDetailDropdown() {
        const payorTypeSelect = document.getElementById('payor-type');
        const payorDetailSelect = document.getElementById('payor-detail');
        
        if (!payorTypeSelect || !payorDetailSelect) return;

        // Store dropdown configuration
        this.dropdowns.set('payor-detail', {
            element: payorDetailSelect,
            apiUrl: '/api/payor-details',
            type: 'dependent',
            dependsOn: 'payor-type'
        });

        // Set initial state
        if (payorTypeSelect.value === '') {
            payorDetailSelect.disabled = true;
        } else {
            payorDetailSelect.disabled = false;
            this.loadPayorDetails(payorTypeSelect.value);
        }

        // Add event listener to update when payor type changes
        payorTypeSelect.addEventListener('change', (e) => {
            this.handlePayorTypeChange(e.target.value, payorDetailSelect);
        });
    }

    /**
     * Handle changes to the payor type dropdown
     * @param {string} payorType - The selected payor type
     * @param {HTMLElement} payorDetailSelect - The payor detail select element
     */
    handlePayorTypeChange(payorType, payorDetailSelect) {
        // Clear existing options
        payorDetailSelect.innerHTML = '';
        
        // Add default option
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Select ' + (payorType ? payorType + ' Detail' : 'Payor Type First');
        payorDetailSelect.appendChild(defaultOption);
        
        // Load payor details if a payor type is selected
        if (payorType) {
            this.loadPayorDetails(payorType);
            payorDetailSelect.disabled = false;
            payorDetailSelect.focus();
        } else {
            payorDetailSelect.disabled = true;
        }
    }

    /**
     * Load payor details based on the selected payor type
     * @param {string} payorType - The selected payor type
     */
    async loadPayorDetails(payorType) {
        try {
            // First, get the payor type ID
            const payorTypesResponse = await fetch('/api/payor-types');
            const payorTypes = await payorTypesResponse.json();
            const payorTypeObj = payorTypes.find(pt => pt.name === payorType);
            
            if (!payorTypeObj) {
                throw new Error('Payor type not found');
            }
            
            // Then get the payor details
            const response = await fetch(`/api/payor-details/${payorTypeObj.id}`);
            const data = await response.json();
            
            // Add payor details to the dropdown
            const payorDetailSelect = document.getElementById('payor-detail');
            data.forEach(detail => {
                const option = document.createElement('option');
                option.value = detail.name;
                option.textContent = detail.name;
                payorDetailSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching payor details:', error);
        }
    }

    /**
     * Load data for a dropdown from its API endpoint
     * @param {string} dropdownId - The ID of the dropdown to load
     */
    async loadDropdownData(dropdownId) {
        const config = this.dropdowns.get(dropdownId);
        if (!config || config.type !== 'standard') return;

        try {
            const response = await fetch(config.apiUrl);
            const data = await response.json();
            
            // Clear existing options except the first one
            while (config.element.options.length > 1) {
                config.element.remove(1);
            }
            
            // Add data to the dropdown
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.name || item.id;
                option.textContent = item.name || item.text;
                config.element.appendChild(option);
            });
        } catch (error) {
            console.error(`Error fetching ${dropdownId} data:`, error);
        }
    }

    /**
     * Format the appearance of items in the dropdown
     * @param {object} data - The data object for the item
     * @returns {string|jQuery} - The formatted item
     */
    formatSelect2Result(data) {
        if (!data.id) {
            return data.text;
        }
        
        const $result = $('<span></span>');
        $result.text(data.text);
        return $result;
    }

    /**
     * Format the appearance of the selected item
     * @param {object} data - The data object for the item
     * @returns {string} - The formatted selection
     */
    formatSelect2Selection(data) {
        return data.text || data.id;
    }

    /**
     * Format a label from an element ID
     * @param {string} id - The element ID
     * @returns {string} - Formatted label
     */
    formatLabel(id) {
        return id
            .replace(/_/g, ' ')
            .replace(/-/g, ' ')
            .replace(/\b\w/g, l => l.toUpperCase());
    }
}

// Initialize the dropdown manager when the DOM is loaded and jQuery is ready
$(document).ready(function() {
    console.log('Document ready, initializing DropdownManager');
    new DropdownManager();
});