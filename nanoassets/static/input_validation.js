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

    const hostnameUpdModal = document.getElementById('hostnameUpdModal');
    const hostnameUpdModalInput = document.getElementById('hostnameUpdModalInput');

    hostnameUpdModal.addEventListener('shown.bs.modal', () => {
        hostnameUpdModalInput.focus()
    })

    hostnameUpdModalInput.addEventListener('focusout', (e) => hostnameCheck(e));
    hostnameUpdModalInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            hostnameCheck(e);
        }
    });
    
    function hostnameCheck(e) {
        const hostnameInvalidSpan = document.querySelector('#hostnameInvalidSpan');
        const hostnameBtn = document.querySelector('#hostnameBtn');
        const hostnameListDataSet = hostnameUpdModal.dataset.hostnameList;
        const hostnameList = hostnameListDataSet.replace(/[\[\]']/g, '').split(', ');

        if (hostnameUpdModalInput.value.trim() === '' || hostnameList.includes(hostnameUpdModalInput.value.trim())) {
            hostnameInvalidSpan.innerHTML = `the Hostname given [ ${hostnameUpdModalInput.value} ] is Empty or already Existing`;
            hostnameInvalidSpan.className = 'invalid-feedback';

            hostnameBtn.classList.add('disabled');

            hostnameUpdModalInput.setCustomValidity(`the Hostname given [ ${hostnameUpdModalInput.value} ] is Empty or already Existing`);
            hostnameUpdModalInput.value = '';
            hostnameUpdModalInput.focus();
            
        } else {
            hostnameInvalidSpan.innerHTML = "";

            hostnameBtn.classList.remove('disabled');

            hostnameUpdModalInput.setCustomValidity("");
        }

    }
})()