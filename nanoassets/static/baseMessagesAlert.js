// page level Alert msg
const baseMessagesAlertPlaceholder = document.getElementById('baseMessagesAlertPlaceholder');
const baseMessagesAlert = (message, type) => {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('')

    // baseMessagesAlertPlaceholder.append(wrapper);
    baseMessagesAlertPlaceholder.firstChild ? baseMessagesAlertPlaceholder.replaceChild(wrapper, baseMessagesAlertPlaceholder.firstChild) : baseMessagesAlertPlaceholder.appendChild(wrapper);
}

export {baseMessagesAlertPlaceholder, baseMessagesAlert};