import { getJsonResponseApiData } from './getJsonResponseApiData.js';
import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

document.addEventListener('click', e => {
    if (e.target.textContent == 'Approve') {

        e.target.closest('button').disabled = true;
        // e.target.disabled = true;
        
        const payment_request_pk = e.target.id;
        const csrftoken = e.target.querySelector('[name=csrfmiddlewaretoken]').value; // get csrftoken
        
        const alertBtns = baseMessagesAlert('proceed ?', 'warning', false);

        alertBtns.forEach(btn => btn.addEventListener('click', btnClickEvent => {
            if (btnClickEvent.target.textContent == 'yes') {
                const postUpdUri = window.location.origin + '/payment_request/approve/';
                const formData = new FormData();
                formData.append('payment_request', payment_request_pk);
                
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
                        if (json.alert_type == 'success') {
                            e.target.closest('td').innerHTML = json.approver;
                        } else {
                            e.target.closest('button').disabled = false;
                        }
                        // location.reload();
                    });
                }).catch(error => {error ? console.error('Error:', error) : null;});
            } else {
                e.target.closest('button').disabled = false;
            }
        }))
    }
})