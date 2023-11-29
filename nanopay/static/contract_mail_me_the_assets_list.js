import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'

const btn = document.querySelector('div.d-grid.gap-2.d-md-flex.justify-content-md-end button.btn.btn-outline-secondary.me-md-2');

btn.addEventListener('click', e => {
    e.target.classList.add('disabled'); // 禁用 按钮
    
    let getLstUri = window.location.origin + '/contract/mail_me_the_list/';
    getLstUri += `?contractPk=${e.target.id}`;

    if (document.querySelectorAll('input[name="instance"][type="checkbox"]:checked').length > 0) {
        const instance_selected = document.querySelectorAll('input[name="instance"][type="checkbox"]:checked');
        let instance_selected_pk = '';
        instance_selected.forEach(el => {
            instance_selected_pk += el.value + ',';
        });
        getLstUri += `&instancesPk=${instance_selected_pk}`;
    }

    fetch(getLstUri
        ).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(`HTTP error: ${response.status}`);
            }
        }).then(json => {
            if (json.is_sent) {
                baseMessagesAlert(`email sent`, 'success');
            } else {
                baseMessagesAlert(`email ! sent`, 'danger');
            }
            
            setTimeout(() => { e.target.classList.remove('disabled');}, 10000); // 3秒后 取消 按钮 禁用
        }).catch(error => {
            error ? console.error('Error:', error) : null;
        });
})