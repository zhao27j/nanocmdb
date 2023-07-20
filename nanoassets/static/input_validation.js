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

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // page level Alert Msg
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
    const appendAlert = (message, type) => {
        const wrapper = document.createElement('div');
        wrapper.innerHTML = [
            `<div class="alert alert-${type} alert-dismissible" role="alert">`,
            `   <div>${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
        ].join('')

        // alertPlaceholder.append(wrapper);
        alertPlaceholder.firstChild ? alertPlaceholder.replaceChild(wrapper, alertPlaceholder.firstChild) : alertPlaceholder.appendChild(wrapper);
    }

    // owner Upd input validation
    const ownerUpdModal = document.querySelector('#ownerUpdModal');
    const ownerUpdModalForm = document.querySelector('#ownerUpdModalForm');
    const ownerUpdModalInput = document.querySelector('#ownerUpdModalInput');
    const ownerUpdModalDataList = document.querySelector('#ownerUpdModalDataList');
    const ownerUpdModalBtn = document.querySelector('#ownerUpdModalBtn');
    const ownerUpdModalInvalidSpan = document.querySelector('#ownerUpdModalInvalidSpan');

    const instanceOwnerDataSet = ownerUpdModal.dataset.instanceOwner;

    let owner_list
    const jsonResponseOwnerListDataSet = ownerUpdModal.dataset.jsonresponseOwnerList;
    fetch(jsonResponseOwnerListDataSet //  'http://127.0.0.1:8000/json_response/owner_list'
        ).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(`HTTP error: ${response.status}`);
            }
        }).then(
            json => owner_list = json
        ).catch(error => {console.error('Error:', error);})

    ownerUpdModal.addEventListener('shown.bs.modal', () => {
        ownerUpdModalInput.focus();
        ownerUpdModalBtn.classList.add('disabled');

        if ( ownerUpdModalDataList.querySelectorAll('option').length == 0 ) {
            Object.keys(owner_list).forEach(key => {
                const dataListOpt = document.createElement('option');
                dataListOpt.textContent = key;
                ownerUpdModalDataList.appendChild(dataListOpt);
            })}
    }, {});

    ownerUpdModalForm.addEventListener('submit', (e) => {
        if (ownerChk(e)) {
            e.preventDefault();

            const ownerUpdModalInstance = bootstrap.Modal.getInstance('#ownerUpdModal');
            ownerUpdModalInstance.hide();

            if (ownerUpdModalInput.value != '') {
                document.querySelector('#instance_status').innerHTML = 'in Use';
                document.querySelector('#instance_owner').innerHTML = ownerUpdModalInput.value;

                appendAlert(`the IT Assets was Re-assign to ${ownerUpdModalInput.value} from ${instanceOwnerDataSet == '' ? "🈳" : instanceOwnerDataSet}`, 'success');

            } else {
                document.querySelector('#instance_status').innerHTML = 'Available';
                document.querySelector('#instance_owner').innerHTML = "🈳";

                appendAlert(`the IT Assets was Returned from ${instanceOwnerDataSet}`, 'success');
            }

            const formData = new FormData();
            formData.append('owner_re_assign_to', ownerUpdModalInput.value);
            // formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

            const submissionInstanceOwnerUpdDataSet = ownerUpdModal.dataset.submissionInstanceOwnerUpd;
            fetch(submissionInstanceOwnerUpdDataSet, {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin', // Do not send CSRF token to another domain
                body: formData,
            }).then(response => response.json()
            ).then(result => {
                console.log('Success:', result);
                
            }).catch(error => {console.error('Error:', error);})
        }
    });
    /*
    ownerUpdModalInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            ownerChk(e);
        }
    });
    */
    ownerUpdModalInput.addEventListener('blur', (e) => ownerChk(e));

    function ownerChk(e) {
        /* 
        const ownerListDataSet = ownerUpdModal.dataset.ownerList;
        const ownerList = ownerListDataSet.replace(/[\[\]']/g, '').split(', ');
        let owners = [];
        ownerList.forEach(owner => {
            owners.push(owner.split("(")[0].trim());
        });
        */
        // const ownerChg = ownerUpdModalInput.value.trim().split("(")[0].trim();
        const ownerChg = ownerUpdModalInput.value.trim();
        if (ownerChg.split("(")[0].trim() === instanceOwnerDataSet) {
            ownerUpdModalInvalidSpan.innerHTML = `the Owner given [ ${ownerChg} ] looks no Change`;
            ownerUpdModalInvalidSpan.className = 'invalid-feedback';

            appendAlert(`the Owner [ ${ownerChg} ] given looks no Change`, 'warning');

            ownerUpdModalBtn.classList.add('disabled');

            ownerUpdModalInput.setCustomValidity(`the Owner given [ ${ownerChg} ] is the same as the orginal`);
            ownerUpdModalInput.value = '';
            ownerUpdModalInput.focus();

            e.preventDefault();
            e.stopPropagation();
            return false;

        } else if (ownerChg !== '' && !(ownerChg in owner_list)) {
            ownerUpdModalInvalidSpan.innerHTML = `the Owner given [ ${ownerChg} ] does NOT exist in the list`;
            ownerUpdModalInvalidSpan.className = 'invalid-feedback';

            appendAlert(`the Owner [ ${ownerChg} ] given does NOT exist in the list`, 'warning');

            ownerUpdModalBtn.classList.add('disabled');

            ownerUpdModalInput.setCustomValidity(`the Owner given [ ${ownerChg} ] does NOT exist in the list`);
            ownerUpdModalInput.value = '';
            ownerUpdModalInput.focus();

            e.preventDefault();
            e.stopPropagation();
            return false;

        } else {
            ownerUpdModalInvalidSpan.innerHTML = "";
            ownerUpdModalInput.setCustomValidity("");
            ownerUpdModalBtn.classList.remove('disabled');

            return true;
        }
    }
})()

// hostname Upd input validation
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
