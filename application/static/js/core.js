document.addEventListener('DOMContentLoaded', function () {
    setupAlerts();

    if (window.self !== window.top) {
        const menu_button = document.getElementById('nt-btn-menu');
        const menu_button_divider = document.getElementById('nt-btn-menu-divider');
        const submenu_buttor = document.getElementById('nt-btn-submenu');

        menu_button.classList.remove('d-none');
        menu_button_divider.classList.remove('d-none');
        submenu_buttor.classList.remove('d-none');
    }

    document.querier_login = window.parent.document.querySelector('.v-filterselect-cuba-user-select-combobox input');
    if (document.querier_login) {
        console.log(document.querier_login.value);
    }

}, false);