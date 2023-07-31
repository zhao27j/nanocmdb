import { formsValidation } from './formsValidation.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

// input validation - Contract Associated with
const contractUpdModal = document.querySelector('#contractUpdModal');
const contractUpdModalInstance = bootstrap.Modal.getOrCreateInstance('#contractUpdModal');
const contractUpdModalForm = document.querySelector('#contractUpdModalForm');
const csrftoken = contractUpdModalForm.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
const contractUpdModalInput = document.querySelector('#contractUpdModalInput');
const contractUpdModalDataList = document.querySelector('#contractUpdModalDataList');
const contractUpdModalBtn = document.querySelector('#contractUpdModalBtn');
const contractUpdModalInvalidSpan = document.querySelector('#contractUpdModalInvalidSpan');

let contract_list;
const jsonResponseContractListDataSet = contractUpdModal.dataset.jsonresponseContractList;
fetch(jsonResponseContractListDataSet //  'http://127.0.0.1:8000/json_response/contract_list'
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).then(
        json => contract_list = json
    ).catch(error => {console.error('Error:', error);})

let instancesChked;
contractUpdModal.addEventListener('shown.bs.modal', () => {
    instancesChked = document.querySelectorAll("input[type='checkbox']:checked");
    if (instancesChked.length > 0) {
        contractUpdModalInput.focus();
        contractUpdModalBtn.classList.add('disabled');

        if ( contractUpdModalDataList.querySelectorAll('option').length == 0 ) {
            Object.keys(contract_list).forEach(key => {
                const dataListOpt = document.createElement('option');
                dataListOpt.textContent = key;
                contractUpdModalDataList.appendChild(dataListOpt);
            })}
    } else {
        baseMessagesAlert(`no IT Assets is selected`, 'warning');
        contractUpdModalInstance.hide();
    }
}, {});

const contractUpdModalInputCtrl = new AbortController();
contractUpdModalInput.addEventListener('focusout', (e) => contractChk(e), { signal: contractUpdModalInputCtrl.signal });

contractUpdModalForm.addEventListener('submit', (e) => { // listening Form Submission event

    if (contractChk(e)) {
        e.preventDefault();
        contractUpdModalInputCtrl.abort(); // remove listener from modal Input element after validation
        contractUpdModalInstance.hide();

        const contractAssociatedWith = contractUpdModalInput.value.trim();
        let instanceChkedPost = [];
        instancesChked.forEach( i => {
            instanceChkedPost.push(i.value);

            instanceAssociatedContract = document.querySelector(`#instanceAssociatedContract${i.id.split('instance')[1]}`);
            if (document.querySelector(`#instanceAssociatedContract${i.id.split('instance')[1]}`).querySelector('a')) {
                instanceAssociatedContractHyperLink = instanceAssociatedContract.createElement('a');
                
                
            }
            const contractDisplay = document.querySelector(`#instanceContract${i.id.split('instance')[1]}`).querySelector('small')
            contractDisplay.innerHTML = contractAssociatedWith;

            console.log(i);
        });

        const formData = new FormData();
        formData.append('contract_associated_with', contractAssociatedWith);
        formData.append('instanceChkedPost', instanceChkedPost);

        const instanceContractAssociatedWithUriDataSet = contractUpdModal.dataset.instanceContractAssociatedWithUri;
        fetch(instanceContractAssociatedWithUriDataSet, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin', // Do not send CSRF token to another domain
            body: formData,
        }).then(response => {
            response.json();
            baseMessagesAlert(`the selected IT Asset(s) [ ${instanceChkedPost} ] were associated with [ ${contractAssociatedWith} ]`, 'success');
        }).then(result => {
            console.log('Success:', result);
        }).catch(error => {console.error('Error:', error)})
    }
});

function contractChk(e) {
    const contractChg = contractUpdModalInput.value.trim();
    if ( !(contractChg in contract_list) ) {
        contractUpdModalInvalidSpan.innerHTML = `the given Contract [ ${contractChg} ] does NOT exist in the list`;
        contractUpdModalInvalidSpan.className = 'invalid-feedback';

        baseMessagesAlert(`the given Contract [ ${contractChg} ] does NOT exist in the list`, 'warning');

        contractUpdModalBtn.classList.add('disabled');

        contractUpdModalInput.setCustomValidity(`the given Contract [ ${contractChg} ] does NOT exist in the list`);
        contractUpdModalInput.value = '';
        contractUpdModalInput.focus();

        e.preventDefault();
        e.stopPropagation();

        return false;

    } else {
        baseMessagesAlert(`the given Contract [ ${contractChg} ] is Valid`, 'info');

        contractUpdModalInvalidSpan.innerHTML = "";
        contractUpdModalInput.setCustomValidity("");
        contractUpdModalBtn.classList.remove('disabled');

        return true;
    }
}