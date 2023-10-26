import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

document.addEventListener('click', e => {

})

const crudUserModal = document.querySelector('#crudUserModal');
// const crudUserModalInstance = bootstrap.Modal.getOrCreateInstance(crudUserModal);

// const csrftoken = crudUserModal.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken

// let modalLbl, modalInputTag, optLst, chkLst, postUpdUri, instanceSelected, instanceSelectedPk;

let deptOptLst, legalEntityOptLst;
const inputChkResults = new Map();

crudUserModal.addEventListener('show.bs.modal', e => {
    let getLstUri = window.location.origin + '/json_response/user_getLst/';
    
    fetch(getLstUri
        ).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(`HTTP error: ${response.status}`);
            }
        }).then(json => {
            deptOptLst = json[0];
            legalEntityOptLst = json[1];
        }).catch(error => {console.error('Error:', error);});
});

const crudUserModalEmailInput = crudUserModal.querySelector('#crudUserModalEmailInput');
const crudUserModalLastNameInput = crudUserModal.querySelector('#crudUserModalLastNameInput');
const crudUserModalFirstNameInput = crudUserModal.querySelector('#crudUserModalFirstNameInput');
const crudUserModalBtnSubmit = crudUserModal.querySelector('#crudUserModalBtnSubmit');

crudUserModal.addEventListener('shown.bs.modal', e => {
    const crudUserModalDeptInputDatalist = crudUserModal.querySelector('#crudUserModalDeptInputDatalist');
    crudUserModalDeptInputDatalist.querySelectorAll('option').forEach(el => el.remove())
    Object.keys(deptOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        crudUserModalDeptInputDatalist.appendChild(datalistOpt);
    })

    const crudUserModalLegalEntityInputDatalist = crudUserModal.querySelector('#crudUserModalLegalEntityInputDatalist');
    crudUserModalLegalEntityInputDatalist.querySelectorAll('option').forEach(el => el.remove())
    Object.keys(legalEntityOptLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        crudUserModalLegalEntityInputDatalist.appendChild(datalistOpt);
    })

    crudUserModalEmailInput.focus();
    crudUserModalBtnSubmit.classList.add('disabled');
})

crudUserModalEmailInput.addEventListener('blur', e => inputChk(e.target, true));
[crudUserModalFirstNameInput, crudUserModalLastNameInput].forEach(m => m.addEventListener('blur', e => inputChk(e.target, true)));


function inputChk(inputEl, rqurd) {
    let inputChkResult = true;

    inputEl.value = inputEl.value.trim();

    if (rqurd && inputEl.value != '') {
        if (inputEl.closest('.row').querySelector('label').textContent == 'email' && !inputEl.value.includes('@')) {
            inputEl.value += '@tishamnspeyer.com';
        }

        if (!inputEl.value.includes('@tishmanspeyer.com')) {
            inputEl.closest('.modal-body').querySelector('#crudUserModalLegalEntityInput').closest('.row').style.display = '';
        }
    } else if (rqurd && inputEl.value == '') {
        inputChkResult = false;
        inputEl.nextElementSibling.textContent = `${inputEl.closest('.row').querySelector('label').textContent} is Required`;
    }

    ['text-danger', 'border-bottom', 'border-danger'].forEach(m => inputEl.classList.toggle(m, !inputChkResult));
    ['border-success'].forEach(m => inputEl.classList.toggle(m, inputChkResult));

    inputChkResults.set(inputEl.id, inputChkResult);

    return inputChkResult;

}
