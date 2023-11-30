import { getRequesterPermissions } from './get_requester_permissions.js'
import { formsValidation } from './modalFormsValidation.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import {modalInputChk} from './modalInputChk.js';

'use strict'

// Instance Bulk Update

const bulkUpdModal = document.querySelector('#bulkUpdModal');
const bulkUpdModalInstance = bootstrap.Modal.getOrCreateInstance('#bulkUpdModal');
const bulkUpdModalForm = document.querySelector('#bulkUpdModalForm');
const csrftoken = bulkUpdModal.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
const bulkUpdModalInput = document.querySelector('#bulkUpdModalInput');
const bulkUpdModalDatalist = document.querySelector('#bulkUpdModalDatalist');
const bulkUpdModalBtn = document.querySelector('#bulkUpdModalBtn');


let is_IT_staff;
async function getRequesterPermissionsAsync() {
    try {
        const json = await getRequesterPermissions();
        if (json.is_IT_staff) {
            is_IT_staff = json.is_IT_staff;
            baseMessagesAlert("you're authorized IT staff", 'info');
        } else {
            baseMessagesAlert("you're NOT authorized IT staff", 'danger');
        }
    } catch (error) {
        console.error('There was a problem with the async operation:', error);
    }
}
getRequesterPermissionsAsync();

let dblClickedEl = null, dblClickedElInnerHTML, dblClickedInstancePk;
let modalLbl, modalInputTag, getLstUri, optLst, chkLst, postUpdUri, instanceSelected, instanceSelectedPk;
document.addEventListener('dblclick', e => { // listerning all Double Click events on the Document
    dblClickedEl = e.target.closest("[id*='Instance']");
    if (dblClickedEl) {
        dblClickedElInnerHTML = dblClickedEl.querySelector('small').innerHTML === '🈳' ? '' : dblClickedEl.querySelector('small').innerHTML;
        dblClickedInstancePk = dblClickedEl.id.split('Instance')[1];
        const dblClickedInstanceCase = dblClickedEl.id.split('Instance')[0];
        switch (dblClickedInstanceCase) {
            case 'status':
                modalLbl = 'Apply for disposal ...';
                modalInputTag = 'status';
                getLstUri = window.location.origin + '/json_response/disposal_lst/';
                postUpdUri = window.location.origin + '/instance/disposal_request/';
                bulkUpdModalInstance.show();
                break;
            case 'inRepair':
                break;
            case 'subCategory':
                if (document.querySelector(`#model_typeInstance${dblClickedInstancePk}`).querySelector('small').innerHTML != '') {
                    modalLbl = 'Re-categorize to ...';
                    modalInputTag = 'subCategory';
                    getLstUri = window.location.origin + '/json_response/sub_category_lst/';
                    postUpdUri = window.location.origin + '/instance/re_subcategorizing_to/';
                    bulkUpdModalInstance.show();
                } else {
                    baseMessagesAlert(`please apply a Model / Type to this IT Assets first`, 'warning');
                    bulkUpdModalInstance.hide();
                }
                break;
            case 'model_type':
                modalLbl = 'Change to ...';
                modalInputTag = 'model_type';
                getLstUri = window.location.origin + '/json_response/model_type_lst/';
                postUpdUri = window.location.origin + '/instance/model_type_changing_to/';
                bulkUpdModalInstance.show();
                break;
            case 'hostname':
                break;
            case 'owner':
                modalLbl = 'Re-assign to ...';
                modalInputTag = 'owner';
                getLstUri = window.location.origin + '/json_response/owner_lst/';
                postUpdUri = window.location.origin + '/instance/owner_re_assigning_to/';
                bulkUpdModalInstance.show();
                break;
            case 'branchSite':
                modalLbl = 'Transfer to ...';
                modalInputTag = 'branchSite';
                getLstUri = window.location.origin + '/json_response/branchSite_lst/';
                postUpdUri = window.location.origin + '/instance/branchSite_transferring_to/';
                bulkUpdModalInstance.show();
                break;
            case 'contract':
                modalLbl = 'Associate with ...';
                modalInputTag = 'contract';
                getLstUri = window.location.origin + '/json_response/contract_lst/';
                postUpdUri = window.location.origin + '/instance/contract_associating_with/';
                bulkUpdModalInstance.show();
                break;

        }
    }
/*
    if (e.target.closest("[id^='instanceOwner']")) {
        dblClickedEl = e.target.closest("[id^='instanceOwner']");
        dblClickedElInnerHTML = dblClickedEl.querySelector('small').innerHTML === '🈳' ? '' : dblClickedEl.querySelector('small').innerHTML; // instanceOwnerDataSet = dblClickedEl.dataset.instanceOwner;
        bulkUpdModalInstance.show();
    }
    else if (e.target.closest("[id^='instanceSubcategory']")) {
        dblClickedEl = e.target.closest("[id^='instanceSubcategory']");
        dblClickedElInnerHTML = dblClickedEl.querySelector('small').innerHTML === '🈳' ? '' : dblClickedEl.querySelector('small').innerHTML;
        if (document.querySelector(`#model_typeInstance${dblClickedEl.id.split('instanceSubcategory')[1]}`).querySelector('small').innerHTML != '') {
            bulkUpdModalInstance.show();
        } else {
            baseMessagesAlert(`please apply a Model / Type to this IT Assets first`, 'warning');
            bulkUpdModalInstance.hide();
        }
    }
    else if (e.target.closest("[id^='instancemodel_type']")) {
        dblClickedEl = e.target.closest("[id^='instancemodel_type']");
        dblClickedElInnerHTML = dblClickedEl.querySelector('small').innerHTML === '🈳' ? '' : dblClickedEl.querySelector('small').innerHTML;
        bulkUpdModalInstance.show();
    }
*/
});

bulkUpdModal.addEventListener('show.bs.modal', (e) => {

    if (e.relatedTarget) {
        dblClickedEl = undefined;
        if (e.relatedTarget.innerHTML.includes('Associate with')) {
            modalLbl = 'Associate with ...';
            modalInputTag = 'contract';
            getLstUri = window.location.origin + '/json_response/contract_lst/';
            postUpdUri = window.location.origin + '/instance/contract_associating_with/';
        }
        else if (e.relatedTarget.innerHTML.includes('Transfer to')) {
            modalLbl = 'Transfer to ...';
            modalInputTag = 'branchSite';
            getLstUri = window.location.origin + '/json_response/branchSite_lst/';
            postUpdUri = window.location.origin + '/instance/branchSite_transferring_to/';
        }
        else if (e.relatedTarget.innerHTML.includes('Apply for Disposal')) {
            modalLbl = 'Apply for disposal ...';
            modalInputTag = 'status';
            getLstUri = window.location.origin + '/json_response/disposal_lst/';
            postUpdUri = window.location.origin + '/instance/disposal_request/';
        }
    }
/*
    else {
        if (dblClickedEl.id.includes('instanceOwner')) {}
        else if (dblClickedEl.id.includes('instanceSubcategory')) {}
        else if (dblClickedEl.id.includes('instancemodel_type')) {}
    }
*/
    instanceSelectedPk = [];
    if (dblClickedEl) {
        instanceSelected = [];
        instanceSelected.push(dblClickedEl);
        instanceSelectedPk.push(dblClickedEl.id.split('Instance')[1]);
    } else {
        instanceSelected = document.querySelectorAll("td > input[type='checkbox']:checked");
        if (instanceSelected.length > 0) {
            instanceSelected.forEach( i => {instanceSelectedPk.push(i.value);})
        }
    }

    bulkUpdModal.querySelector('#bulkUpdModalLabel').innerHTML = modalLbl;
    bulkUpdModal.querySelector('span').innerHTML = instanceSelectedPk.join(', ');

    if (instanceSelectedPk.length > 0) {
        getLstUri += `?instanceSelectedPk=${instanceSelectedPk}`;

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
    }
})

bulkUpdModal.addEventListener('shown.bs.modal', () => {
    if (!is_IT_staff) {
        baseMessagesAlert("you're NOT authorized IT staff", 'danger');
        bulkUpdModalInstance.hide();
    } else if (instanceSelected.length > 0) {
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
        bulkUpdModalInput.value = '';
        bulkUpdModalBtn.classList.add('disabled');
    } else {
        baseMessagesAlert(`no IT Assets is selected`, 'warning');
        bulkUpdModalInstance.hide();
    }
}, {});

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

            instanceSelected.forEach( i => {
                if (modalInputTag == 'owner') {
                    if (bulkUpdModalInputValue == '') {
                        const msgAlert = `the IT Assets [ ${instanceSelectedPk.join(', ')} ] was Returned from [ ${dblClickedElInnerHTML} ]`;
                        document.querySelector(`#statusInstance${i.id.split('Instance')[1]}`).innerHTML = 'Available';
                    } else {
                        const msgAlert = `the IT Assets [ ${instanceSelectedPk.join(', ')} ] was Re-assigned to [ ${bulkUpdModalInputValue} ] from [ ${dblClickedElInnerHTML == '' ? "🈳" : dblClickedElInnerHTML} ]`;
                        document.querySelector(`#statusInstance${i.id.split('Instance')[1]}`).innerHTML = 'in Use';
                    }
                }
                else if (modalInputTag == 'contract') {
                    const msgAlert = `the selected IT Assets [ ${instanceSelectedPk.join(', ')} ] were Associated with [ ${bulkUpdModalInputValue} ]`;
                }
                else if (modalInputTag == 'branchSite') {
                    const msgAlert = `the selected IT Assets [ ${instanceSelectedPk.join(', ')} ] were Transfered to [ ${bulkUpdModalInputValue} ]`;
                }
                else if (modalInputTag == 'subCategory') {
                    const msgAlert = `the selected IT Assets [ ${instanceSelectedPk.join(', ')} ] was re-subCategorized to [ ${bulkUpdModalInputValue} ]`;
                }
                else if (modalInputTag == 'model_type') {
                    const msgAlert = `the Model / Type of the selected IT Assets [ ${instanceSelectedPk.join(', ')} ] was Changed to [ ${bulkUpdModalInputValue} ]`;
                }
                else if (modalInputTag == 'status') {
                    const msgAlert = `${bulkUpdModalInputValue} request for the selected IT Assets [ ${instanceSelectedPk.join(', ')} ] was sent`;
                }
                const instanceBulkUpdEl = document.querySelector(`#${modalInputTag}Instance${i.id.split('Instance')[1]}`);
                const instanceBulkUpdElHyperLink = instanceBulkUpdEl.querySelector('a');
                if (instanceBulkUpdElHyperLink) {
                    instanceBulkUpdElHyperLink.href = window.location.origin + optLst[bulkUpdModalInputValue];
                    instanceBulkUpdElHyperLink.className = "text-decoration-none";
                }
                const instanceBulkUpdElSmall = instanceBulkUpdEl.querySelector('small');
                if (instanceBulkUpdElSmall) {
                    bulkUpdModalInputValue == '' ? instanceBulkUpdElSmall.innerHTML = "🈳" : instanceBulkUpdElSmall.innerHTML = bulkUpdModalInputValue;
                }
                /*
                if (!instanceBulkUpdEl.querySelector('a')) {instanceBulkUpdEl.querySelector('small').remove();}
                const instanceBulkUpdElHyperLink = instanceBulkUpdEl.appendChild(document.createElement('a'));
                instanceBulkUpdElHyperLink.appendChild(document.createElement('small')).innerHTML = bulkUpdModalInputValue;
                */
                i.checked = false; // uncheck
            });

            baseMessagesAlert(msgAlert, 'success');
            console.log('Success:', result);
        }).catch(error => {console.error('Error:', error)})
    }
});

const bulkUpdModalInputCtrl = new AbortController();
// bulkUpdModalInput.addEventListener('change', (e) => {modalInputChk(e, optLst, chkLst, bulkUpdModal, modalInputTag);}, { signal: bulkUpdModalInputCtrl.signal });
bulkUpdModalBtn.addEventListener('focus', (e) => {modalInputChk(e, optLst, chkLst, bulkUpdModal, modalInputTag);}, { signal: bulkUpdModalInputCtrl.signal });
