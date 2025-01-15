$(document).on('click', '.editable', function () {
    const $this = $(this);

    // Avoid creating multiple input elements if clicked again
    if ($this.find('input').length > 0) return;

    const originalValue = $this.text().trim(); // The current value displayed
    const pk = $this.data('pk'); // Primary key of the record
    const fieldName = $this.data('name'); // Field name to update

    // Create the input element
    const input = $('<input>', {
        type: 'text',
        value: originalValue,
        class: 'editable-input',
        css: { width: '100%' },
    });

    // Replace the text with the input element
    $this.html(input);
    input.focus();

    // Handle save on Enter key press
    input.on('keypress', function (e) {
        if (e.key === 'Enter') {
            handleSave($this, input, pk, fieldName, originalValue);
        }
    });

    // Handle blur event to save or revert
    input.on('blur', function () {
        handleSave($this, input, pk, fieldName, originalValue);
    });

    function handleSave(element, inputField, recordPk, field, original) {
        const newValue = inputField.val().trim(); // The value entered by the user

        if (newValue === original) {
            // If value hasn't changed, revert to original display
            element.text(original);
        } else {
            // If value has changed, send an AJAX request to update
            $.ajax({
                url: '/update/',
                method: 'POST',
                data: {
                    pk: recordPk,
                    field: field,
                    value: newValue,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success: function () {
                    element.text(newValue); // Update display with the new value
                },
                error: function () {
                    alert('Failed to update. Please try again.');
                    element.text(original); // Revert to original value on failure
                },
            });
        }
    }
});
