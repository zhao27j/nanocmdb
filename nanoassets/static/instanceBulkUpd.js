import { formsValidation } from './modalFormsValidation.js';
// import {modalLable, modalInputTag, getLstUri, optLst, chkLst, postUpdUri, bulkUpdModal, instanceSelected, instanceSelectedPk} from './instanceBulkUpdBranchSite.js'
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import {modalInputChk} from './modalInputChk.js';

'use strict'

// Instance Bulk Update

let modalLable, modalInputTag, getLstUri, optLst, chkLst, postUpdUri, instanceSelected, instanceSelectedPk;

const bulkUpdModal = document.querySelector('#bulkUpdModal');
const bulkUpdModalInstance = bootstrap.Modal.getOrCreateInstance('#bulkUpdModal');
const bulkUpdModalForm = document.querySelector('#bulkUpdModalForm');
const csrftoken = bulkUpdModalForm.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
const bulkUpdModalInput = document.querySelector('#bulkUpdModalInput');
const bulkUpdModalDatalist = document.querySelector('#bulkUpdModalDatalist');
const bulkUpdModalBtn = document.querySelector('#bulkUpdModalBtn');

bulkUpdModal.addEventListener('show.bs.modal', (e) => {

    if (e.relatedTarget.innerHTML.includes('Associate with')) {
        modalLable = 'Associated with ...';
        modalInputTag = 'Contract';

        getLstUri = window.location.origin + '/json_response/contract_lst/';
        postUpdUri = window.location.origin + '/instance/contract_associating_with/';
    } else if (e.relatedTarget.innerHTML.includes('Transfer to')) {
        modalLable = 'Transfer to ...';
        modalInputTag = 'branchSite';

        getLstUri = window.location.origin + '/json_response/branchSite_lst/';
        postUpdUri = window.location.origin + '/instance/branchSite_transferring_to/';
    }
    bulkUpdModal.querySelector('#bulkUpdModalLabel').innerHTML = modalLable;
    instanceSelectedPk = [];
    instanceSelected = document.querySelectorAll("input[type='checkbox']:checked");
    if (instanceSelected.length > 0) {

        instanceSelected.forEach( i => {instanceSelectedPk.push(i.value);})

        getLstUri += `?instanceSelectedPk=${instanceSelectedPk}`

        fetch(getLstUri
            ).then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(json => {
                optLst = json[0];
                chkLst = json[1];
            }).catch(error => {console.error('Error:', error);})

    } /*else {
        baseMessagesAlert(`no IT Assets is selected`, 'warning');
        bulkUpdModalInstance.hide();
    }*/
})

bulkUpdModal.addEventListener('shown.bs.modal', () => {
    if (instanceSelected.length > 0) {
        if ( bulkUpdModalDatalist.querySelectorAll('option').length > 0 ) {
            while (bulkUpdModalDatalist.querySelector('option')) {
                bulkUpdModalDatalist.removeChild(bulkUpdModalDatalist.querySelector('option'))
            }
        }

        Object.keys(optLst).forEach(key => {
            const dataListOpt = document.createElement('option');
            dataListOpt.textContent = key;
            bulkUpdModalDatalist.appendChild(dataListOpt);
        })

        bulkUpdModalInput.focus();
        bulkUpdModalBtn.classList.add('disabled');
    } else {
        baseMessagesAlert(`no IT Assets is selected`, 'warning');
        bulkUpdModalInstance.hide();
    }
}, {});

const bulkUpdModalInputCtrl = new AbortController();
bulkUpdModalInput.addEventListener('focusout', (e) => {modalInputChk(e, optLst, chkLst, bulkUpdModal, modalInputTag);}, { signal: bulkUpdModalInputCtrl.signal });

bulkUpdModalForm.addEventListener('submit', (e) => { // listening Form Submission event
    const modalInputChkResult = modalInputChk(e, optLst, chkLst, bulkUpdModal, modalInputTag);
    if (modalInputChkResult) {
        e.preventDefault();
        bulkUpdModalInputCtrl.abort(); // remove listener from modal Input element after validation
        bulkUpdModalInstance.hide();

        const bulkUpdModalInputValue = bulkUpdModalInput.value.trim();
        const formData = new FormData();
        formData.append('bulkUpdModalInputValue', bulkUpdModalInputValue);
        formData.append('instanceSelectedPk', instanceSelectedPk);

        fetch(postUpdUri, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin', // Do not send CSRF token to another domain
            body: formData,
        }).then(response => {
            response.json();
        }).then(result => {

            
            baseMessagesAlert(`the selected IT Asset(s) [ ${instanceSelectedPk} ] were associated with [ ${bulkUpdModalInputValue} ]`, 'success');

            instanceSelected.forEach( i => {
                const instanceBulkUpdEl = document.querySelector(`#instance${modalInputTag}${i.id.split('instance')[1]}`);
                if (!instanceBulkUpdEl.querySelector('a')) {
                    instanceBulkUpdEl.querySelector('small').remove();
                }
                const instanceBulkUpdElHyperLink = instanceBulkUpdEl.appendChild(document.createElement('a'));
                instanceBulkUpdElHyperLink.href = window.location.origin + optLst[bulkUpdModalInputValue];
                instanceBulkUpdElHyperLink.className = "text-decoration-none";

                instanceBulkUpdElHyperLink.appendChild(document.createElement('small')).innerHTML = bulkUpdModalInputValue;

                i.checked = false; // uncheck
            });

            console.log('Success:', result);
        }).catch(error => {console.error('Error:', error)})
    }
});
