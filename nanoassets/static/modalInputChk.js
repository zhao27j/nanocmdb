import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

let chkResult, chkAlert;
export function modalInputChk(e, optLst, chkLst, modalEl, modalInputTag) {
    const modalInput = modalEl.querySelector('input');
    const modalInputValue = modalInput.value.trim();
    
    // if ( (modalInputTag != 'owner' || modalInputValue != '') && !(modalInputValue in optLst) || modalInputValue in chkLst ) {    
    chkResult = true;
    if (modalInputTag == 'status' && modalInputValue in optLst) {
        const chkLstDisposal = Object.values(chkLst);
        if (
            modalInputValue == 'Scraping' && ['inUSE', 'inREPAIR', 'SCRAPPED', 'scrappingRequested', 'buyBACK', 'reUSE'].some(i => chkLstDisposal.includes(i))
        ) {
            chkResult = false;
            chkAlert = "only Available IT assets could be applied for Scrapping";
        }
        else if (
            (modalInputValue == 'Reusing' || modalInputValue == 'Buying back') && ['inUSE', 'inREPAIR', 'AVAILABLE', 'scrappingRequested', 'buyBACK', 'reUSE'].some(i => chkLstDisposal.includes(i))
        ) {
            chkResult = false;
            chkAlert = "only Scrapped IT assets could be applied for Resuing / Buying back";
        }
    } else if (!(modalInputValue in optLst) || modalInputValue in chkLst) {
        chkResult = false;
        chkAlert = `the given ${modalInputTag} [ ${modalInputValue} ] does NOT exist in the Option List, Or has been applied on one of the IT Assets selected`;
    }

    if (chkResult) {
        baseMessagesAlert(`the given ${modalInputTag} [ ${modalInputValue} ] is Valid`, 'info');
        modalEl.querySelector("button[type='submit']").classList.remove('disabled');
        modalInput.setCustomValidity("");
        return true;
    } else {
        baseMessagesAlert(chkAlert, 'warning');
        modalEl.querySelector("button[type='submit']").classList.add('disabled');
        modalInput.setCustomValidity(chkAlert);
        modalInput.value = '';
        modalInput.focus();
        e.preventDefault();
        e.stopPropagation();
        return false;
    };
}