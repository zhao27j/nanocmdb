'use strict'

const inputChk = (inputEl, optLst = null, orig = null) => {

    let chkAlert, chkAlertType, inputChkResult = true
    
    if (orig != null && orig == inputEl.value) {
        chkAlert = `no changes`;
        inputChkResult = 'noChg';
    }

    if (inputEl.required) {
        if (inputEl.value.trim() == '') {
            chkAlert = `the given ${inputEl.id.replaceAll('_', ' ')} [ ${inputEl.value.trim()} ] is Empty`;
            inputChkResult = false;
        }
    }

    if (inputEl.type == 'number' && inputEl.value < 0) {
        inputEl.value = Math.abs(inputEl.value);
    }

    if (inputEl.type == 'number' && inputEl.value == '0') {
        chkAlert = `the given ${inputEl.id.replaceAll('_', ' ')} [ ${inputEl.value.trim()} ] is Invalid`;
        inputChkResult = false;
    }

    if (optLst && !(inputEl.value.trim() in optLst)) {
        chkAlert = `the given ${inputEl.id.replaceAll('_', ' ')} [ ${inputEl.value.trim()} ] does NOT exist in the Option List`;
        inputChkResult = false;
    }

    ['text-danger', 'border-bottom', 'border-danger'].forEach(t => inputEl.classList.toggle(t, !inputChkResult));
    ['border-success'].forEach(t => inputEl.classList.toggle(t, inputChkResult));

    inputChkResult == true ? inputEl.nextElementSibling.innerHTML = "" : inputEl.nextElementSibling.innerHTML = chkAlert;

    return inputChkResult;
}

export { inputChk };