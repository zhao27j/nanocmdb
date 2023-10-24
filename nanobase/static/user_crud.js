import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

document.addEventListener('click', e => {

})

const cuModal = document.querySelector('#cuModal');
// const cuModalInstance = bootstrap.Modal.getOrCreateInstance(cuModal);

const csrftoken = cuModal.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken

// let modalLbl, modalInputTag, optLst, chkLst, postUpdUri, instanceSelected, instanceSelectedPk;
let optLst;
cuModal.addEventListener('show.bs.modal', e => {
    let getLstUri = window.location.origin + '/json_response/legalEntity_getLst/';
    
    fetch(getLstUri
        ).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(`HTTP error: ${response.status}`);
            }
        }).then(json => {
            optLst = json[3];
        }).catch(error => {console.error('Error:', error);});
});

const cuModalInput = cuModal.querySelector('#cuModalInput');

const cuModalBtn = cuModal.querySelector('#cuModalBtn');

cuModal.addEventListener('shown.bs.modal', e => {

    const cuModalDatalist = cuModal.querySelector('#cuModalDatalist');
    cuModalDatalist.querySelectorAll('option').forEach(el =>{el.remove();})
    Object.keys(optLst).forEach(key => {
        const datalistOpt = document.createElement('option');
        datalistOpt.textContent = key;
        cuModalDatalist.appendChild(datalistOpt);
    })

    cuModalBtn.classList.add('disabled');

})

