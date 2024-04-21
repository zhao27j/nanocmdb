'use strict'

document.addEventListener('keyup', e => {
    //if (!e.isComposing && e.ctrlKey && e.key.toLocaleLowerCase() == 'k') {
    if (e.ctrlKey && e.key.toLocaleLowerCase() == 'k') {
        const searchInputEl = document.querySelector("input[type='search']")
        searchInputEl.focus();
        searchInputEl.value = '';
    }
})

document.querySelectorAll("button.nav-link.dropdown-toggle[role='button'][data-bs-toggle='dropdown']").forEach(el => {
    const dropdownInstance = bootstrap.Dropdown.getOrCreateInstance(el);
    el.addEventListener('mouseover', e => {
        dropdownInstance.show();
    });
    el.nextElementSibling.addEventListener('mouseleave', e =>{setTimeout(() => { dropdownInstance.hide();}, 100);});

    el.parentElement.addEventListener('mouseleave', e => {setTimeout(() => {dropdownInstance.hide();}, 100);});
})

// <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">PR Mgmt</a>
// <li class="nav-item dropdown">