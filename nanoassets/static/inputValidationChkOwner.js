import { formsValidation } from './formsValidation.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// owner Upd input validation
const ownerUpdModal = document.querySelector('#ownerUpdModal');
const ownerUpdModalInstance = bootstrap.Modal.getOrCreateInstance('#ownerUpdModal');
const ownerUpdModalForm = document.querySelector('#ownerUpdModalForm');
const csrftoken = ownerUpdModalForm.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
const ownerUpdModalInput = document.querySelector('#ownerUpdModalInput');
const ownerUpdModalDataList = document.querySelector('#ownerUpdModalDataList');
const ownerUpdModalBtn = document.querySelector('#ownerUpdModalBtn');
const ownerUpdModalInvalidSpan = document.querySelector('#ownerUpdModalInvalidSpan');

let dblClickedElId, dblClickedElIdPk, instanceOwner, instanceOwnerDataSet;
document.addEventListener('dblclick', e => {
    if (e.target.id !== '') {
        dblClickedElId = e.target.id;
        dblClickedElIdPk = dblClickedElId.split('instanceOwner')[1];
        if (dblClickedElId.includes('instanceOwner')) {
            instanceOwner = document.querySelector(`#${dblClickedElId}`);
            
            ownerUpdModalInstance.show();
        }
    }
});

// document.querySelector('#instanceOwnerLi').addEventListener('dblclick', () => ownerUpdModalInstance.show());

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

// ownerUpdModal.addEventListener('hidden.bs.modal', () => ownerUpdModalInputCtrl.abort()); // remove listener from modal Input element after validation

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

const ownerUpdModalInputCtrl = new AbortController();
ownerUpdModalInput.addEventListener('focusout', (e) => ownerChk(e), { signal: ownerUpdModalInputCtrl.signal });
/*
ownerUpdModalInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
        ownerChk(e);
    }
});
*/

ownerUpdModalForm.addEventListener('submit', (e) => {

    if (ownerChk(e)) {
        e.preventDefault();
        ownerUpdModalInputCtrl.abort(); // remove listener from modal Input element after validation

        ownerUpdModalInstance.hide();

        instanceOwnerDataSet = instanceOwner.dataset.instanceOwner;
        if (ownerUpdModalInput.value != '') {
            document.querySelector(`#instanceStatus-${dblClickedElIdPk}`).innerHTML = 'in Use';
            instanceOwner.querySelector('small').innerHTML = ownerUpdModalInput.value.split('(')[0].trim();

            baseMessagesAlert(`the IT Assets was Re-assigned to [ ${ownerUpdModalInput.value} ] from [ ${instanceOwnerDataSet == '' ? "🈳" : instanceOwnerDataSet} ]`, 'success');
            instanceOwnerDataSet = ownerUpdModalInput.value.split('(')[0].trim();
        } else {
            document.querySelector(`#instanceStatus-${dblClickedElIdPk}`).innerHTML = 'Available';
            instanceOwner.querySelector('small').innerHTML = "🈳";

            baseMessagesAlert(`the IT Assets was Returned from [ ${instanceOwnerDataSet} ]`, 'success');
            instanceOwnerDataSet = ownerUpdModalInput.value.split('(')[0].trim();
        }

        const formData = new FormData();
        formData.append('owner_re_assign_to', ownerUpdModalInput.value);
        // formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

        const instanceOwnerUpdUriDataSet = instanceOwner.dataset.instanceOwnerUpdUri;
        fetch(instanceOwnerUpdUriDataSet, {
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
        ownerUpdModalInvalidSpan.innerHTML = `the given Owner [ ${ownerChg} ] looks no Change`;
        ownerUpdModalInvalidSpan.className = 'invalid-feedback';

        baseMessagesAlert(`the given Owner [ ${ownerChg} ] looks no Change`, 'warning');

        ownerUpdModalBtn.classList.add('disabled');

        ownerUpdModalInput.setCustomValidity(`the given Owner [ ${ownerChg} ] looks no Change`);
        ownerUpdModalInput.value = '';
        ownerUpdModalInput.focus();

        e.preventDefault();
        e.stopPropagation();
        return false;

    } else if (ownerChg !== '' && !(ownerChg in owner_list)) {
        ownerUpdModalInvalidSpan.innerHTML = `the given Owner [ ${ownerChg} ] does NOT exist in the list`;
        ownerUpdModalInvalidSpan.className = 'invalid-feedback';

        baseMessagesAlert(`the given Owner [ ${ownerChg} ] does NOT exist in the list`, 'warning');

        ownerUpdModalBtn.classList.add('disabled');

        ownerUpdModalInput.setCustomValidity(`the given Owner [ ${ownerChg} ] does NOT exist in the list`);
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


export { ownerUpdModalInstance };