'use strict'

document.addEventListener('keyup', e => {
    //if (!e.isComposing && e.ctrlKey && e.key.toLocaleLowerCase() == 'k') {
    if (e.ctrlKey && e.key.toLocaleLowerCase() == 'k') {
        const searchInputEl = document.querySelector("input[type='search']")
        searchInputEl.focus();
        searchInputEl.value = '';
    }
})

document.querySelectorAll("a.nav-link.dropdown-toggle[role='button'][data-bs-toggle='dropdown']").forEach(e => {

    const dropdownInstance = bootstrap.Dropdown.getOrCreateInstance(e);
    e.addEventListener('mouseover', e => {dropdownInstance.show();});
    // e.closest('li.nav-item.dropdown').addEventListener('mouseleave', e =>{setTimeout(() => { dropdownInstance.hide();}, 300);});
    e.parentElement.addEventListener('mouseleave', e =>{setTimeout(() => { dropdownInstance.hide();}, 100);});
     
})

// <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">PR Mgmt</a>
// <li class="nav-item dropdown">