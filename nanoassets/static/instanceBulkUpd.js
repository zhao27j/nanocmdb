import { formsValidation } from './modalFormsValidation.js';
// import {modalLable, modalInputTag, getLstUri, optLst, chkLst, postUpdUri, bulkUpdModal, instanceSelected, instanceSelectedPk} from './instanceBulkUpdBranchSite.js'
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import {modalInputChk} from './modalInputChk.js';

'use strict'

// Instance Bulk Update

document.addEventListener('mouseover', e => {
    if (e.target.id.includes('instanceOwner') || (e.target.parentElement ? e.target.parentElement.id.includes('instanceOwner') : false)) {
        e.target.style.cursor = 'pointer';
        e.target.style.color = 'orange'; // 突出显示鼠标悬停目标
        setTimeout(() => { e.target.style.color = "";}, 500); // 短暂延迟后重置颜色
    }
})

const bulkUpdModal = document.querySelector('#bulkUpdModal');
const bulkUpdModalInstance = bootstrap.Modal.getOrCreateInstance('#bulkUpdModal');
const bulkUpdModalForm = document.querySelector('#bulkUpdModalForm');
const csrftoken = bulkUpdModalForm.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
const bulkUpdModalInput = document.querySelector('#bulkUpdModalInput');
const bulkUpdModalDatalist = document.querySelector('#bulkUpdModalDatalist');
const bulkUpdModalBtn = document.querySelector('#bulkUpdModalBtn');

let dblClickedElIdUniqueCode, dblClickedEl, dblClickedElInnerHTML;
document.addEventListener('dblclick', e => { // listerning all Double Click events on the Document
    if (e.target.id.includes('instanceOwner') || e.target.parentElement.id.includes('instanceOwner')) {
        dblClickedEl = e.target.id.includes('instanceOwner') ? e.target : e.target.parentElement;
        // dblClickedElIdUniqueCode = dblClickedEl.id.split('instanceOwner')[1];
        dblClickedElInnerHTML = dblClickedEl.querySelector('small').innerHTML === '🈳' ? '' : dblClickedEl.querySelector('small').innerHTML;
        // instanceOwnerDataSet = dblClickedEl.dataset.instanceOwner;

        bulkUpdModalInstance.show();
    }
});

let modalLable, modalInputTag, getLstUri, optLst, chkLst, postUpdUri, instanceSelected, instanceSelectedPk;

bulkUpdModal.addEventListener('show.bs.modal', (e) => {

    if (e.relatedTarget) {
        if (e.relatedTarget.innerHTML.includes('Associate with')) {
            modalLable = 'Associate with ...';
            modalInputTag = 'Contract';

            getLstUri = window.location.origin + '/json_response/contract_lst/';
            postUpdUri = window.location.origin + '/instance/contract_associating_with/';
        } else if (e.relatedTarget.innerHTML.includes('Transfer to')) {
            modalLable = 'Transfer to ...';
            modalInputTag = 'branchSite';

            getLstUri = window.location.origin + '/json_response/branchSite_lst/';
            postUpdUri = window.location.origin + '/instance/branchSite_transferring_to/';
        }
    } else {
        if (dblClickedEl.id.includes('instanceOwner')) {
            modalLable = 'Re-assign to ...';
            modalInputTag = 'Owner';

            getLstUri = window.location.origin + '/json_response/owner_lst/';
            postUpdUri = window.location.origin + '/instance/owner_reassigning_to/';
        }
    }

    bulkUpdModal.querySelector('#bulkUpdModalLabel').innerHTML = modalLable;
    
    instanceSelectedPk = [];
    if (dblClickedEl) {
        instanceSelected = [];
        instanceSelected.push(dblClickedEl);
        instanceSelectedPk.push(dblClickedEl.id.split('instanceOwner')[1]);
    } else {
        instanceSelected = document.querySelectorAll("input[type='checkbox']:checked");
        if (instanceSelected.length > 0) {
            instanceSelected.forEach( i => {instanceSelectedPk.push(i.value);})
        } /*else {
            baseMessagesAlert(`no IT Assets is selected`, 'warning');
            bulkUpdModalInstance.hide();
        }*/
    }
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

            instanceSelected.forEach( i => {
                if (modalInputTag == 'Owner') {
                    if (bulkUpdModalInputValue == '') {
                        baseMessagesAlert(`the IT Asset(s) [ ${instanceSelectedPk} ] was Returned from [ ${dblClickedElInnerHTML} ]`, 'success');
                        document.querySelector(`#instanceStatus${i.id.split(`instance${modalInputTag}`)[1]}`).innerHTML = 'Available';
                    } else {
                        baseMessagesAlert(`the IT Asset(s) [ ${instanceSelectedPk} ] was Re-assigned to [ ${ownerUpdModalInput} ] from [ ${dblClickedElInnerHTML == '' ? "🈳" : dblClickedElInnerHTML} ]`, 'success');
                        document.querySelector(`#instanceStatus${i.id.split('instanceOwner')[1]}`).innerHTML = 'in Use';
                    }

                } else if (modalInputTag == 'Contract') {
                    baseMessagesAlert(`the selected IT Asset(s) [ ${instanceSelectedPk} ] were associated with [ ${bulkUpdModalInputValue} ]`, 'success');
                } else if (modalInputTag == 'branchSite') {
                    baseMessagesAlert(`the selected IT Asset(s) [ ${instanceSelectedPk} ] were transfered to [ ${bulkUpdModalInputValue} ]`, 'success');
                }

                const instanceBulkUpdEl = document.querySelector(`#instance${modalInputTag}${i.id.split(`instance${modalInputTag}`)[1]}`);
                const instanceBulkUpdElHyperLink = instanceBulkUpdEl.querySelector('a');
                if (instanceBulkUpdElHyperLink) {
                    instanceBulkUpdElHyperLink.href = window.location.origin + optLst[bulkUpdModalInputValue];
                    instanceBulkUpdElHyperLink.className = "text-decoration-none";
                }
                const instanceBulkUpdElSmall = instanceBulkUpdEl.querySelector('small');
                if (instanceBulkUpdElSmall) {
                    instanceBulkUpdElSmall.innerHTML = bulkUpdModalInputValue;
                }

                // if (!instanceBulkUpdEl.querySelector('a')) {instanceBulkUpdEl.querySelector('small').remove();}
                // const instanceBulkUpdElHyperLink = instanceBulkUpdEl.appendChild(document.createElement('a'));
                // instanceBulkUpdElHyperLink.appendChild(document.createElement('small')).innerHTML = bulkUpdModalInputValue;

                i.checked = false; // uncheck
            });

            console.log('Success:', result);
        }).catch(error => {console.error('Error:', error)})
    }
});
