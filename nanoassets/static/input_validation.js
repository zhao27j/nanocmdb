
(() => {
    // const templateVariableDataSet = document.querySelector('#template_variable');
    // const dataHostnameList = templateVariableDataSet.hostnameList;

})()

// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }

        form.classList.add('was-validated')
        }, false)
    })
})()

(() => {
    'use strict'

    const hostnameUpdModal = document.getElementById('hostnameUpdModal');
    const hostnameUpdModalInput = document.getElementById('hostnameUpdModalInput');

    hostnameUpdModal.addEventListener('shown.bs.modal', () => {
        hostnameUpdModalInput.focus()
    })

    hostnameUpdModalInput.addEventListener('focusout', event => {
        const hostnameListDataSet = hostnameUpdModal.dataset.hostnameList;
        const hostnameList = hostnameListDataSet.replace(/[\[\]']/g, '').split(', ');

        if (hostnameList.includes(hostnameUpdModalInput.value)) {
            hostnameUpdModalInput.setCustomValidity(`the Hostname given [ {hostnameUpdModalInput.value} ] does exist in the system`);
            hostnameUpdModalInput.value = '';
            hostnameUpdModalInput.focus();
        } else {
            hostnameUpdModalInput.setCustomValidity("");
        }

    })
})()
