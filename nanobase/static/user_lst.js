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
userLstSwitch.addEventListener('change', e => fltr(e.target.checked))

function fltr(isExt) {
    const userProfileThead = document.querySelector('table#userProfileTbl thead');
    userProfileThead.innerHTML = ''

    let thLst = ['', 'name', 'email', 'title', 'dept'];
    if (isExt) {
        ['legal entity', 'mobile'].forEach(m => thLst.push(m))
    }
    
    const thTrEl = document.createElement('tr');
    ['text-capitalize', 'fs-6'].forEach(m => thTrEl.classList.add(m));
    
    thLst.forEach(m => {
        const thEl = document.createElement('th');
        // thEl.textContent = m;
        thEl.innerHTML = `<small>${m}</small>`
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
                    const tbodyTrInputChk = document.createElement('input');
                    tbodyTrInputChk.setAttribute('type', 'checkbox');
                    tbodyTrInputChk.name = 'user';
                    tbodyTrInputChk.value = key;
                    tbodyTrTdEl.appendChild(tbodyTrInputChk);

                    // <td><input type="checkbox" name="user" id="user{{ forloop.counter }}" value="{{ user.pk }}"/></td>
                } else {
                    // tbodyTrTdEl.textContent = value[`${m}`];
                    tbodyTrTdEl.innerHTML = value[m] == null || value[m] == '' ? '🈳' : `<small>${value[m]}</small>`;
                }
                tbodyTrEl.appendChild(tbodyTrTdEl);
            })
            userProfileTbody.appendChild(tbodyTrEl);
        }
    });
}