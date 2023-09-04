import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import {modalInputChk} from './modalInputChk.js';

'use strict'

// Assets Bulk Update

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const newAssetsModal = document.querySelector('#newAssetsModal');
const newAssetsModalInstance = bootstrap.Modal.getOrCreateInstance('#newAssetsModal');

let modalLbl, modalInputTag, getLstUri, postUpdUri, serialNumberOptLst, modelTypeOptLst, ownerOptLst, branchSiteOptLst, contractOptLst

newAssetsModal.addEventListener('show.bs.modal', () => {
    modalLbl = '';
    modalInputTag = 'new';
    getLstUri = window.location.origin + '/json_response/jsonResponse_new_lst/';
    // postUpdUri = window.location.origin + '/instance/contract_associating_with/';

    fetch(getLstUri
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).then(json => {
        serialNumberOptLst = json[0];
        modelTypeOptLst = json[1];
        ownerOptLst = json[2];
        branchSiteOptLst = json[3];
        contractOptLst = json[4];
    }).catch(error => {console.error('Error:', error);})
})

const newSerialNumberModalInput = newAssetsModal.querySelector('#newSerialNumberModalInput');

const newModelTypeModalInput = newAssetsModal.querySelector('#newModelTypeModalInput');
const newModelTypeModalDatalist = newAssetsModal.querySelector('#newModelTypeModalDatalist');

const newOnwerModalInput = newAssetsModal.querySelector('#newOnwerModalInput');
const newOnwerModalDatalist = newAssetsModal.querySelector('#newOnwerModalDatalist');

const newBranchSiteModalInput = newAssetsModal.querySelector('#newBranchSiteModalInput');
const newBranchSiteModalDatalist = newAssetsModal.querySelector('#newBranchSiteModalDatalist');

const newContractModalInput = newAssetsModal.querySelector('#newContractModalInput');
const newContractModalDatalist = newAssetsModal.querySelector('#newContractModalDatalist');

const newAssetsModalBtn = newAssetsModal.querySelector('#newAssetsModalBtn');

let dblClickedEl = null, dblClickedElInnerHTML, dblClickedInstancePk;

let instanceSelected, instanceSelectedPk;

newAssetsModal.addEventListener('shown.bs.modal', () => {
   newAssetsModal.querySelectorAll('option').forEach(el =>{
    el.remove();
   })
    Object.keys(modelTypeOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        newModelTypeModalDatalist.appendChild(datalistOpt);
    })
    Object.keys(ownerOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        newOnwerModalDatalist.appendChild(datalistOpt);
    })
    Object.keys(branchSiteOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        newBranchSiteModalDatalist.appendChild(datalistOpt);
    })
    Object.keys(contractOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        newContractModalDatalist.appendChild(datalistOpt);
    })
    newSerialNumberModalInput.focus();
    // newSerialNumberModalInput.value = '';
    newAssetsModalBtn.classList.add('disabled');
}, {});

// const newAssetsModalForm = newAssetsModal.querySelector('#newAssetsModalForm');
// const csrftoken = newAssetsModalForm.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken


const inputChkResults = {
    'Serial #': false,
    'Model / Type': false,
    'Owner': false,
    'Branch Site': false,
    'Contract': false,
};

newAssetsModalBtn.addEventListener('keydown', e => {
    if (e.key == 'Enter'){
        if (Object.values(inputChkResults).every((element, index, array) => {return element == true;})) {
            newAssetsModalBtn.classList.remove('disabled');
        } else {
            newAssetsModalBtn.classList.add('disabled');
            e.stopPropagation();
            e.preventDefault();
            baseMessagesAlert("something Invalid", 'warning');
        }
    }
})

newSerialNumberModalInput.addEventListener('blur', e => {
    if (inputChk(e, 'Serial #', serialNumberOptLst, newAssetsModalBtn)) {
        if (e.target.value.replaceAll(' ', '').split(',').length > 1) {
            newOnwerModalInput.value = '';
            newAssetsModal.querySelector('#newOnwerModalDiv').style.display = "none";
        } else {
            newAssetsModal.querySelector('#newOnwerModalDiv').style.display = "flex";
        }
    }
})

newModelTypeModalInput.addEventListener('blur', e => {inputChk(e, 'Model / Type', modelTypeOptLst, newAssetsModalBtn);})
newOnwerModalInput.addEventListener('blur', e => {inputChk(e, 'Owner', ownerOptLst, newAssetsModalBtn);})
newBranchSiteModalInput.addEventListener('blur', e => {inputChk(e, 'Branch Site', branchSiteOptLst, newAssetsModalBtn);})
newContractModalInput.addEventListener('blur', e => {inputChk(e, 'Contract', contractOptLst, newAssetsModalBtn);})

function inputChk(e, inputLbl, optLst, btn) {
    let chkAlert, chkAlertType, inputChkResult = true

    if (inputLbl == 'Serial #') {
        const serialNumberInputValue = e.target.value.trim().replaceAll(' ', '').split(',');
        
        if (serialNumberInputValue.some((element, index, array) => {return element.trim() == ''})) {
            chkAlert = `one of the given ${inputLbl} [ ${e.target.value.trim()} ] is Empty`;
            inputChkResult = false;
        } else if (serialNumberInputValue.some((element, index, array) => {return element in optLst})) {
            chkAlert = `one of the given ${inputLbl} [ ${e.target.value.trim()} ] does Exist in the System`;
            inputChkResult = false;
        } else if (!serialNumberInputValue.every((element, index, array) => {return /^[a-zA-Z0-9-_]+$/.test(element)})) {
            chkAlert = `one of the given ${inputLbl} [ ${serialNumberInputValue} ] includes the Invalid character(s)`
            inputChkResult = false;
        }
    } else if (optLst && !(e.target.value.trim() in optLst)) {
        chkAlert = `the given ${inputLbl} [ ${e.target.value.trim()} ] does NOT exist in the Option List`;
        inputChkResult = false;
    }

    if (inputChkResult) {
        chkAlert = `the given ${inputLbl} [ ${e.target.value.trim()} ] is Valid`;
        chkAlertType = 'info';
        // newAssetsModal.querySelector("button[type='submit']").classList.remove('disabled');
        
    } else {
        chkAlertType = 'warning';
        // newAssetsModal.querySelector("button[type='submit']").classList.add('disabled');
        
        e.target.value = '';
        // e.target.focus();
        /*
        e.target.closest("form").addEventListener('submit', event => {
            event.preventDefault();
            event.stopPropagation();
        })
        */
    }

    inputChkResults[inputLbl] = inputChkResult;

    if (Object.values(inputChkResults).every((element, index, array) => {return element == true;})) {
        btn.classList.remove('disabled');
    } else {
        btn.classList.add('disabled');
    }

    e.target.setCustomValidity(chkAlert);
    baseMessagesAlert(chkAlert, chkAlertType);
    return inputChkResult;
}

