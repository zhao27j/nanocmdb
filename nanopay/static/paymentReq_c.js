import { getJsonResponseApiData } from './getJsonResponseApiData.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

const paymentReqModal = document.querySelector('#paymentReqModal');

let paymentTermPk, paymentTermDetails, nPE_lst, inputChkResults;

paymentReqModal.addEventListener('show.bs.modal', (e) => {
    paymentTermPk = e.relatedTarget.id;
    async function getDetailsAsync() {
        try {
            const getUri = window.location.origin + `/json_respone/paymentReq_getLst/?paymentTermPk=${paymentTermPk}`;
            const json = await getJsonResponseApiData(getUri);
            if (json) {
                // paymentTermDetails = new Map(Object.entries(json[0]));
                paymentTermDetails = json[0];
                // nPE_lst = new Map(Object.entries(json[1]));
                nPE_lst = json[1];

                baseMessagesAlert("non Payroll Expense data is ready", 'success');
            } else {
                baseMessagesAlert("non Payroll Expense data is NOT ready", 'danger');
            }
        } catch (error) {
            console.error('There was a problem with the async operation:', error);
        }
    }
    getDetailsAsync();
});

const paymentReqModalLabel = paymentReqModal.querySelector('#paymentReqModalLabel');
const amount = paymentReqModal.querySelector('#amount');
const nPE = paymentReqModal.querySelector('#non_payroll_expense');

const scanned_copy = paymentReqModal.querySelector('#scanned_copy');

function initModal(e) {
    paymentReqModalLabel.textContent = 'new Payment Request';
    
    if (e.type == 'shown.bs.modal') {
        amount.value = paymentTermDetails.amount;
        nPE.value = paymentTermDetails.nPE;
        const nPEDatalist = paymentReqModal.querySelector('#nPEDatalist');
        Object.keys(nPE_lst).forEach(key => {
            const dataListOpt = document.createElement('option');
            dataListOpt.textContent = key;
            nPEDatalist.appendChild(dataListOpt);
        });
        scanned_copy.value = '';
        const progressBar = paymentReqModal.querySelector('.progress-bar');
        if (paymentTermDetails.contract_remaining > 0) {
            progressBar.classList.add('bg-info');
        } else {
            progressBar.classList.add('bg-danger');
        }
        progressBar.style.width = `${paymentTermDetails.contract_remaining}%`;
        progressBar.textContent = `${paymentTermDetails.contract_remaining}%`;
    } else {
        modalInputElAll.forEach(modalInputEl => {modalInputEl.disabled = false});
        e.target.textContent = 'next';
        submitModalBtn.classList.add('hidden');  // submitModalBtn.style.display = 'none';
    }

    inputChkResults = {
        'Amount': paymentTermDetails.amount ? true : false,
        'non Payroll Expense': paymentTermDetails.nPE ? true : false,
        'Scanned Copy': false,
    };
}

paymentReqModal.addEventListener('shown.bs.modal', e => {initModal(e)});

const modalInputElAll = Array.from(paymentReqModal.querySelector('.modal-body').querySelectorAll('input'));
const nextModalBtn = paymentReqModal.querySelector('#nextModalBtn');
const submitModalBtn = paymentReqModal.querySelector('#submitModalBtn');
modalInputElAll.forEach(m => m.addEventListener('blur', e => inputChk(e.target, nextModalBtn)));
nextModalBtn.addEventListener('focus', e => {modalInputElAll.forEach(m => inputChk(m, nextModalBtn));});
nextModalBtn.addEventListener('click', e => {
    if (e.target.textContent == 'next'){
        if (Object.values(inputChkResults).every((element, index, array) => {return element == true;})) {
            paymentReqModalLabel.textContent = 'review & confirm';
            modalInputElAll.forEach(modalInputEl => {
                ['text-danger', 'border-bottom', 'border-danger', 'border-success'].forEach(m => modalInputEl.classList.remove(m));
                modalInputEl.disabled = true;
                modalInputEl.nextElementSibling.textContent = '';
                // inputChkResults.get(`${modalInputEl.id}`) == modalInputTag ? modalInputEl.classList.add('border-success') : null;
            });
            e.target.textContent = 'back';
            submitModalBtn.classList.remove('hidden');  // submitModalBtn.style.display = '';
        }
    } else if (e.target.textContent == 'back') {initModal(e);}
})

function inputChk(inputEl, btn) {
    let inputLbl, optLst, chkAlert, chkAlertType, inputChkResult = true

    switch (inputEl.id) {
        case 'amount':
            inputLbl = 'Amount';
            optLst = null;
            break;
        case 'non_payroll_expense':
            inputLbl = 'non Payroll Expense';
            optLst = nPE_lst;
            break;
        case 'scanned_copy':
            inputLbl = 'Scanned Copy';
            optLst = null;
            break;
        default:
            optLst = null;
            break;
    }

    if (inputEl.required && inputEl.value.trim() == '') {
        chkAlert = `the given ${inputLbl} [ ${inputEl.value.trim()} ] is Empty`;
        inputChkResult = false;
    }

    if (optLst && !(inputEl.value.trim() in optLst)) {
        chkAlert = `the given ${inputLbl} [ ${inputEl.value.trim()} ] does NOT exist in the Option List`;
        inputChkResult = false;
    }

    ['text-danger', 'border-bottom', 'border-danger'].forEach(t => inputEl.classList.toggle(t, !inputChkResult));
    ['border-success'].forEach(t => inputEl.classList.toggle(t, inputChkResult));

    inputChkResult ? inputEl.nextElementSibling.innerHTML = "" : inputEl.nextElementSibling.innerHTML = chkAlert;

    inputChkResults[inputLbl] = inputChkResult;
    btn.classList.toggle('disabled', !Object.values(inputChkResults).every((element, index, array) => {return element == true;}));
    
    return inputChkResult;
}

submitModalBtn.addEventListener('click', e => {
    const postUpdUri = window.location.origin + '/payment_request/c/';
    const csrftoken = paymentReqModal.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken

    const formData = new FormData();
    formData.append('payment_term', paymentTermPk);
    
    modalInputElAll.forEach(m => {
        if (m.type == 'file') {
            // m.files.forEach((value, key, array) => formData.append(`scanned_copy_${key}`, value));
            for (let i = 0; i < m.files.length; i++) {
                formData.append('scanned_copy', m.files[i]);
            }
        } else if (m.id == 'non_payroll_expense') {
            formData.append('budgetYr', nPE_lst[m.value].split('---')[0]);
            formData.append('reforecasting', nPE_lst[m.value].split('---')[1]);
            formData.append(m.id, m.value);
        } else {
            formData.append(m.id, m.value);
        }
    })

    fetch(postUpdUri, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // do not send CSRF token to another domain
        body: formData,
    }).then(response => {
        // response.json();
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).then(json => {
        baseMessagesAlert(json.alert_msg, json.alert_type);
        baseMessagesAlertPlaceholder.addEventListener('hidden.bs.toast', () => {
            location.reload();
        });
    }).catch(error => {error ? console.error('Error:', error) : null;});
})

