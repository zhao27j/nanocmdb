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
        
    }).catch(error => {console.error('Error:', error);})


const legalEntitiesBtnByPrjct = document.querySelector("#legalEntitiesBtnByPrjct");
const legalEntitiesBtnByType = document.querySelector("#legalEntitiesBtnByType");

const legalEntitiesAccordion = document.querySelector("#legalEntitiesAccordion");

legalEntitiesBtnByPrjct.addEventListener('click', e => {});

legalEntitiesBtnByType.addEventListener('click', e => reLst(legalEntitiesAccordion, 'type', legalEntityTypes, 'legalEntities', legalEntities, ['name', 'prjct', 'code']));

function reLst(accordionEl, lstByTag, lstBy, idOfTblTdPrefix, rows, cols) {
    // if (lstByTag == 'Type') {tableTh = 'Project';} else if (lstByTag == 'Project') {tableTh = 'Type';}

    accordionEl.innerHTML = "";

    lstBy.forEach((valueBy, keyBy, mapBy) => {
        const accordionItem = document.createElement('div');
        accordionItem.classList.add("accordion-item");
        accordionItem.innerHTML = [
            `<h2 class="accordion-header">`,
                `<button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">`,
                    `${keyBy}`,
                `</button>`,
            `</h2>`,
            `<div id="collapseOne" class="accordion-collapse collapse show" data-bs-parent="#accordionExample">`,
                `<div class="accordion-body" id="accordionElBody${keyBy}"></div>`,
            `</div>`,
        ].join('');
        
        accordionEl.appendChild(accordionItem);
        const accordionElBody = accordionEl.querySelector(`#accordionElBody${keyBy}`);

        const tableEl = document.createElement('table');
        tableEl.id = `${idOfTblTdPrefix}Tbl`;
        ['table', 'table-striped', 'table-hover', 'fw-light'].forEach(element => tableEl.classList.add(element));
        // tableEl.classList.add('table table-striped table-hover fw-light');
        accordionElBody.appendChild(tableEl);

        let tableTrEl = document.createElement('tr');
        tableTrEl.innerHTML = '<th></th>';
        cols.forEach(col => {
            const tabelThEl = document.createElement('th');
            tabelThEl.innerHTML = `<small>${col}</small>`;
            tableTrEl.appendChild(tabelThEl);
        })
        tableEl.appendChild(tableTrEl);

        rows.forEach(row => {
            if (row.fields[`${lstByTag}`] == lstBy.get(`${keyBy}`)) {
                tableTrEl = document.createElement('tr');
                tableTrEl.innerHTML = `<td><input type="checkbox" name="legal_entity" id="legal_entity{{ forloop.counter }}" value="{{ legal_entity.pk }}"/></td>`;
                cols.forEach(col => {

                    const tabelTdEl = document.createElement('td');
                    
                    const smallEl = document.createElement('small');
                    smallEl.id = `${idOfTblTdPrefix}TblTd${col}`;
                    smallEl.textContent = row.fields[`${col}`];
                    
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
                tableEl.appendChild(tableTrEl);
            }
        })
    })
}