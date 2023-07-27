import { formsValidation } from './formsValidation.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

// branch site Upd input validation
const branchSiteUpdModal = document.querySelector('#branchSiteUpdModal');
const branchSiteUpdModalInstance = bootstrap.Modal.getOrCreateInstance('#branchSiteUpdModal');
const branchSiteUpdModalForm = document.querySelector('#branchSiteUpdModalForm');
const csrftoken = branchSiteUpdModalForm.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
const branchSiteUpdModalInput = document.querySelector('#branchSiteUpdModalInput');
const branchSiteUpdModalDataList = document.querySelector('#branchSiteUpdModalDataList');
const branchSiteUpdModalBtn = document.querySelector('#branchSiteUpdModalBtn');
const branchSiteUpdModalInvalidSpan = document.querySelector('#branchSiteUpdModalInvalidSpan');

let branchSite_list;
const jsonResponseBranchSiteListDataSet = branchSiteUpdModal.dataset.jsonresponseBranchsiteList;
fetch(jsonResponseBranchSiteListDataSet //  'http://127.0.0.1:8000/json_response/branchSite_list'
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).then(
        json => branchSite_list = json
    ).catch(error => {console.error('Error:', error);})

let instancesChked;
branchSiteUpdModal.addEventListener('shown.bs.modal', () => {
    instancesChked = document.querySelectorAll("input[type='checkbox']:checked");
    if (instancesChked.length > 0) {
        branchSiteUpdModalInput.focus();
        branchSiteUpdModalBtn.classList.add('disabled');

        if ( branchSiteUpdModalDataList.querySelectorAll('option').length == 0 ) {
            Object.keys(branchSite_list).forEach(key => {
                const dataListOpt = document.createElement('option');
                dataListOpt.textContent = key;
                branchSiteUpdModalDataList.appendChild(dataListOpt);
            })}
    } else {
        baseMessagesAlert(`no IT Assets is selected`, 'warning');
        branchSiteUpdModalInstance.hide();
    }
}, {});

const branchSiteUpdModalInputCtrl = new AbortController();
branchSiteUpdModalInput.addEventListener('focusout', (e) => branchSiteChk(e), { signal: branchSiteUpdModalInputCtrl.signal });

branchSiteUpdModalForm.addEventListener('submit', (e) => { // listening Form Submission event

    if (branchSiteChk(e)) {
        e.preventDefault();
        branchSiteUpdModalInputCtrl.abort(); // remove listener from modal Input element after validation
        branchSiteUpdModalInstance.hide();

        const branchSiteTransferTo = branchSiteUpdModalInput.value.trim();
        let instanceChkedPost = [];
        instancesChked.forEach( i => {
            instanceChkedPost.push(i.value);
            const branchSiteDisplay = document.querySelector(`#instanceBranchSite${i.id.split('instance')[1]}`).querySelector('small')
            branchSiteDisplay.innerHTML = branchSiteTransferTo;

            console.log(i);
        });

        const formData = new FormData();
        formData.append('branchSite_transfer_to', branchSiteTransferTo);
        formData.append('instanceChkedPost', instanceChkedPost);

        const instanceBranchSiteTransferUriDataSet = branchSiteUpdModal.dataset.instanceBranchsiteTransferUri;
        fetch(instanceBranchSiteTransferUriDataSet, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin', // Do not send CSRF token to another domain
            body: formData,
        }).then(response => {
            response.json();
            baseMessagesAlert(`the selected IT Asset(s) [ ${instanceChkedPost} ] were Transferred to [ ${branchSiteTransferTo} ]`, 'success');
        }).then(result => {
            console.log('Success:', result);
        }).catch(error => {console.error('Error:', error)})
    }
});

function branchSiteChk(e) {
    const branchSiteChg = branchSiteUpdModalInput.value.trim();
    if ( !(branchSiteChg in branchSite_list) ) {
        branchSiteUpdModalInvalidSpan.innerHTML = `the given Branch Site [ ${branchSiteChg} ] does NOT exist in the list`;
        branchSiteUpdModalInvalidSpan.className = 'invalid-feedback';

        baseMessagesAlert(`the given Branch Site [ ${branchSiteChg} ] does NOT exist in the list`, 'warning');

        branchSiteUpdModalBtn.classList.add('disabled');

        branchSiteUpdModalInput.setCustomValidity(`the given Branch Site [ ${branchSiteChg} ] does NOT exist in the list`);
        branchSiteUpdModalInput.value = '';
        branchSiteUpdModalInput.focus();

        e.preventDefault();
        e.stopPropagation();

        return false;

    } else {
        baseMessagesAlert(`the given Branch Site [ ${branchSiteChg} ] is Valid`, 'info');

        branchSiteUpdModalInvalidSpan.innerHTML = "";
        branchSiteUpdModalInput.setCustomValidity("");
        branchSiteUpdModalBtn.classList.remove('disabled');

        return true;
    }
}