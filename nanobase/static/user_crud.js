import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'


const crudUserModal = document.querySelector('#crudUserModal');
const crudUserModalInst = bootstrap.Modal.getOrCreateInstance(crudUserModal);

let userProfileTblTrDblClckd, userPk;

const userProfileTbl = document.querySelector("#userProfileTbl");
document.addEventListener('dblclick', e => {
    if (userProfileTbl) {
        userProfileTblTrDblClckd = e.target.closest("tr");
        if (userProfileTblTrDblClckd.querySelector("input[type='checkbox']")) {
            userPk = userProfileTblTrDblClckd.querySelector("input[type='checkbox']").value;
            crudUserModalInst.show();
        }
    }
})

const crudUserModalInputElAll = Array.from(crudUserModal.querySelector('.modal-body').querySelectorAll('input'));
crudUserModalInputElAll.push(crudUserModal.querySelector('.modal-body').querySelector('textarea'));

let modalInputTag, isLESelected, isUserSelected, defaultEmailDomain = '@tishmanspeyer.com', deptOptLst, LEOptLst, emailOptLst, LESelected, userSelected;
const inputChkResults = new Map();

crudUserModal.addEventListener('show.bs.modal', e => {
    isLESelected = false; isUserSelected = false;

    let getLstUri = window.location.origin + '/json_response/user_getLst/';
    modalInputTag = '';
    if (e.relatedTarget && (e.relatedTarget.innerHTML.includes('New User') || e.relatedTarget.innerHTML.includes('plus'))) {
        modalInputTag = 'new';
        if (e.relatedTarget.name) {
            isLESelected = true;
            getLstUri += `?legalEntityPk=${e.relatedTarget.name}`;
        }
    } else {
        modalInputTag = 'updating';
        // getLstUri += `?legalEntityPk=${e.relatedTarget.id}`;
        isUserSelected = true;
        getLstUri += `?userPk=${userPk}`;
    }
    fetch(getLstUri
        ).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(`HTTP error: ${response.status}`);
            }
        }).then(json => {
            deptOptLst = json[0];
            LEOptLst = json[1];
            emailOptLst = json[2];
            LESelected = json[3];
            userSelected = json[4];
        }).catch(error => {console.error('Error:', error);});
});

const crudUserModalBtnSubmit = crudUserModal.querySelector('#submit');
const crudUserModalBtnOk = crudUserModal.querySelector('#ok');

function crudUserModalInitial() {
    crudUserModal.querySelector("h1.modal-title").textContent = modalInputTag

    crudUserModalInputElAll.forEach(modalInputEl => {
        // modalInputTag == 'new' ? modalInputEl.value = '' : null;
        ['text-danger', 'border-bottom', 'border-danger', 'border-success'].forEach(m => modalInputEl.classList.remove(m));
        modalInputEl.nextElementSibling.textContent = '';
        modalInputEl.disabled = false;
        modalInputEl.value = '';

        if (modalInputEl.closest('.row').querySelector('datalist')) {
            modalInputEl.closest('.row').querySelector('datalist').querySelectorAll('option').forEach(optionEl => optionEl.remove());
        }

        if (modalInputEl.id == 'dept') {
            Object.keys(deptOptLst).forEach(key => {
                const datalistOpt = document.createElement('option');
                datalistOpt.textContent = key;
                modalInputEl.closest('.row').querySelector('datalist').appendChild(datalistOpt);
            })
        }

        if (modalInputEl.id == 'legal_entity') {
            Object.keys(LEOptLst).forEach(key => {
                const datalistOpt = document.createElement('option');
                datalistOpt.textContent = key;
                modalInputEl.closest('.row').querySelector('datalist').appendChild(datalistOpt);
            })
        }
    });

    if (isLESelected) {
        crudUserModal.querySelector('#legal_entity').value = LESelected.name;
        crudUserModal.querySelector('#legal_entity').disabled = true;
        defaultEmailDomain = `@${LESelected.email_domain}`;
    }

    if (isUserSelected) {
        crudUserModal.querySelector('#email').value = userSelected.email;
        crudUserModal.querySelector('#email').disabled = true;
        crudUserModal.querySelector('#last_name').value = userSelected.last_name;
        crudUserModal.querySelector('#last_name').disabled = true;
        crudUserModal.querySelector('#first_name').value = userSelected.first_name;
        crudUserModal.querySelector('#first_name').disabled = true;
        crudUserModal.querySelector('#legal_entity').value = userSelected.legal_entity;
        crudUserModal.querySelector('#legal_entity').disabled = true;
        crudUserModal.querySelector('#title').value = userSelected.title;
        crudUserModal.querySelector('#dept').value = userSelected.dept;
        crudUserModal.querySelector('#cellphone').value = userSelected.cellphone;
        crudUserModal.querySelector('#work_phone').value = userSelected.work_phone;
        crudUserModal.querySelector('#postal_addr').value = userSelected.postal_addr;
    }

    crudUserModalInputElAll.forEach(modalInputEl => {
        if (modalInputEl.disabled && modalInputTag == 'new') {
            inputChkResults.set(modalInputEl.id, modalInputTag);
        } else if (modalInputEl.disabled && modalInputTag == 'updating') {
            inputChkResults.set(modalInputEl.id, 'noChg');
        } else {
            inputChkResults.set(modalInputEl.id, false);
        }
    })

    crudUserModal.querySelector('#email').focus();

    crudUserModalBtnSubmit.textContent = 'submit';
    crudUserModalBtnSubmit.classList.add('disabled');
    crudUserModalBtnOk.style.display = 'none';
}

crudUserModal.addEventListener('shown.bs.modal', e => {crudUserModalInitial();})

crudUserModalInputElAll.forEach(m => m.addEventListener('blur', e => inputChk(e.target, crudUserModalBtnSubmit)));
crudUserModalBtnSubmit.addEventListener('focus', e => {crudUserModalInputElAll.forEach(m => inputChk(m, crudUserModalBtnSubmit));});

crudUserModalBtnSubmit.addEventListener('click', e => {
    if (e.target.textContent == 'submit') {
        if (Array.from(inputChkResults.values()).every((element, index, array) => {return element != false;}) && !Array.from(inputChkResults.values()).every((element, index, array) => {return element == 'noChg';})) {
            crudUserModal.querySelector("h1.modal-title").textContent = 'review & confirm';
            crudUserModalInputElAll.forEach(inputEl => {
                ['text-danger', 'border-bottom', 'border-danger', 'border-success'].forEach(m => inputEl.classList.remove(m));
                inputEl.disabled = true;
                inputEl.nextElementSibling.textContent = '';
                inputChkResults.get(`${inputEl.id}`) == modalInputTag ? inputEl.classList.add('border-success') : null;
            });
            e.target.textContent = 'back';
            crudUserModalBtnOk.style.display = '';
        }
    } else if (e.target.textContent == 'back') {
        crudUserModal.querySelector("h1.modal-title").textContent = modalInputTag;
        crudUserModalInputElAll.forEach(inputEl => {
            if (isLESelected && ['legal_entity', ].some((element, index, array) => {return element == inputEl.id})) {
                
            } else if (isUserSelected && ['email', 'last_name', 'first_name', 'legal_entity', ].some((element, index, array) => {return element == inputEl.id})) {

            } else {
                inputEl.disabled = false
            }
        });
        // if (isUserSelected) {['email', 'last_name', 'first_name', 'legal_entity', ].forEach(m => crudUserModal.querySelector(`#${m}`).disabled = true);}
        // if (isLESelected) {['legal_entity', ].forEach(m => crudUserModal.querySelector(`#${m}`).disabled = true);}
        e.target.textContent = 'submit';
        crudUserModalBtnOk.style.display = 'none';
    }
});
/*
crudUserModalBtnSubmit.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.keyCode === 13) {
        e.preventDefault;
        crudUserModalSubmit(e);
    }
});
*/


function inputChk(inputEl, btn) {
    if (!inputEl.disabled) {
        let inputChkResult = true, inputChkAlert;

        inputEl.value = inputEl.value.trim();

        if (inputEl.closest('.row').querySelector('label').textContent == 'email') {
            inputEl.value = inputEl.value.trim().replaceAll(/[`~!#$%^&*()+=\[\]\\{}|;':",/<>? ·~！#￥%……&*（）——+=【】、{}|；‘：“，。、《》？]/g,'');

            inputEl.value != '' && !inputEl.value.includes('@') ? inputEl.value += defaultEmailDomain : null;
            
            // const legalEntityRowStyle = inputEl.closest('.modal-body').querySelector('#legal_entity').closest('.row').style;
            if (!inputEl.value.includes(defaultEmailDomain)) {
                // legalEntityRowStyle.display = '';
                inputEl.closest('.modal-body').querySelector('#legal_entity').disabled = false;
            } else {
                // legalEntityRowStyle.display = 'none';
                inputEl.closest('.modal-body').querySelector('#legal_entity').disabled = true;
                // inputEl.closest('.modal-body').querySelector('#legal_entity').value = '';
            }
        } else {
            inputEl.value = inputEl.value.trim().replaceAll(/[`~!@#$%^&*()+=\[\]\\{}|;:",./<>?·~！@#￥%……&*（）——+=【】、{}|；‘：“，。、《》？]/g,'');
        }

        if (inputChkResult && inputEl.required && inputEl.value == '') {
            // inputChkAlert = `${inputEl.closest('.row').querySelector('label').textContent} is Required`;
            inputChkAlert = `${inputEl.id.replaceAll(/[_]/g, ' ')} is Required`;
            inputChkResult = false;
        }

        switch (inputEl.id) {
            case 'email':
                if (inputChkResult && inputEl.value != '' && (inputEl.value in emailOptLst) && modalInputTag == 'new') {
                    inputChkAlert = `the given Email [ ${inputEl.value} ] already Exists in the system`;
                    inputChkResult = false;
                }
                break;
            case 'last_name':
                break;
            case 'first_name':
                break;
            case 'legal_entity':
                if (inputChkResult && inputEl.value != '' && !(inputEl.value in LEOptLst)) {
                    inputChkAlert = `the given Legal Entity [ ${inputEl.value} ] does NOT exist in the Option List`;
                    inputChkResult = false;
                }
                break;
            case 'title':
                if (inputChkResult && inputEl.value.length > 64) {
                    inputChkAlert = `the given Title [ ${inputEl.value} ] is > 64 characters`;
                    inputChkResult = false;
                }
                break;
            case 'dept':
                break;
            case 'cellphone':
                if (inputChkResult && inputEl.value.length > 11) {
                    inputChkAlert = `the given Mobile Phone # [ ${inputEl.value} ] is > 11 characters`;
                    inputChkResult = false;
                }
                break;
            case 'work_phone':
                if (inputChkResult && inputEl.value.length > 8) {
                    inputChkAlert = `the given Work Phone # [ ${inputEl.value} ] is > 8 characters`;
                    inputChkResult = false;
                }
                break;
            case 'postal_addr':
                if (inputChkResult && inputEl.value.length > 128) {
                    inputChkAlert = `the given Postal Address [ ${inputEl.value} ] is > 128 characters`;
                    inputChkResult = false;
                }
                break;
        }

        if (inputChkResult) {
            switch (modalInputTag) {
                case 'new':
                    inputChkAlert = inputEl.value != '' ? modalInputTag : 'noChg';
                    inputChkResult = inputEl.value != '' ? modalInputTag : 'noChg';
                    break;
                case 'updating':
                    const userSelectedMap = new Map(Object.entries(userSelected));
                    inputChkAlert = inputEl.value != userSelectedMap.get(`${inputEl.id}`) ? modalInputTag : 'noChg';
                    inputChkResult = inputEl.value != userSelectedMap.get(`${inputEl.id}`) ? modalInputTag : 'noChg'
                    break;
                case 'deleting':
                  console.log('Mangoes and papayas are $2.79 a pound.');
                  // Expected output: "Mangoes and papayas are $2.79 a pound."
                  break;
                default:
                  console.log(`Sorry, we are out of ${modalInputTag}.`);
              }
        }

        ['text-danger', 'border-bottom', 'border-danger'].forEach(m => inputEl.classList.toggle(m, !inputChkResult));
        ['border-success'].forEach(m => inputEl.classList.toggle(m, inputChkResult));
        inputEl.nextElementSibling.textContent = inputChkAlert;

        inputChkResults.set(inputEl.id, inputChkResult);
        btn.classList.toggle(
            'disabled', !Array.from(inputChkResults.values()).every((element, index, array) => {return element != false;}) || Array.from(inputChkResults.values()).every((element, index, array) => {return element == 'noChg';})
        );

        return inputChkResult;
    }
}

crudUserModalBtnOk.addEventListener('click', e => {
    const postUpdUri = window.location.origin + '/user/crud/';
    const csrftoken = crudUserModal.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken

    const formData = new FormData();
    if (modalInputTag != 'new') {formData.append('email', userSelected.email);}
    // if (modalInputTag == 'newLegalEntity') {legalEntityModalInputtype.checked ? formData.append('type', 'I') : formData.append('type', 'E');}
    inputChkResults.forEach((value, key, map) => {if (value == modalInputTag) {formData.append(`${key}`, crudUserModal.querySelector(`#${key}`).value);}});

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
        baseMessagesAlert(json.chg_log, 'info');

    /*
        if (modalInputTag == 'updLegalEntity') {
            inputChkResults.forEach((value, key, map) => {
                if (value == 'updating') {
                    if (key == 'type') {
                        legalEntityModalInputtype.checked ? userProfileTblTrDblClckd.querySelector(`#userProfileTblTd${key}`).textContent = 'Internal' : userProfileTblTrDblClckd.querySelector(`#userProfileTblTd${key}`).textContent = 'External';
                    } else if (key != 'contact' && key != 'postal_addr') {
                        userProfileTblTrDblClckd.querySelector(`#userProfileTblTd${key}`).textContent = legalEntityModal.querySelector(`#legalEntityModalInput${key}`).value;
                    }
                }
            });
        } else if (modalInputTag == 'newLegalEntity') {
            const userProfileTblTr = document.createElement('tr');
            inputChkResults.forEach((value, key, map) => {
                if (value == 'new') {
                    document.createElement('td').in

                }

            });
            userProfileTbl.appendChild(document.createElement('tr'));
        }
    */

    }).catch(error => {console.error('Error:', error);});
})