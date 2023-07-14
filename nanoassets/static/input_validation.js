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

    // owner Upd Input Verify
    const ownerUpdModal = document.getElementById('ownerUpdModal');
    const ownerUpdModalInput = document.getElementById('ownerUpdModalInput');

    ownerUpdModal.addEventListener('shown.bs.modal', () => ownerUpdModalInput.focus());

    ownerUpdModalInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            ownerChk(e);
        }
    });
    ownerUpdModalInput.addEventListener('focusout', (e) => ownerChk(e));

    function ownerChk(e) {
        const ownerInvalidSpan = document.querySelector('#ownerInvalidSpan');
        const ownerUpdBtn = document.querySelector('#ownerUpdBtn');
        const ownerInstanceDataSet = ownerUpdModal.dataset.ownerInstance;
        const ownerListDataSet = ownerUpdModal.dataset.ownerList;
        const ownerList = ownerListDataSet.replace(/[\[\]']/g, '').split(', ');
        let owners = [];
        ownerList.forEach(owner => {
            owners.push(owner.split("(")[0].trim());
        });

        const ownerChg = ownerUpdModalInput.value.trim();
        if (ownerChg === ownerInstanceDataSet) {
            ownerInvalidSpan.innerHTML = `the Owner given [ ${ownerChg} ] is the same as the orginal`;
            ownerInvalidSpan.className = 'invalid-feedback';

            ownerUpdBtn.classList.add('disabled');

            ownerUpdModalInput.setCustomValidity(`the Owner given [ ${ownerChg} ] is the same as the orginal`);
            ownerUpdModalInput.value = '';
            ownerUpdModalInput.focus();

            // e.preventDefault();
            // e.stopPropagation();

        } else if (ownerChg !== '' && !ownerList.includes(ownerChg)) {
            ownerInvalidSpan.innerHTML = `the Owner given [ ${ownerChg} ] does NOT exist in the system`;
            ownerInvalidSpan.className = 'invalid-feedback';

            ownerUpdBtn.classList.add('disabled');

            ownerUpdModalInput.setCustomValidity(`the Owner given [ ${ownerChg} ] does NOT exist in the system`);
            ownerUpdModalInput.value = '';
            ownerUpdModalInput.focus();

            // e.preventDefault();
            // e.stopPropagation();

        } else {
            ownerInvalidSpan.innerHTML = "";
            ownerUpdModalInput.setCustomValidity("");
            ownerUpdBtn.classList.remove('disabled');
        }
    }

    // hostname Upd Input Verify
    const hostnameUpdModal = document.getElementById('hostnameUpdModal');
    const hostnameUpdModalInput = document.getElementById('hostnameUpdModalInput');

    hostnameUpdModal.addEventListener('shown.bs.modal', () => hostnameUpdModalInput.focus());

    hostnameUpdModalInput.addEventListener('focusout', (e) => hostnameCheck(e));
    hostnameUpdModalInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            hostnameCheck(e);
        }
    });
    
    function hostnameCheck(e) {
        const hostnameInvalidSpan = document.querySelector('#hostnameInvalidSpan');
        const hostnameUpdBtn = document.querySelector('#hostnameUpdBtn');
        const hostnameListDataSet = hostnameUpdModal.dataset.hostnameList;
        const hostnameList = hostnameListDataSet.replace(/[\[\]']/g, '').split(', ');

        if (hostnameUpdModalInput.value.trim() === '' || hostnameList.includes(hostnameUpdModalInput.value.trim())) {
            hostnameInvalidSpan.innerHTML = `the Hostname given [ ${hostnameUpdModalInput.value} ] is Empty or already Existing`;
            hostnameInvalidSpan.className = 'invalid-feedback';

            hostnameUpdBtn.classList.add('disabled');

            hostnameUpdModalInput.setCustomValidity(`the Hostname given [ ${hostnameUpdModalInput.value} ] is Empty or already Existing`);
            hostnameUpdModalInput.value = '';
            hostnameUpdModalInput.focus();
            
        } else {
            hostnameInvalidSpan.innerHTML = "";
            hostnameUpdModalInput.setCustomValidity("");
            hostnameUpdBtn.classList.remove('disabled');
        }

    }
})()