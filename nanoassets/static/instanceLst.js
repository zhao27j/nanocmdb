import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

let instance_lst, owner_lst, status_lst, model_type_lst, sub_categories_lst, manufacturer_lst, branchSite_lst, contract_lst;

const getLstUri = window.location.origin + '/json_response/instance_lst/';

fetch(getLstUri
            ).then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error(`HTTP error: ${response.status}`);
                }
            }).then(json => {
                instance_lst = new Map(Object.entries(json[0]));
                status_lst = new Map(Object.entries(json[1]));
                model_type_lst = new Map(Object.entries(json[2]));
                sub_categories_lst = new Map(Object.entries(json[3]));
                manufacturer_lst = new Map(Object.entries(json[4]));
                branchSite_lst = new Map(Object.entries(json[4]));
            }).catch(error => {console.error('Error:', error);})

document.addEventListener('click', e => {
    if (e.target.textContent.includes('+')) {
        

        

    }
})