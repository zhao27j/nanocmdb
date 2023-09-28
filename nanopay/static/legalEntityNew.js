import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import {modalInputChk} from './modalInputChk.js';

// import {modalInputChk} from '../static/nanopay/'

'use strict'

// new Legal Entity

const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const newLegalEntityModal = document.querySelector('#newLegalEntityModal');

let modalLbl, modalInputTag, getLstUri, postUpdUri, legalEntity, legalEntityOptLst, projectOptLst, contactOptLst;

newLegalEntityModal.addEventListener('show.bs.modal', (e) => {
    // modalLbl = '';
    getLstUri = window.location.origin + '/json_response/legalEntity_getLst/';

    if (e.relatedTarget.innerHTML.includes('New Legal Entity')) {
        modalInputTag = 'newLegalEntity';
    } else {
        modalInputTag = 'updLegalEntity';
        getLstUri += `?legalEntityPk=${e.relatedTarget.id}`;
    }

    postUpdUri = window.location.origin + '/legal_entity/new/';

    fetch(getLstUri
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).then(json => {
        legalEntity = json[0];
        legalEntityOptLst = json[1];
        projectOptLst = json[2];
        contactOptLst = json[3];
    }).catch(error => {console.error('Error:', error);})
})

const newLegalEntityModalInputName = newLegalEntityModal.querySelector('#newLegalEntityModalInputName');
const newLegalEntityModalInputType = newLegalEntityModal.querySelector('#newLegalEntityModalInputType');
const newLegalEntityModalInputCode = newLegalEntityModal.querySelector('#newLegalEntityModalInputCode');
const newLegalEntityModalInputPrjct = newLegalEntityModal.querySelector('#newLegalEntityModalInputPrjct');
const newLegalEntityModalInputDepositBank = newLegalEntityModal.querySelector('#newLegalEntityModalInputDepositBank');
const newLegalEntityModalInputDepositBankAccount = newLegalEntityModal.querySelector('#newLegalEntityModalInputDepositBankAccount');
const newLegalEntityModalInputTax = newLegalEntityModal.querySelector('#newLegalEntityModalInputTax');
const newLegalEntityModalInputRegAddr = newLegalEntityModal.querySelector('#newLegalEntityModalInputRegAddr');
const newLegalEntityModalInputRegPhone = newLegalEntityModal.querySelector('#newLegalEntityModalInputRegPhone');
const newLegalEntityModalInputPostalAddr = newLegalEntityModal.querySelector('#newLegalEntityModalInputPostalAddr');
const newLegalEntityModalInputContact = newLegalEntityModal.querySelector('#newLegalEntityModalInputContact');

const newLegalEntityModalBtn = newLegalEntityModal.querySelector('#newLegalEntityModalBtn');
const newLegalEntityModalBtnSubmit = newLegalEntityModal.querySelector('#newLegalEntityModalBtnSubmit');

let dblClickedEl = null, dblClickedElInnerHTML, dblClickedInstancePk, instanceSelected, instanceSelectedPk;

const inputChkResults = new Map();
function respondToLegalEntityTypeSwitcher(switchElValue) {
    newLegalEntityModal.querySelectorAll(".border-danger, .border-success").forEach(el => {
        ['text-danger', 'border-bottom', 'border-danger', 'border-success'].forEach(t => el.classList.remove(t));
        el.nextElementSibling.innerHTML = "";
    })
    newLegalEntityModalBtn.classList.add('disabled');
    inputChkResults.clear();
    if (switchElValue.checked){
        newLegalEntityModal.querySelector("p.card-text").innerHTML = '- Internal -';
        [newLegalEntityModalInputCode, newLegalEntityModalInputContact].forEach(i => {
            i.closest("[class^='row']").style.display = 'none';
            i.value = '';
            i.placeholder = '';
        })
        newLegalEntityModalInputPrjct.closest("[class^='row']").style.display = '';

        newLegalEntityModalInputPrjct.placeholder = 'required ...';
        newLegalEntityModalInputTax.placeholder = 'required ...';

        newLegalEntityModalInputDepositBank.placeholder = '';
        newLegalEntityModalInputDepositBankAccount.placeholder = '';

        // chkResults = {'Type': 'I', 'Name': false, 'Project': false, 'Tax #': false};
        inputChkResults.set('Type', 'I');
        inputChkResults.set('Name', false);
        inputChkResults.set('Project', false);
        inputChkResults.set('Tax #', false);
    } else {
        newLegalEntityModal.querySelector("p.card-text").innerHTML = '- External -';
        [newLegalEntityModalInputCode, newLegalEntityModalInputContact].forEach(i => {
            i.closest("[class^='row']").style.display = '';
            i.placeholder = 'required ...';
        })
        newLegalEntityModalInputPrjct.closest("[class^='row']").style.display = 'none';
        newLegalEntityModalInputPrjct.value = '';

        newLegalEntityModalInputPrjct.placeholder = '';
        newLegalEntityModalInputTax.placeholder = '';

        newLegalEntityModalInputDepositBank.placeholder = 'required ...';
        newLegalEntityModalInputDepositBankAccount.placeholder = 'required ...';

        // chkResults = {'Type': 'E', 'Name': false, 'Code': false, 'Bank': false, 'Bank acc': false, 'Contact': false,};
        inputChkResults.set('Type', 'E');
        inputChkResults.set('Name', false);
        inputChkResults.set('Code', false);
        inputChkResults.set('Bank', false);
        inputChkResults.set('Bank acc', false);
        inputChkResults.set('Contact', false);
    }

    newLegalEntityModalInputName.focus();
    // return chkResults;
}

newLegalEntityModal.addEventListener('shown.bs.modal', () => {
    if (modalInputTag == 'updLegalEntity') {
        newLegalEntityModalInputName.value = legalEntity.name;
        legalEntity.type == 'I' ? newLegalEntityModalInputType.checked = true : newLegalEntityModalInputType.checked = false;
        // newLegalEntityModalInputType.value = legalEntity.type;
        newLegalEntityModalInputCode.value = legalEntity.code;
        newLegalEntityModalInputPrjct.value = legalEntity.prjct;

        newLegalEntityModalInputDepositBank.value = legalEntity.deposit_bank;
        newLegalEntityModalInputDepositBankAccount.value = legalEntity.deposit_bank_account;

        newLegalEntityModalInputRegAddr.value = legalEntity.reg_addr;
        newLegalEntityModalInputRegPhone.value = legalEntity.reg_phone;
        newLegalEntityModalInputPostalAddr.value = legalEntity.postal_addr;

    }
    respondToLegalEntityTypeSwitcher(newLegalEntityModalInputType);

    newLegalEntityModal.querySelectorAll('option').forEach(el =>{el.remove();})
    
    const newLegalEntityModalInputPrjctDatalist = newLegalEntityModal.querySelector('#newLegalEntityModalInputPrjctDatalist');
    Object.keys(projectOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        newLegalEntityModalInputPrjctDatalist.appendChild(datalistOpt);
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
    newLegalEntityModalBtnSubmit.style.display = 'none';
}, {});

newLegalEntityModal.querySelector("input[type='checkbox']").addEventListener('change', e => { respondToLegalEntityTypeSwitcher(e.target) });

newLegalEntityModalBtn.addEventListener('click', e => {
    newLegalEntityModal.querySelectorAll(".border-danger, .border-success").forEach(el => {
        ['text-danger', 'border-bottom', 'border-danger', 'border-success'].forEach(t => el.classList.remove(t));
        el.nextElementSibling.innerHTML = "";
    })
    if (e.target.innerHTML == 'next') {
        newLegalEntityModal.querySelector("textarea[type='text']").disabled = true;
        newLegalEntityModal.querySelectorAll("input").forEach(el => el.disabled = true);
        e.target.innerHTML = 'back';
        newLegalEntityModalBtnSubmit.style.display = '';
    } else if (e.target.innerHTML == 'back') {
        newLegalEntityModal.querySelector("textarea[type='text']").disabled = false;
        newLegalEntityModal.querySelectorAll("input").forEach(el => el.disabled = false);
        e.target.innerHTML = 'next';
        newLegalEntityModalBtnSubmit.style.display = 'none';
    }
})

newLegalEntityModalInputName.addEventListener('blur', e => { // 下次再说
    if (e.target.value != legalEntity.name) {
        inputChk(e.target, 'Name', false, legalEntityOptLst, newLegalEntityModalBtn, true, true);
    } else {
        const legalEntityUpdLst = {};
        legalEntityUpdLst[legalEntity.name] = 0;
        inputChk(e.target, 'Name', true, legalEntityUpdLst, newLegalEntityModalBtn, true, true);
    }
});

newLegalEntityModalInputCode.addEventListener('blur', e => inputChk(e.target, 'Code', false, null, newLegalEntityModalBtn, true, true));
newLegalEntityModalInputPrjct.addEventListener('blur', e => inputChk(e.target, 'Project', true, projectOptLst, newLegalEntityModalBtn, false, true));

newLegalEntityModalInputTax.addEventListener('blur', e => { if (inputChkResults.get('Type') == 'I') { inputChk(e.target, 'Tax #', false, null, newLegalEntityModalBtn, true, true);}});
newLegalEntityModalInputDepositBank.addEventListener('blur', e => { if (inputChkResults.get('Type') == 'E') { inputChk(e.target, 'Bank', false, null, newLegalEntityModalBtn, true, true);}});
newLegalEntityModalInputDepositBankAccount.addEventListener('blur', e => { if (inputChkResults.get('Type') == 'E') { inputChk(e.target, 'Bank acc', false, null, newLegalEntityModalBtn, true, true);}});
newLegalEntityModalInputContact.addEventListener('blur', e => { if (inputChkResults.get('Type') == 'E') { inputChk(e.target, 'Contact', true, contactOptLst, newLegalEntityModalBtn, false, true);}});

newLegalEntityModalBtn.addEventListener('focus', e => {

    inputChk(newLegalEntityModalInputName, 'Name', false, legalEntityOptLst, newLegalEntityModalBtn, true, true);
    
    if (newLegalEntityModal.querySelector("input[type='checkbox']").checked) {
        inputChk(newLegalEntityModalInputPrjct, 'Project', true, projectOptLst, newLegalEntityModalBtn, false, true);
        
        inputChk(newLegalEntityModalInputTax, 'Tax #', false, null, newLegalEntityModalBtn, true, true);
    } else {
        inputChk(newLegalEntityModalInputCode, 'Code', false, null, newLegalEntityModalBtn, true, true);

        inputChk(newLegalEntityModalInputDepositBank, 'Bank', false, null, newLegalEntityModalBtn, true, true);
        inputChk(newLegalEntityModalInputDepositBankAccount, 'Bank acc', false, null, newLegalEntityModalBtn, true, true);
        inputChk(newLegalEntityModalInputContact, 'Contact', true, contactOptLst, newLegalEntityModalBtn, false, true);
    }
    
    // e.target.classList.toggle('disabled', !Array.from(inputChkResults.values()).every((element, index, array) => {return element != false;}));
    /*
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
    */
})

function inputChk(inputEl, inputLbl, isOptLst, optLst, btn, isAlphanumeric, reqd ) {
    let inputValue, chkAlert, chkAlertType, inputChkResult = true;

    if (isAlphanumeric) {
        inputValue = inputEl.value.trim().replaceAll(/[`~!@#$%^&*()+=\[\]\\{}|;':",./<>? ·~！@#￥%……&*（）——+=【】、{}|；‘：“，。、《》？ ]/g,'');
        inputEl.value = inputValue;
    } else {
        inputValue = inputEl.value;
    }

    if (inputChkResult && reqd && inputValue == '') {
        chkAlert = `the given ${inputLbl} [ ${inputValue} ] is Empty`;
        inputChkResult = false;
    }

    if (inputChkResult && isOptLst && optLst && !(inputValue in optLst)) {
        chkAlert = `the given ${inputLbl} [ ${inputValue} ] does NOT exist in the Option List`;
        inputChkResult = false;
    } else if (inputChkResult && !isOptLst && optLst && (inputValue in optLst)) {
        chkAlert = `the given ${inputLbl} [ ${inputValue} ] does Exist in the System`;
        inputChkResult = false;
    }

    ['text-danger', 'border-bottom', 'border-danger'].forEach(t => inputEl.classList.toggle(t, !inputChkResult));
    ['border-success'].forEach(t => inputEl.classList.toggle(t, inputChkResult));

    inputChkResult ? inputEl.nextElementSibling.innerHTML = "" : inputEl.nextElementSibling.innerHTML = chkAlert;

    /*
    setTimeout(() => {
        ['text-danger', 'border-bottom', 'border-danger'].forEach(t => inputEl.classList.remove(t));
        inputEl.nextElementSibling.innerHTML = "";
    }, 3000); // clear Alert in 3000ms
    */

    inputChkResults.set(inputLbl, inputChkResult);
    btn.classList.toggle('disabled', !Array.from(inputChkResults.values()).every((element, index, array) => {return element != false;}));
    
    return inputChkResult;
}

newLegalEntityModalBtnSubmit.addEventListener('click', e => {
    const csrftoken = newLegalEntityModal.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
    const formData = new FormData();
    formData.append('name', newLegalEntityModalInputName.value);
    formData.append('type', inputChkResults.get('Type'));
    formData.append('prjct', newLegalEntityModalInputPrjct.value);
    formData.append('code', newLegalEntityModalInputCode.value);
    formData.append('deposit_bank', newLegalEntityModalInputDepositBank.value);
    formData.append('deposit_bank_account', newLegalEntityModalInputDepositBankAccount.value);
    formData.append('tax_number', newLegalEntityModalInputTax.value);
    formData.append('reg_addr', newLegalEntityModal.querySelector('#newLegalEntityModalInputRegAddr').value.trim());
    formData.append('reg_phone', newLegalEntityModal.querySelector('#newLegalEntityModalInputRegPhone').value.trim());
    formData.append('postal_addr', newLegalEntityModal.querySelector('#newLegalEntityModalInputContact').value.trim());
    formData.append('contact', newLegalEntityModalInputContact.value);

    fetch(postUpdUri, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // do not send CSRF token to another domain
        body: formData,
    }).then(response => {
        response.json();
    }).then(result => {
        bootstrap.Modal.getOrCreateInstance('#newLegalEntityModal').hide();
        // newLegalEntityModalNextInstance.hide();
        baseMessagesAlert(`1 x new Legal Entity [${newLegalEntityModalInputName.value} ] was added`, 'info');
    }).catch(error => {console.error('Error:', error)})
})

const newLegalEntityModalNext = document.querySelector('#newLegalEntityModalNext');
const newLegalEntityModalNextInstance = bootstrap.Modal.getOrCreateInstance('#newLegalEntityModalNext');
// const newLegalEntityModalForm = newLegalEntityModal.querySelector('#newLegalEntityModalForm');
const newLegalEntityModalNextTbl = newLegalEntityModalNext.querySelector('table');

let newLegalEntityModalInputNameValue, isDefaultHostname;

newLegalEntityModalNext.addEventListener('shown.bs.modal', () => {
    newLegalEntityModalNext.querySelector('#newModelTypeValueModalNext').innerHTML = newLegalEntityModalInputCode.value;
    newLegalEntityModalNext.querySelector('#newBranchSiteValueModalNext').innerHTML = newLegalEntityModalInputDepositBank.value;
    newLegalEntityModalNext.querySelector('#newContractValueModalNext').innerHTML = newLegalEntityModalInputDepositBankAccount.value;

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
            `<td><small>${newLegalEntityModalInputPrjct.value == '' ? 'Available' : 'in Use'}</small></td>`,
            `<td><small>${newLegalEntityModalInputPrjct.value == '' ? '🈳' : newLegalEntityModalInputPrjct.value}</small></td>`
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
        
        
    // }
})
