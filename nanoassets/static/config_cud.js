import { getJsonResponseApiData } from './getJsonResponseApiData.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';
import { inputChk } from './inputChk.js';

'use strict'

const configCUDModal = document.querySelector('#configCUDModal');

let pK, crud, modalLabelContent, configClass_lst, details, digital_copies, inputChkResults;

configCUDModal.addEventListener('show.bs.modal', (e) => {
    let getUri;
    pK = e.relatedTarget.id;
    switch (e.relatedTarget.name) {
        case 'createConfig':
            crud = 'cc'
            modalLabelContent = 'create Config';
            getUri = window.location.origin + `/json_response/config_getLst/`;
            break;
        default:
            getUri = window.location.origin + `/json_response/config_getLst/?pK=${pK}`;
            crud = e.relatedTarget.name == 'updateConfig' ? 'uc' : 'dc';
            modalLabelContent = e.relatedTarget.name == 'updateConfig' ? 'update Config' : 'delete Config';
            break;
    }
    
    async function getDetailsAsync() {
        try {
            const json = await getJsonResponseApiData(getUri);
            if (json) {
                configClass_lst = json[0];
                details = json[1];
                digital_copies = json[2];
            } else {
                baseMessagesAlert("the data for Config is NOT ready", 'danger');
            }
        } catch (error) {
            console.error('There was a problem with the async operation:', error);
        }
    }
    getDetailsAsync();
});

const modalLabel = configCUDModal.querySelector('#modalLabel');
const configClass = configCUDModal.querySelector('#configClass');
const order = configCUDModal.querySelector('#order');
const configPara = configCUDModal.querySelector('#configPara');
const comments = configCUDModal.querySelector('#comments');
const scanned_copy = configCUDModal.querySelector('#scanned_copy');

function modalIni(e, full = true) {
    if (full) {
        configClass.value = details[configClass.id] ? details[configClass.id] : '';
    
        const configClassDatalist = configCUDModal.querySelector('#configClassDatalist');
        configClassDatalist.innerHTML = ''
        Object.keys(configClass_lst).forEach(key => {
            const dataListOpt = document.createElement('option');
            dataListOpt.textContent = key;
            configClassDatalist.appendChild(dataListOpt);
        });

        order.value = details[order.id] ? details[order.id] : '';
        configPara.value = details[configPara.id] ? details[configPara.id] : '';
        comments.value = details[comments.id] ? details[comments.id] : '';
        scanned_copy.value = '';
    }

    modalLabel.textContent = modalLabelContent;
    configClass.focus();
    modalBtnNext.textContent = 'next';
    modalBtnSubmit.classList.add('hidden');  // modalBtnSubmit.style.display = 'none';

    modalInputElAll.forEach(modalInputEl => {
        modalInputEl.disabled = crud == 'dc' ? true : false;
        ['text-danger', 'border-bottom', 'border-danger', 'border-success'].forEach(m => modalInputEl.classList.remove(m));
        modalInputEl.nextElementSibling.textContent = '';
        // inputChkResults.get(`${modalInputEl.id}`) == modalInputTag ? modalInputEl.classList.add('border-success') : null;
    });
    
    inputChkResults = {
        // 'configClass': configClass.value ? true : false,
        // 'configPara': configPara.value ? true : false,
        // 'scanned_copy': false,
    };

    const digitalCopiesUlEl = configCUDModal.querySelector('ul');
    digitalCopiesUlEl.textContent = "";
    if (crud != 'cc') {
        configClass.disabled = true;
        Object.entries(digital_copies).forEach((value, key, map) => {
            const digitalCopiesLiEl = document.createElement('li');
            
            digitalCopiesLiEl.classList.add('text-break');
            // digitalCopiesLiEl.textContent = value;
            digitalCopiesLiEl.innerHTML = crud == 'dc' ? value :
                    `<a href="">${value}</a>
                    <a href="{% url 'nanobase:digital-copy-delete' digital_copy.pk %}" class="text-decoration-none">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x" viewBox="0 0 16 16">
                        <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                        </svg>
                    </a>
                    `
            digitalCopiesUlEl.appendChild(digitalCopiesLiEl);
        })
    }
}

configCUDModal.addEventListener('shown.bs.modal', e => {modalIni(e)});

const inputElAll = Array.from(configCUDModal.querySelector('.modal-body').querySelectorAll('input'));
const modalInputElAll = inputElAll.concat(Array.from(configCUDModal.querySelector('.modal-body').querySelectorAll('textarea')))
const modalBtnNext = configCUDModal.querySelector('#modalBtnNext');
const modalBtnSubmit = configCUDModal.querySelector('#modalBtnSubmit');

let if_some_required_input_is_false, if_all_required_input_is_noChg;

modalInputElAll.forEach(inputEl => inputEl.addEventListener('blur', e => { // Input validation on leaving each of Input elements 在离开每个输入元素时进行输入验证
    const optLst = e.target.list && e.target.id == 'configClass' ? configClass_lst : null;
    inputChkResults[e.target.id] = inputChk(e.target, optLst, details[e.target.id] ? details[e.target.id] : '');
    if_some_required_input_is_false = Object.values(inputChkResults).some((element, index, array) => {return element == false;});
    if_all_required_input_is_noChg = Object.values(inputChkResults).every((element, index, array) => {return element == 'noChg';});
    // const if_all_required_input_is_noChg =  (inputChkResults.configClass == 'noChg' && inputChkResults.configPara == 'noChg') ? true : false;
    modalBtnNext.classList.toggle('disabled', if_some_required_input_is_false || if_all_required_input_is_noChg);
}));

/*
modalBtnNext.addEventListener('focus', e => {modalInputElAll.forEach(inputEl => { // Input validation when Next button gets focus 在Next按钮获得焦点时进行输入验证
    const optLst = inputEl.list && inputEl.id == 'configClass' ? configClass_lst : null;
    inputChkResults[inputEl.id] = inputChk(inputEl, optLst, details[inputEl.id] ? details[inputEl.id] : '');
    if_some_required_input_is_false = Object.values(inputChkResults).some((element, index, array) => {return element == false;});
    if_all_required_input_is_noChg = Object.values(inputChkResults).every((element, index, array) => {return element == 'noChg';});
    // const if_all_required_input_is_noChg =  (inputChkResults.configClass == 'noChg' && inputChkResults.configPara == 'noChg') ? true : false;
    modalBtnNext.classList.toggle('disabled', crud != 'dc' && (if_some_required_input_is_false || if_all_required_input_is_noChg));
});});
*/
modalBtnNext.addEventListener('click', e => {
    modalInputElAll.forEach(inputEl => { // Input validation when Next button gets focus 在Next按钮获得焦点时进行输入验证
        const optLst = inputEl.list && inputEl.id == 'configClass' ? configClass_lst : null;
        inputChkResults[inputEl.id] = inputChk(inputEl, optLst, details[inputEl.id] ? details[inputEl.id] : '');
        if_some_required_input_is_false = Object.values(inputChkResults).some((element, index, array) => {return element == false;});
        if_all_required_input_is_noChg = Object.values(inputChkResults).every((element, index, array) => {return element == 'noChg';});
        // const if_all_required_input_is_noChg =  (inputChkResults.configClass == 'noChg' && inputChkResults.configPara == 'noChg') ? true : false;
        modalBtnNext.classList.toggle('disabled', crud != 'dc' && (if_some_required_input_is_false || if_all_required_input_is_noChg));
    });

    if (e.target.textContent == 'next'){
        if (!(crud != 'dc' && (if_some_required_input_is_false || if_all_required_input_is_noChg))) {
            modalLabel.textContent = 'review & confirm';
            modalInputElAll.forEach(modalInputEl => {
                ['text-danger', 'border-bottom', 'border-danger', 'border-success'].forEach(m => modalInputEl.classList.remove(m));
                modalInputEl.disabled = true;
                modalInputEl.nextElementSibling.textContent = '';
                // inputChkResults.get(`${modalInputEl.id}`) == modalInputTag ? modalInputEl.classList.add('border-success') : null;
            });
            e.target.textContent = 'back';
            modalBtnSubmit.classList.remove('hidden');  // modalBtnSubmit.style.display = '';
        }
    } else if (e.target.textContent == 'back') {modalIni(e, false);}
})

modalBtnSubmit.addEventListener('click', e => {
    const postUpdUri = window.location.origin + '/config/cud/';
    const csrftoken = configCUDModal.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken

    const formData = new FormData();
    formData.append('crud', crud);
    formData.append('pk', pK);
    // formData.append('comments', comments.value);
    
    modalInputElAll.forEach(inputEl => {
        if (inputEl.type == 'file') {
            for (let i = 0; i < inputEl.files.length; i++) {
                formData.append('scanned_copy', inputEl.files[i]);
            }
        } else {
            formData.append(inputEl.id, inputEl.value);
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

