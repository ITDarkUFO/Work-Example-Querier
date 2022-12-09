function alert() { }
const delay = ms => new Promise(res => setTimeout(res, ms));

const Types = {
    PRIMARY: 'primary',
    SECONDARY: 'secondary',
    SUCCESS: 'success',
    DANGER: 'danger',
    WARNING: 'warning',
    INFO: 'info',
    LIGHT: 'light',
    DARK: 'dark'
};

/**
 * Настраивает систему создания и последовательного удаления alert'ов.
 */
function setupAlerts() {
    const max_alerts_count = 5;
    const placeholder = document.getElementById('alerts-wrapper');

    // Асинхронная функция удаления alert'ов
    const removeAlert = async (id) => {
        await delay(5000);
        document.getElementById(id).classList.remove('show');
        await delay(1000);
        document.getElementById(id).remove();
    };

    // Создание alert'ов
    /* jshint -W021 */
    alert = (message, type = Types.INFO) => {
        const wrapper = document.createElement('div');
        wrapper.classList = `alert alert-${type} alert-dismissible fade show`;
        wrapper.role = 'alert';
        wrapper.innerHTML = [
            `   <div>${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        ].join('');
        wrapper.id = 'alert-' + placeholder.childElementCount;

        if (placeholder.childElementCount > max_alerts_count)
            placeholder.childNodes.item(max_alerts_count).replaceWith(wrapper);
        else
            placeholder.insertAdjacentElement("beforeend", wrapper);

        removeAlert(wrapper.id);
    };
    /* jshint +W021 */
}