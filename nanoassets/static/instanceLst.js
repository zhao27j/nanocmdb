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
    branchSite_lst = new Map(Object.entries(json[5]));
    contract_lst = new Map(Object.entries(json[6]));
    console.log('getLst has been fetched');
}).catch(error => {console.error('Error:', error ? error : null);})

let accordionFlush;
document.addEventListener('click', e => {
    if (e.target.parentNode.className == 'dropdown-item' && e.target.textContent == 'Supported+') {
        const pgCntnt = document.querySelector('div#page_content');
        pgCntnt.innerHTML = '';

        ['group by', 'filter by'].forEach(textContentItm => {
            const dropdownBtnGrp = document.createElement('div');
            ['btn-group', 'dropend', 'm-3', ].forEach(classItm => dropdownBtnGrp.classList.add(classItm));

            const dropdownBtn = document.createElement('button');
            new Map([
                ['class', 'btn btn-secondary dropdown-toggle'],
                ['type', 'button'],
                ['data-bs-toggle', 'dropdown'],
                ['aria-expanded', 'false'],
            ]).forEach((attrValue, attrKey, attrMap) => {
                dropdownBtn.setAttribute(attrKey, attrValue);
                dropdownBtn.textContent = textContentItm;
            });
            dropdownBtnGrp.appendChild(dropdownBtn);

            const dropdownBtnUl = document.createElement('ul');
            dropdownBtnUl.classList.add('dropdown-menu');
            dropdownBtnGrp.appendChild(dropdownBtnUl);

            if (textContentItm == 'group by') {
                new Map([
                    ['status', status_lst],
                    ['sub_category', sub_categories_lst],
                    ['model_type', model_type_lst],
                    ['branchSite', branchSite_lst],
                ]).forEach((groupByValue, groupByKey, groupBymap) => {
                    // dropdownBtnUl.innerHTML += [`<li><a class="dropdown-item" href="#" id="${key}">${key.replaceAll('_', ' ')}</a></li>`,].join('');
                    const dropdownItemLi = document.createElement('li');
                    const dropdownItemHref = document.createElement('a');
                    new Map([
                        ['class', "dropdown-item"],
                        ['href', "#"],
                        ['id', groupByKey],
                    ]).forEach((attrValue, attrKey, attrMap) => {
                        dropdownItemHref.setAttribute(attrKey, attrValue);
                        dropdownItemHref.textContent = groupByKey.replaceAll('_', ' ');
                    });
                    dropdownItemLi.appendChild(dropdownItemHref);
                    // dropdownBtnUl.querySelector(`#${key}`).addEventListener('click', e => {
                    dropdownItemHref.addEventListener('click', e => {
                        accordionFlush.innerHTML = '';
                        groupByValue.forEach((lstValue, lstKey, lstMap) => {reGrp(e.target.id, lstKey, accordionFlush)});
                        baseMessagesAlert(`grouped by ${e.target.textContent}`, 'success');
                    });
                    dropdownBtnUl.appendChild(dropdownItemLi);
                })
            }

            const dropdownInstance = bootstrap.Dropdown.getOrCreateInstance(dropdownBtn);
            dropdownBtn.addEventListener('mouseover', e => {
                dropdownInstance.show()
            })

            dropdownBtnUl.addEventListener('mouseleave', e => {
                setTimeout(() => { dropdownInstance.hide();}, 300);
            })

            dropdownBtnGrp.addEventListener('mouseleave', e => {
                setTimeout(() => { dropdownInstance.hide();}, 300);
            })

            pgCntnt.appendChild(dropdownBtnGrp);

        })

        accordionFlush = document.createElement('div');
        ['accordion', 'accordion-flush'].forEach(classItm => accordionFlush.classList.add(classItm));
        accordionFlush.id = "accordionFlush";
        pgCntnt.appendChild(accordionFlush);

        if (sub_categories_lst) {
            sub_categories_lst.forEach((value, key, map) => {reGrp('sub_category', key, accordionFlush)});
            baseMessagesAlert('grouped by Sub category', 'success');
        }
    }
})

function reGrp(grpBy, accordionBtnTxt, accordion) {

    const table = document.createElement('table');
    ['table', 'table-striped', 'table-hover', 'fw-light'].forEach(classItem => table.classList.add(classItem));

    table.appendChild(document.createElement('thead'));
    table.querySelector('thead').appendChild(document.createElement('tr'));
    ['', 'Serial #', '', 'Model / Type', 'Hostname', 'Status', 'Owner', 'Site', 'Contract', ].forEach(th_txt => {
        const th = document.createElement('th');
        th.innerHTML = `<small>${th_txt}<small/>`;
        table.querySelector('thead tr').appendChild(th);
    })

    table.appendChild(document.createElement('tbody'));
    let num = 0, numOfAvailable = 0, numOfRepair = 0;
    instance_lst.forEach((mapValue, mapKey, map) => {
        if (mapValue[grpBy] == accordionBtnTxt) { // the keyword grouping by
            const tr = document.createElement('tr');
            ['', 'serial_number', '', 'model_type', 'hostname', 'status', 'owner', 'branchSite', 'contract', ].forEach(td_txt => {
                const td = document.createElement('td');
                td.innerHTML = td_txt == '' ? '' : `<small>${mapValue[td_txt]}<small/>`;
                tr.appendChild(td);
                if (td_txt == 'status') {
                    mapValue[td_txt] == 'Available' ? numOfAvailable++ : mapValue[td_txt] == 'in Repair' ? numOfRepair++ : null;
                }
            })
            table.querySelector('tbody').appendChild(tr);
            num++;
        }
    })
    const accordionItem = document.createElement('div');
    accordionItem.classList.add('accordion-item');
    accordionItem.innerHTML = [
        `<h2 class="accordion-header">`,
            `<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#${accordionBtnTxt.replaceAll(' ', '_')}" aria-expanded="false" aria-controls="${accordionBtnTxt.replaceAll(' ', '_')}">`,
                `<small>`,
                    `<span class="badge rounded-pill text-bg-light ms-3">${accordionBtnTxt.replaceAll('_', ' ')}</span>`,
                    `<span class="badge rounded-pill text-bg-secondary ms-3">${num}</span>`,
                `</small>`,
            `</button>`,
        `</h2>`,
        `<div id="${accordionBtnTxt.replaceAll(' ', '_')}" class="accordion-collapse collapse" data-bs-parent="#${accordion.id}">`,
            `<div class="accordion-body"></div>`,
        `</div>`,
    ].join('');

    const btnInnerHTMLSmallEl = accordionItem.querySelector('small');
    if (numOfAvailable != 0) {btnInnerHTMLSmallEl.innerHTML += [`<span class="badge rounded-pill text-bg-warning ms-3">${numOfAvailable}</span>`,].join('');}
    if (numOfRepair != 0) {btnInnerHTMLSmallEl.innerHTML += [`<span class="badge rounded-pill text-bg-danger ms-3">${numOfRepair}</span>`,].join('');}

    accordionItem.querySelector('div.accordion-body').appendChild(table);
    accordion.appendChild(accordionItem);
}