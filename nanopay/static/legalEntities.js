'use strict'

let legalEntities, legalEntityTypes, legalEntityPrjcts;

const getLstUri = window.location.origin + '/json_response/legalEntities_getLst/';

fetch(getLstUri
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).then(json => {
        legalEntities = json[0];
        legalEntityTypes = new Map(Object.entries(json[1]));
        legalEntityPrjcts = new Map(Object.entries(json[2]));
        legalEntityPrjcts.set("None", null);
        
        
    }).catch(error => {console.error('Error:', error);})

const legalEntitiesBtnByPrjct = document.querySelector("#legalEntitiesBtnByPrjct");
const legalEntitiesBtnByType = document.querySelector("#legalEntitiesBtnByType");

const legalEntitiesAccordion = document.querySelector("#legalEntitiesAccordion");

legalEntitiesBtnByPrjct.addEventListener('click', e => reLst(legalEntitiesAccordion, 'prjct', ['name', 'type', 'code']));

legalEntitiesBtnByType.addEventListener('click', e => reLst(legalEntitiesAccordion, 'type', ['name', 'prjct', 'code']));

function reLst(accordionEl, lstByTag, cols) {
    // if (lstByTag == 'Type') {tableTh = 'Project';} else if (lstByTag == 'Project') {tableTh = 'Type';}

    accordionEl.innerHTML = "";

    const lstBy = lstByTag == 'prjct' ? legalEntityPrjcts : lstByTag == 'type' ? legalEntityTypes : null;
    lstBy.forEach((valueBy, keyBy, mapBy) => {
        const accordionItem = document.createElement('div');
        accordionItem.classList.add("accordion-item");
        const accordionElItemHeaderBtnTxt = lstByTag == 'prjct' ? legalEntityPrjcts.get(`${keyBy}`) : lstByTag == 'type' ? legalEntityTypes.get(`${keyBy}`) : keyBy;
        accordionItem.innerHTML = [
            `<h2 class="accordion-header">`,
                `<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse${keyBy}" aria-expanded="true" aria-controls="panelsStayOpen-collapse${keyBy}">`,
                    `${accordionElItemHeaderBtnTxt}`,
                `</button>`,
            `</h2>`,
            `<div id="panelsStayOpen-collapse${keyBy}" class="accordion-collapse collapse show">`,
                `<div class="accordion-body" id="accordionElBody${keyBy}"></div>`,
            `</div>`,
        ].join('');
        
        accordionEl.appendChild(accordionItem);
        const accordionElItemHeaderBtn = accordionItem.querySelector('button');
        const accordionElBody = accordionItem.querySelector(`#accordionElBody${keyBy}`);

        const tableEl = document.createElement('table');
        tableEl.id = `${legalEntities}Tbl`;
        // ['table', 'table-striped', 'table-hover', 'fw-light'].forEach(element => tableEl.classList.add(element));
        tableEl.classList.add('table', 'table-striped', 'table-hover', 'fw-light');
        accordionElBody.appendChild(tableEl);

        const tableTheadEl = document.createElement('thead');
        let tableTrEl = document.createElement('tr');
        tableTrEl.innerHTML = '<th></th>';
        cols.forEach(col => {
            const tabelThEl = document.createElement('th');
            tabelThEl.innerHTML = `<small>${col}</small>`;
            tableTrEl.appendChild(tabelThEl);
        })
        tableTheadEl.appendChild(tableTrEl);
        tableEl.appendChild(tableTheadEl);

        const tableTbodyEl = document.createElement('tbody');
        tableEl.appendChild(tableTbodyEl);

        let counterBy = 0;
        legalEntities.forEach(row => {
            if (row.fields[`${lstByTag}`] == keyBy || legalEntityPrjcts.get(`${row.fields[lstByTag]}`) == lstBy.get(`${keyBy}`)) {
                tableTrEl = document.createElement('tr');
                tableTrEl.innerHTML = `<td><input type="checkbox" name="legal_entity_${row.pk}" id="${legalEntities}TblTd${row.pk}" value="${row.pk}" /></td>`;
                cols.forEach(col => {
                    const tabelTdEl = document.createElement('td');
                    const smallEl = document.createElement('small');
                    smallEl.id = `${legalEntities}TblTd${col}`;
                    if (col == 'prjct') {
                        legalEntityPrjcts.get(`${row.fields[col]}`) ? smallEl.textContent = legalEntityPrjcts.get(`${row.fields[col]}`) : smallEl.textContent = '🈳';
                    } else {
                        smallEl.textContent = col =='type' ? legalEntityTypes.get(`${row.fields[col]}`) : row.fields[`${col}`];
                    }
                    if (col == 'name') {
                        const hyperLink = document.createElement('a');
                        hyperLink.href = window.location.origin + `/legal_entity/${row.pk}/detail/`;
                        hyperLink.className = "text-decoration-none";

                        hyperLink.appendChild(smallEl);
                        tabelTdEl.appendChild(hyperLink)
                    } else {
                        tabelTdEl.appendChild(smallEl);
                    }
                    tableTrEl.appendChild(tabelTdEl);
                })
                tableTbodyEl.appendChild(tableTrEl);
                counterBy++;
            }
        })
        const accordionElItemHeaderBtnbadge = document.createElement('span');
        accordionElItemHeaderBtnbadge.classList.add("badge", "rounded-pill", "text-bg-secondary", "m-3");
        accordionElItemHeaderBtnbadge.textContent = counterBy;
        accordionElItemHeaderBtn.appendChild(accordionElItemHeaderBtnbadge);
    })
}