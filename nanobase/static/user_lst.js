import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

// let legalEntities, legalEntityTypes, legalEntityPrjcts, legalEntitiesCntcts;

let users;

const getLstUri = window.location.origin + '/json_response/users_getLst/';

fetch(getLstUri
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).then(json => {
        // users = new Map(Object.entries(json[0]));
        users = new Map(Object.entries(json));
    }).catch(error => {console.error('Error:', error);})

const userLstSwitch = document.querySelector('#userLstSwitch');
userLstSwitch.addEventListener('change', e => {
    baseMessagesAlert(fltr(e.target.checked), 'success');
})

function fltr(isExt) {
    const userProfileThead = document.querySelector('table#userProfileTbl thead');
    userProfileThead.innerHTML = ''

    let msg = 'Internal users filtered out', thLst = ['', 'name', 'email', 'title', 'dept'];
    if (isExt) {
        ['legal_entity', 'cellphone'].forEach(m => thLst.push(m));
        msg = 'External users filtered out';
    }
    
    const thTrEl = document.createElement('tr');
    ['text-capitalize', 'fs-6'].forEach(m => thTrEl.classList.add(m));
    
    thLst.forEach(m => {
        const thEl = document.createElement('th');
        // thEl.textContent = m;
        thEl.innerHTML = `<small>${m.replaceAll('_', ' ')}</small>`
        thTrEl.appendChild(thEl);
    })
    userProfileThead.appendChild(thTrEl);
    
    const userProfileTbody = document.querySelector('table#userProfileTbl tbody');
    userProfileTbody.innerHTML = '';
    
    users.forEach((value, key, map) => {
        if (isExt == value['is_ext']) {
            const tbodyTrEl = document.createElement('tr');
            thLst.forEach(m => {
                const tbodyTrTdEl = document.createElement('td');
                if (m == '') {
                    tbodyTrTdEl.innerHTML = [
                        `<samll>`,
                            `<div class="form-check form-switch">`,
                                `<input class="form-check-input" type="checkbox" role="switch" name="userprofile" id="" value="${key}" />`,
                                `<label class="form-check-label" for=""></label>`,
                            `</div>`,
                        `</samll>`,
                    ].join('');
                    const tbodyTrInputChk = tbodyTrTdEl.querySelector('input[type=checkbox][role=switch]');
                    /*
                    new Map([
                        ['type', 'checkbox'],
                        ['class', 'form-check-input'],
                        ['role', 'switch'],
                    ]).forEach((value, key, map) => {
                        tbodyTrInputChk.setAttribute(key, value);
                    })
                    tbodyTrInputChk.name = 'user';
                    tbodyTrInputChk.value = key;
                    */
                    tbodyTrInputChk.checked = value['is_active'] ? true : false;
                    // tbodyTrTdEl.appendChild(tbodyTrInputChk);

                    // <td><input type="checkbox" name="user" id="user{{ forloop.counter }}" value="{{ user.pk }}"/></td>
                } else {
                    // tbodyTrTdEl.textContent = value[`${m}`];
                    // http://127.0.0.1:8000/instance_search_results/?q=li%2C+jeremy

                    tbodyTrTdEl.innerHTML = value[m] == null || value[m] == '' ? '🈳' : `<small>${value[m]}</small>`;
                    
                    if (!isExt && m == 'name') {
                        const badgeRoundedPillHrefEl = document.createElement('a')
                        new Map([
                            // ['href', `${window.location.origin}/instance_search_results/?q=${value[m].replaceAll(', ', '%2C+')}`],
                            ['href', `${window.location.origin}/instance_search_results/?q=${value[m]}`],
                            ['class', 'text-decoration-none'],
                        ]).forEach((attrValue, attrKey, attrMap) => {
                            badgeRoundedPillHrefEl.setAttribute(attrKey, attrValue);
                        });
                        [value['number_of_owned_assets_pc'], value['number_of_owned_assets_other']].forEach((number_of_owned_assets, index, array) => {
                            const badgeRoundedPillSpanEl = document.createElement('span');
                            new Map([
                                ['class', 'badge rounded-pill ms-1'],
                                ['data-bs-toggle', 'tooltip'],
                                ['data-bs-placement', 'top'],
                                ['data-bs-custom-class', 'custom-tooltip'],
                                ['data-bs-html', 'true'],
                                ['data-bs-title', `${index == 0 ? 'PC' : 'Others'}`],
                            ]).forEach((attrValue, attrKey, attrMap) => {
                                badgeRoundedPillSpanEl.setAttribute(attrKey, attrValue);   // tier1Btn.innerHTML = `<small>Supported +</small>`;
                            });
                            // ['badge', 'rounded-pill', 'ms-1', ].forEach(m => badgeRoundedPillSpanEl.classList.add(m));
                            badgeRoundedPillSpanEl.classList.add(number_of_owned_assets == 1 ? 'bg-secondary' : 'bg-danger');
                            badgeRoundedPillSpanEl.textContent = number_of_owned_assets;

                            badgeRoundedPillHrefEl.appendChild(badgeRoundedPillSpanEl);
                        })
                        tbodyTrTdEl.appendChild(badgeRoundedPillHrefEl);
                        /*
                        tbodyTrTdEl.innerHTML += [
                            `<span class="badge rounded-pill bg-secondary">`,
                                // `${value['number_of_owned_assets']}`,
                                `<span class="visually-hidden">the # of Assets Instance owned</span>`,
                            `</span>`,
                        ];
                        
                        const deactivateBtn = document.createElement('button');
                        ['btn', 'btn-link', 'text-decoration-none'].forEach(m => deactivateBtn.classList.add(m));
                        new Map([
                            ['data-bs-toggle', 'modal'],
                            ['data-bs-target', '#crudUserModal'],
                            ['name', ''],
                        ]).forEach((value, key, map) => {
                            deactivateBtn.setAttribute(key, value);
                        })
                        if (value['is_active']) {
                            deactivateBtn.innerHTML = [
                                `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-lock" viewBox="0 0 16 16">`,
                                    `<path d="M11 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm0 5.996V14H3s-1 0-1-1 1-4 6-4c.564 0 1.077.038 1.544.107a4.524 4.524 0 0 0-.803.918A10.46 10.46 0 0 0 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h5ZM9 13a1 1 0 0 1 1-1v-1a2 2 0 1 1 4 0v1a1 1 0 0 1 1 1v2a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1v-2Zm3-3a1 1 0 0 0-1 1v1h2v-1a1 1 0 0 0-1-1Z"/>`,
                                `</svg>`,
                            ].join('')
                        } else {
                            deactivateBtn.innerHTML = [
                                `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-unlock" viewBox="0 0 16 16">`,
                                    `<path d="M11 1a2 2 0 0 0-2 2v4a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h5V3a3 3 0 0 1 6 0v4a.5.5 0 0 1-1 0V3a2 2 0 0 0-2-2zM3 8a1 1 0 0 0-1 1v5a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1H3z"/>`,
                                `</svg>`,
                            ].join('')
                        }
                        tbodyTrTdEl.appendChild(deactivateBtn);
                        */
                    }
                }
                tbodyTrEl.appendChild(tbodyTrTdEl);
            })
            userProfileTbody.appendChild(tbodyTrEl);
        }
    });
    
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    return msg;
}