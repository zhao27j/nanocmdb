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
    if (e.target.textContent == 'Supported+') {
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
                    dropdownItemHref.addEventListener('click', e => {
                        accordionFlush.innerHTML = '';
                        groupByValue.forEach((lstValue, lstKey, lstMap) => {reLst(e.target.id, lstKey, accordionFlush)});
                        baseMessagesAlert(`grouped by ${e.target.textContent}`, 'success');
                    });
                    dropdownBtnUl.appendChild(dropdownItemLi);
                })
            } 
            /* else if (textContentItm == 'filter by') {
                status_lst.forEach((value, key, map) => {
                    const chkBox = document.createElement('input');
                    new Map([
                        ['type', 'checkbox'],
                        ['class', 'btn-check'],
                        ['id', "btn-check"],
                        ['autocomplete', 'off'],
                    ]).forEach((attrValue, attrKey, attrMap) => {
                        chkBox.setAttribute(attrKey, attrValue);
                        // dropdownItemHref.textContent = groupByKey.replaceAll('_', ' ');
                    });
                    dropdownBtnUl.appendChild(chkBox);
                    const chkBoxLbl = document.createElement('label');
                    new Map([
                        ['class', 'btn btn-primary'],
                        ['for', "btn-check"],
                    ]).forEach((attrValue, attrKey, attrMap) => {
                        chkBoxLbl.setAttribute(attrKey, attrValue);
                    });
                    chkBoxLbl.textContent = key;
                    dropdownBtnUl.appendChild(chkBoxLbl);
                })
            }
            */

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
            sub_categories_lst.forEach((value, key, map) => {reLst('sub_category', key, accordionFlush)});
            baseMessagesAlert('grouped by Sub category', 'success');
        }
    }
})

function reLst(grpBy, accordionBtnTxt, accordion) {

    const table = document.createElement('table');
    ['table', 'table-striped', 'table-hover', 'fw-light'].forEach(classItem => table.classList.add(classItem));

    table.appendChild(document.createElement('thead'));
    table.querySelector('thead').appendChild(document.createElement('tr'));
    ['', 'Serial #', '', 'Model / Type', 'Hostname', 'Status', 'Owner', 'Site', 'Contract', ].forEach(th_txt => {
        const th = document.createElement('th');
        th.innerHTML = `<small>${th_txt}</small>`;
        table.querySelector('thead tr').appendChild(th);
    })

    table.appendChild(document.createElement('tbody'));
    let num = 0, numOfAvailable = 0, numOfRepair = 0;
    instance_lst.forEach((lstValue, lstKey, map) => {
        if (lstValue[grpBy] == accordionBtnTxt) { // the keyword grouping by
            const tr = document.createElement('tr');
            ['instance', 'serial_number', 'inRepair', 'model_type', 'hostname', 'status', 'owner', 'branchSite', 'contract', ].forEach(td_txt => {
                const td = document.createElement('td');
                switch (td_txt) {
                    case 'instance':
                        const checkbox = document.createElement('input');
                        new Map([
                            ['type', 'checkbox'],
                            ['name', `${td_txt}`],
                            ['id', `Instance${lstKey}`],
                            ['value', `${lstKey}`],
                        ]).forEach((attrValue, attrKey, attrMap) => {
                            checkbox.setAttribute(attrKey, attrValue);
                        })
                        td.appendChild(checkbox);
                        break;
                    case 'serial_number':
                        const serial_numberLbl = document.createElement('label');
                        serial_numberLbl.setAttribute('for', `Instance${lstKey}`);
                        const serial_numberHref = document.createElement('a');
                        new Map([
                            ['href', `${window.location.origin}/instance/${lstKey}/detail/`],
                            ['class', 'text-decoration-none'],
                        ]).forEach((attrValue, attrKey, attrMap) => {
                            serial_numberHref.setAttribute(attrKey, attrValue);
                        })
                        serial_numberHref.innerHTML = `<small>${lstValue[td_txt]}</small>`
                        serial_numberLbl.appendChild(serial_numberHref);
                        td.appendChild(serial_numberLbl);
                        break;
                    case 'inRepair':
                        td.id = `${td_txt}Instance${lstKey}`;
                        if (lstValue['status'] == 'in Repair') {
                            td.innerHTML = [
                                `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send-exclamation" viewBox="0 0 16 16">`,
                                    `<path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855a.75.75 0 0 0-.124 1.329l4.995 3.178 1.531 2.406a.5.5 0 0 0 .844-.536L6.637 10.07l7.494-7.494-1.895 4.738a.5.5 0 1 0 .928.372l2.8-7Zm-2.54 1.183L5.93 9.363 1.591 6.602l11.833-4.733Z"></path>`,
                                    `<path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Zm.5-5v1.5a.5.5 0 0 1-1 0V11a.5.5 0 0 1 1 0Zm0 3a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0Z"></path>`,
                                `</svg>`,
                            ].join('');
                        } else if (lstValue['status'] == 'Available' || lstValue['status'] == 'in Use') {
                            td.innerHTML = [
                                `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-wrench-adjustable" viewBox="0 0 16 16">`,
                                    `<path d="M16 4.5a4.492 4.492 0 0 1-1.703 3.526L13 5l2.959-1.11c.027.2.041.403.041.61Z"/>`,
                                    `<path d="M11.5 9c.653 0 1.273-.139 1.833-.39L12 5.5 11 3l3.826-1.53A4.5 4.5 0 0 0 7.29 6.092l-6.116 5.096a2.583 2.583 0 1 0 3.638 3.638L9.908 8.71A4.49 4.49 0 0 0 11.5 9Zm-1.292-4.361-.596.893.809-.27a.25.25 0 0 1 .287.377l-.596.893.809-.27.158.475-1.5.5a.25.25 0 0 1-.287-.376l.596-.893-.809.27a.25.25 0 0 1-.287-.377l.596-.893-.809.27-.158-.475 1.5-.5a.25.25 0 0 1 .287.376ZM3 14a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"/>`,
                                `</svg>`,
                            ].join('');
                        }
                        break;
                    case 'status':
                        td.id = `${td_txt}Instance${lstKey}`;
                        td.innerHTML = `<small>${lstValue[td_txt]}</small>`;
                        if (lstValue['disposal_request']) {
                            td.innerHTML += [
                                `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-recycle" viewBox="0 0 16 16">`,
                                   `<path d="M9.302 1.256a1.5 1.5 0 0 0-2.604 0l-1.704 2.98a.5.5 0 0 0 .869.497l1.703-2.981a.5.5 0 0 1 .868 0l2.54 4.444-1.256-.337a.5.5 0 1 0-.26.966l2.415.647a.5.5 0 0 0 .613-.353l.647-2.415a.5.5 0 1 0-.966-.259l-.333 1.242-2.532-4.431zM2.973 7.773l-1.255.337a.5.5 0 1 1-.26-.966l2.416-.647a.5.5 0 0 1 .612.353l.647 2.415a.5.5 0 0 1-.966.259l-.333-1.242-2.545 4.454a.5.5 0 0 0 .434.748H5a.5.5 0 0 1 0 1H1.723A1.5 1.5 0 0 1 .421 12.24l2.552-4.467zm10.89 1.463a.5.5 0 1 0-.868.496l1.716 3.004a.5.5 0 0 1-.434.748h-5.57l.647-.646a.5.5 0 1 0-.708-.707l-1.5 1.5a.498.498 0 0 0 0 .707l1.5 1.5a.5.5 0 1 0 .708-.707l-.647-.647h5.57a1.5 1.5 0 0 0 1.302-2.244l-1.716-3.004z"/>`,
                                `</svg>`,
                            ].join('');
                        }
                        lstValue[td_txt] == 'Available' ? numOfAvailable++ : lstValue[td_txt] == 'in Repair' ? numOfRepair++ : null;
                        break;
                    case 'contract':
                        td.id = `${td_txt}Instance${lstKey}`;
                        if (lstValue[td_txt] == '') {

                        } else if (typeof lstValue[td_txt] === 'object') {
                            for (var k in lstValue[td_txt]) {
                            // Object.keys(lstValue[td_txt]).forEach(k => {
                                const contractHREF = document.createElement('a');
                                new Map([
                                    ['href', `${window.location.origin}/${td_txt}/${k}/detail/`],
                                    ['class', 'text-decoration-none'],
                                ]).forEach((attrValue, attrKey, attrMap) => {
                                    contractHREF.setAttribute(attrKey, attrValue);
                                })
                                contractHREF.innerHTML = `<small>${lstValue[td_txt][k]}</small>`
                                td.appendChild(contractHREF);
                            }
                        }
                        break;
                    default:
                        td.id = `${td_txt}Instance${lstKey}`;
                        td.innerHTML = `<small>${lstValue[td_txt]}</small>`;
                        break;
                }
                tr.appendChild(td);
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