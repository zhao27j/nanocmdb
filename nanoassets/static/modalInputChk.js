import { baseMessagesAlertPlaceholder, baseMessagesAlert } from './baseMessagesAlert.js';

export function modalInputChk(e, refLst, modalEl, modalInputTag) {
    const modalInputEl = modalEl.querySelector('input');
    const modalInputValue = modalInputEl.value.trim();
    if ( !(modalInputValue in refLst) ) {
        // contractUpdModalInvalidSpan.innerHTML = `the given Contract [ ${modalInputValue} ] does NOT exist in the list`;
        // contractUpdModalInvalidSpan.className = 'invalid-feedback';

        baseMessagesAlert(`the given ${modalInputTag} [ ${modalInputValue} ] does NOT exist in the list`, 'warning');

        modalEl.querySelector("button[type='submit']").classList.add('disabled');

        modalInputEl.setCustomValidity(`the given ${modalInputTag} [ ${modalInputValue} ] does NOT exist in the list`);
        modalInputEl.value = '';
        modalInputEl.focus();

        e.preventDefault();
        e.stopPropagation();

        return false;

    } else {
        baseMessagesAlert(`the given Contract [ ${modalInputValue} ] is Valid`, 'info');

        // contractUpdModalInvalidSpan.innerHTML = "";
        modalInputEl.setCustomValidity("");
        modalEl.querySelector("button[type='submit']").classList.remove('disabled');

        return true;
    }
}