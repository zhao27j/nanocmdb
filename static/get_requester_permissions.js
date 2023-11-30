'use strict'


export function getRequesterPermissions() {
    const getUri = window.location.origin + '/json_response/requester_permissions/';

    return fetch(getUri
    ).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP error: ${response.status}`);
        }
    }).catch(error => {error ? console.error('Error:', error) : null;})
}

// export { getRequesterPermissions };