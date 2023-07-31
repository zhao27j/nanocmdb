import { formsValidation } from './modalFormsValidation.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import {modalInputChk} from './modalInputChk.js';

'use strict'

// input validation - Branch Site Transferred
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

let instanceSelected;
branchSiteUpdModal.addEventListener('shown.bs.modal', () => {
    instanceSelected = document.querySelectorAll("input[type='checkbox']:checked");
    if (instanceSelected.length > 0) {
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
branchSiteUpdModalInput.addEventListener('focusout', (e) => modalInputChk(e, branchSite_list, branchSiteUpdModal, 'Branch Site'), { signal: branchSiteUpdModalInputCtrl.signal });

branchSiteUpdModalForm.addEventListener('submit', (e) => { // listening Form Submission event

    if (modalInputChk(e, branchSite_list, branchSiteUpdModal, 'Branch Site')) {
        e.preventDefault();
        branchSiteUpdModalInputCtrl.abort(); // remove listener from modal Input element after validation
        branchSiteUpdModalInstance.hide();

        const branchSiteTransferredTo = branchSiteUpdModalInput.value.trim();
        let instanceSelectedPost = [];
        instanceSelected.forEach( i => {
            instanceSelectedPost.push(i.value);
        });

        const formData = new FormData();
        formData.append('branchSite_transferred_to', branchSiteTransferredTo);
        formData.append('instanceSelectedPost', instanceSelectedPost);

        const instanceBranchSiteTransferredToUriDataSet = branchSiteUpdModal.dataset.instanceBranchsiteTransferredToUri;
        fetch(instanceBranchSiteTransferredToUriDataSet, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin', // Do not send CSRF token to another domain
            body: formData,
        }).then(response => {
            response.json();
            
        }).then(result => {
            baseMessagesAlert(`the selected IT Asset(s) [ ${instanceSelectedPost} ] were Transferred to [ ${branchSiteTransferredTo} ]`, 'success');

            instanceSelected.forEach( i => {
                const branchSiteDisplay = document.querySelector(`#instanceBranchSite${i.id.split('instance')[1]}`).querySelector('small')
                branchSiteDisplay.innerHTML = branchSiteTransferredTo;
            });
    
            console.log('Success:', result);
        }).catch(error => {console.error('Error:', error)})
    }
});
