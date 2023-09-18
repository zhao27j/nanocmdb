import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import {modalInputChk} from './modalInputChk.js';

// import {modalInputChk} from '../static/nanopay/'

'use strict'

// new Legal Entity

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const newLegalEntityModal = document.querySelector('#newLegalEntityModal');

let modalLbl, modalInputTag, getLstUri, postUpdUri, projectOptLst, contactOptLst

newLegalEntityModal.addEventListener('show.bs.modal', () => {
    modalLbl = '';
    modalInputTag = 'newLegalEntity';
    getLstUri = window.location.origin + '/json_response/jsonResponse_legal_entity_new_lst/';
    postUpdUri = window.location.origin + '/instance/new/';

    fetch(getLstUri
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).then(json => {
        projectOptLst = json[0];
        contactOptLst = json[1];
    }).catch(error => {console.error('Error:', error);})
})

const newLegalEntityModalInputName = newLegalEntityModal.querySelector('#newLegalEntityModalInputName');
const newLegalEntityModalInputType = newLegalEntityModal.querySelector('#newLegalEntityModalInputType');
const newLegalEntityModalInputCode = newLegalEntityModal.querySelector('#newLegalEntityModalInputCode');
const newLegalEntityModalInputProject = newLegalEntityModal.querySelector('#newLegalEntityModalInputProject');
const newLegalEntityModalInputBank = newLegalEntityModal.querySelector('#newLegalEntityModalInputBank');
const newLegalEntityModalInputBankAcc = newLegalEntityModal.querySelector('#newLegalEntityModalInputBankAcc');
const newLegalEntityModalInputTax = newLegalEntityModal.querySelector('#newLegalEntityModalInputTax');
const newLegalEntityModalInputRegAddr = newLegalEntityModal.querySelector('#newLegalEntityModalInputRegAddr');
const newLegalEntityModalInputRegPhone = newLegalEntityModal.querySelector('#newLegalEntityModalInputRegPhone');
const newLegalEntityModalInputContact = newLegalEntityModal.querySelector('#newLegalEntityModalInputContact');

const newLegalEntityModalBtn = newLegalEntityModal.querySelector('#newLegalEntityModalBtn');

let dblClickedEl = null, dblClickedElInnerHTML, dblClickedInstancePk, instanceSelected, instanceSelectedPk;

newLegalEntityModal.addEventListener('shown.bs.modal', () => {
    legalEntityTypeSwitcher(newLegalEntityModalInputType);
    /*
    [newLegalEntityModalInputCode, newLegalEntityModalInputContact].forEach(i => {
        newLegalEntityModalInputType.checked ? i.closest("[class^='row']").style.display = 'none' : i.closest("[class^='row']").style.display = '';
        newLegalEntityModal.querySelector("p.card-text").innerHTML = 'Internal';
    })
    newLegalEntityModalInputType.checked ? newLegalEntityModalInputProject.closest("[class^='row']").style.display = '' : newLegalEntityModalInputProject.closest("[class^='row']").style.display = 'none';
    newLegalEntityModalInputType.checked ? newLegalEntityModal.querySelector("p.card-text").innerHTML = '- Internal -' : newLegalEntityModal.querySelector("p.card-text").innerHTML = '- External -';
    */
    newLegalEntityModal.querySelectorAll('option').forEach(el =>{el.remove();})
    
    const newLegalEntityModalInputProjectDatalist = newLegalEntityModal.querySelector('#newLegalEntityModalInputProjectDatalist');
    Object.keys(projectOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        newLegalEntityModalInputProjectDatalist.appendChild(datalistOpt);
    })

    const newLegalEntityModalInputContactDatalist = newLegalEntityModal.querySelector('#newLegalEntityModalInputContactDatalist');
    Object.keys(contactOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        newLegalEntityModalInputContactDatalist.appendChild(datalistOpt);
    })

    newLegalEntityModalInputName.focus();
    // newLegalEntityModalInputName.value = '';
    newLegalEntityModalBtn.classList.add('disabled');
}, {});

newLegalEntityModal.querySelector("input[type='checkbox']").addEventListener('change', e => { legalEntityTypeSwitcher(e.target) });

function legalEntityTypeSwitcher(switchElValue) {
    if (switchElValue.checked){
        newLegalEntityModal.querySelector("p.card-text").innerHTML = '- Internal -';
        [newLegalEntityModalInputCode, newLegalEntityModalInputContact].forEach(i => {
            i.closest("[class^='row']").style.display = 'none';
            i.value = '';
            i.placeholder = '';
        })
        newLegalEntityModalInputProject.closest("[class^='row']").style.display = '';

        newLegalEntityModalInputProject.placeholder = 'required ...';
        newLegalEntityModalInputTax.placeholder = 'required ...';

        newLegalEntityModalInputBank.placeholder = '';
        newLegalEntityModalInputBankAcc.placeholder = '';
    } else {
        newLegalEntityModal.querySelector("p.card-text").innerHTML = '- External -';
        [newLegalEntityModalInputCode, newLegalEntityModalInputContact].forEach(i => {
            i.closest("[class^='row']").style.display = '';
            i.placeholder = 'required ...';
        })
        newLegalEntityModalInputProject.closest("[class^='row']").style.display = 'none';
        newLegalEntityModalInputProject.value = '';

        newLegalEntityModalInputProject.placeholder = '';
        newLegalEntityModalInputTax.placeholder = '';

        newLegalEntityModalInputBank.placeholder = 'required ...';
        newLegalEntityModalInputBankAcc.placeholder = 'required ...';
    }
}

const inputChkResults = {
    'Serial #': false,
    'Model / Type': false,
    'Owner': true,
    'Branch Site': false,
    'Contract': false,
};

newLegalEntityModalBtn.addEventListener('keydown', e => {
    if (e.key == 'Enter'){
        if (Object.values(inputChkResults).every((element, index, array) => {return element == true;})) {
            newLegalEntityModalBtn.classList.remove('disabled');
        } else {
            newLegalEntityModalBtn.classList.add('disabled');
            e.stopPropagation();
            e.preventDefault();
            baseMessagesAlert("something Invalid", 'warning');
        }
    }
})

/*
newLegalEntityModalInputName.addEventListener('blur', e => {
    if (inputChk(e, 'Serial #', serialNumberOptLst, newLegalEntityModalBtn)) {
        if (e.target.value.replaceAll(' ', '').split(',').length > 1) {
            newLegalEntityModalInputProject.value = '';
            newLegalEntityModal.querySelector('#newOnwerModalDiv').style.display = "none";
        } else {
            newLegalEntityModal.querySelector('#newOnwerModalDiv').style.display = "flex";
        }
    }
})

newLegalEntityModalInputCode.addEventListener('blur', e => {inputChk(e, 'Model / Type', modelTypeOptLst, newLegalEntityModalBtn);})
newLegalEntityModalInputProject.addEventListener('blur', e => {inputChk(e, 'Owner', ownerOptLst, newLegalEntityModalBtn);})
newLegalEntityModalInputBank.addEventListener('blur', e => {inputChk(e, 'Branch Site', branchSiteOptLst, newLegalEntityModalBtn);})
newLegalEntityModalInputBankAcc.addEventListener('blur', e => {inputChk(e, 'Contract', contractOptLst, newLegalEntityModalBtn);})
*/

function inputChk(e, inputLbl, optLst, btn) {
    let chkAlert, chkAlertType, inputChkResult = true

    if (inputLbl == 'Serial #') {
        const serialNumberInputValue = e.target.value.replaceAll(' ', '').split(',');
        
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

    ['text-danger', 'border-bottom', 'border-danger'].forEach(t => e.target.classList.toggle(t, !inputChkResult));
    ['border-success'].forEach(t => e.target.classList.toggle(t, inputChkResult));

    inputChkResult ? e.target.nextElementSibling.innerHTML = "" : e.target.nextElementSibling.innerHTML = chkAlert;

    inputChkResults[inputLbl] = inputChkResult;
    btn.classList.toggle('disabled', !Object.values(inputChkResults).every((element, index, array) => {return element == true;}));
    
    return inputChkResult;
}

const newLegalEntityModalNext = document.querySelector('#newLegalEntityModalNext');
const newLegalEntityModalNextInstance = bootstrap.Modal.getOrCreateInstance('#newLegalEntityModalNext');
// const newLegalEntityModalForm = newLegalEntityModal.querySelector('#newLegalEntityModalForm');
const newLegalEntityModalNextTbl = newLegalEntityModalNext.querySelector('table');

let newLegalEntityModalInputNameValue, isDefaultHostname;
const formData = new FormData();

newLegalEntityModalNext.addEventListener('shown.bs.modal', () => {
    newLegalEntityModalNext.querySelector('#newModelTypeValueModalNext').innerHTML = newLegalEntityModalInputCode.value;
    newLegalEntityModalNext.querySelector('#newBranchSiteValueModalNext').innerHTML = newLegalEntityModalInputBank.value;
    newLegalEntityModalNext.querySelector('#newContractValueModalNext').innerHTML = newLegalEntityModalInputBankAcc.value;

    formData.append('model_type', newLegalEntityModalInputCode.value.split(',')[0].trim());
    formData.append('owner', newLegalEntityModalInputProject.value.trim() == '' ? '' : newLegalEntityModalInputProject.value.replaceAll(')', '').split('(')[1].trim());
    formData.append('branchSite', newLegalEntityModalInputBank.value.trim());
    formData.append('contract', newLegalEntityModalInputBankAcc.value.trim());

    newLegalEntityModalNextTbl.replaceChildren();        // newLegalEntityModalNextTbl.innerHTML = '';

    const newLegalEntityModalNextTblTh = document.createElement('tr');
    newLegalEntityModalNextTblTh.innerHTML = [
        `<th><small>Serial #</small></th>`,
        `<th><small>Hostname</small></th>`,
        `<th><small>Status</small></th>`,
        `<th><small>Owner</small></th>`
    ].join('');
    newLegalEntityModalNextTbl.appendChild(newLegalEntityModalNextTblTh);

    newLegalEntityModalInputNameValue = newLegalEntityModalInputName.value.toUpperCase().replaceAll(' ', '').split(',').filter((element, index, array) => array.indexOf(element) === index)
    formData.append('serial_number', newLegalEntityModalInputNameValue);

    newLegalEntityModalInputNameValue.forEach(i => {
        const newLegalEntityModalNextTblTd = document.createElement('tr');
        newLegalEntityModalNextTblTd.innerHTML = [
            `<td><small>${i}</small></td>`,
            `<td><small>TS-${i}</small></td>`,
            `<td><small>${newLegalEntityModalInputProject.value == '' ? 'Available' : 'in Use'}</small></td>`,
            `<td><small>${newLegalEntityModalInputProject.value == '' ? '🈳' : newLegalEntityModalInputProject.value}</small></td>`
        ].join('');
        newLegalEntityModalNextTbl.appendChild(newLegalEntityModalNextTblTd);
    })
})

newLegalEntityModalNext.querySelector("input[type='checkbox']:checked").addEventListener('change', e => {
    let i = 0, newLegalEntityModalNextTblTr = newLegalEntityModalNextTbl.querySelector('tr');
    while(newLegalEntityModalNextTblTr.nextElementSibling) {
        newLegalEntityModalNextTblTr = newLegalEntityModalNextTblTr.nextElementSibling;
        e.target.checked ? newLegalEntityModalNextTblTr.querySelector('td:nth-child(2)').innerHTML = `<small>TS-${newLegalEntityModalInputNameValue[i]}</small>` : newLegalEntityModalNextTblTr.querySelector('td:nth-child(2)').innerHTML = `<small></small>`
    
        i++;
    }
    formData.append('isDefaultHostname', e.target.checked);
})

newLegalEntityModalNext.querySelector('#newLegalEntityModalNextBtnSubmit').addEventListener('click', e => {
    // if (e.key = 'Enter') {
        const csrftoken = newLegalEntityModalNext.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
        fetch(postUpdUri, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin', // Do not send CSRF token to another domain
            body: formData,
        }).then(response => {
            response.json();
        }).then(result => {
            newLegalEntityModalNextInstance.hide();
            baseMessagesAlert(`the new IT assets [${newLegalEntityModalInputNameValue} ] were added`, 'info');
        }).catch(error => {console.error('Error:', error)})
    // }
})
