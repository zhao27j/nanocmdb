import { formsValidation } from './modalFormsValidation.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import {modalInputChk} from './modalInputChk.js';

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

let instancesSelected;
contractUpdModal.addEventListener('shown.bs.modal', () => {
    instancesSelected = document.querySelectorAll("input[type='checkbox']:checked");
    if (instancesSelected.length > 0) {
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
contractUpdModalInput.addEventListener('focusout', (e) => modalInputChk(e, contract_list, contractUpdModal, 'Contract'), { signal: contractUpdModalInputCtrl.signal });

contractUpdModalForm.addEventListener('submit', (e) => { // listening Form Submission event

    if (modalInputChk(e, contract_list, contractUpdModal, 'Contract')) {
        e.preventDefault();
        contractUpdModalInputCtrl.abort(); // remove listener from modal Input element after validation
        contractUpdModalInstance.hide();

        let instanceSelectedPost = [];
        instancesSelected.forEach( i => {
            instanceSelectedPost.push(i.value);
        });

        const contractUpdModalInputValue = contractUpdModalInput.value.trim();
        const formData = new FormData();
        formData.append('contract_associated_with', contractUpdModalInputValue);
        formData.append('instanceSelectedPost', instanceSelectedPost);

        const instanceContractAssociatedWithUriDataSet = contractUpdModal.dataset.instanceContractAssociatedWithUri;
        fetch(instanceContractAssociatedWithUriDataSet, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin', // Do not send CSRF token to another domain
            body: formData,
        }).then(response => {
            response.json();
        }).then(result => {
            baseMessagesAlert(`the selected IT Asset(s) [ ${instanceSelectedPost} ] were associated with [ ${contractUpdModalInputValue} ]`, 'success');

            instancesSelected.forEach( i => {
                const instanceAssociatedContract = document.querySelector(`#instanceAssociatedContract${i.id.split('instance')[1]}`);
                if (!instanceAssociatedContract.querySelector('a')) {
                    instanceAssociatedContract.querySelector('small').remove();
                }
                const instanceAssociatedContractHyperLink = instanceAssociatedContract.appendChild(document.createElement('a'));
                instanceAssociatedContractHyperLink.href = window.location.origin + contract_list[contractUpdModalInputValue];
                instanceAssociatedContractHyperLink.className = "text-decoration-none";

                instanceAssociatedContractHyperLink.appendChild(document.createElement('small')).innerHTML = contractUpdModalInputValue;
            });

            console.log('Success:', result);
        }).catch(error => {console.error('Error:', error)})
    }
});
