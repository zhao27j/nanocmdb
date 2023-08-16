import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

export function modalInputChk(e, optLst, chkLst, modalEl, modalInputTag) {
    const modalInput = modalEl.querySelector('input');
    const modalInputValue = modalInput.value.trim();
    
    if ( (modalInputTag != 'Owner' || modalInputValue != '') && !(modalInputValue in optLst) || modalInputValue in chkLst ) {

        baseMessagesAlert(`the given ${modalInputTag} [ ${modalInputValue} ] does NOT exist in the Option List, OR has been applied on one of the IT Assets selected`, 'warning');

        modalEl.querySelector("button[type='submit']").classList.add('disabled');

        modalInput.setCustomValidity(`the given ${modalInputTag} [ ${modalInputValue} ] does NOT exist in the Option List, OR has been applied on one of the IT Assets selected`);
        modalInput.value = '';
        modalInput.focus();

        e.preventDefault();
        e.stopPropagation();

        return false;

    } else {
        baseMessagesAlert(`the given ${modalInputTag} [ ${modalInputValue} ] is Valid`, 'info');

        modalInput.setCustomValidity("");
        modalEl.querySelector("button[type='submit']").classList.remove('disabled');

        return true;
    };

}