import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

'use strict'


function getNonPayrollExpenseLst(budgetYear) {
    const getUri = window.location.origin + `/json_respone/nonPayrollExpense_getLst/?budgetYear=${budgetYear}`;

    return fetch(getUri
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).catch(error => {error ? console.error('Error:', error) : null;})
}

let is_IT_staff;
async function getNonPayrollExpenseLstAsync(budgetYear) {
    try {
        
        const json = await getNonPayrollExpenseLst(budgetYear);
        if (json) {
            const nonPayrollExpense_lst = json[0];
            baseMessagesAlert("non Payroll Expense data is ready", 'success');

            const dropdownItemBtn = document.createElement('button');
            new Map([
                ['class', 'dropdown-item'],
                ['type', 'button'],
            ]).forEach((attrValue, attrKey, attrMap) => {
                dropdownItemBtn.setAttribute(attrKey, attrValue);
                dropdownItemBtn.innerHTML = `<small>Payment Calendar</small>`;
            });
            document.querySelector('#dropdownItemPlaceholderForNonPayrollExpenseList').appendChild(dropdownItemBtn);
            dropdownItemBtn.addEventListener('click', e => dropdownMenuCreation(e));

        } else {
            baseMessagesAlert("non Payroll Expense data is NOT ready", 'danger');
        }
    } catch (error) {
        console.error('There was a problem with the async operation:', error);
    }
}

if (document.querySelector('#dropdownItemPlaceholderForNonPayrollExpenseList')) {
    const date = new Date();
    const budgetYear = date.getFullYear();
    getNonPayrollExpenseLstAsync(budgetYear);
}