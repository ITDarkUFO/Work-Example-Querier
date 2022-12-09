const page_wrapper = document.querySelector('#page-wrapper');
const form_wrapper = page_wrapper.querySelector('#form-wrapper');
const table_wrapper = page_wrapper.querySelector('#table-wrapper');
const table = table_wrapper.querySelector('#table');
const table_head = table.querySelector('#table-head');
const table_body = table.querySelector('#table-body');

/**
 * Получает и отрисовывает страницу выбора параметров соответствующего отчета.
 * @param {string} pagename Название требуемой страницы.
 */
function openPage(pagename, app = 'server') {
    const results_counter_node = form_wrapper.querySelector('#results-counter');
    // Записываем название страницы и приложения
    window.pagename = pagename;
    window.app = app;

    // AJAX запрос на сервер
    const request = new XMLHttpRequest();
    request.open('GET', `/${app}/api/page?name=${pagename}`);

    request.setRequestHeader('Content-Type', 'text/html');
    request.addEventListener('readystatechange', () => {
        if (request.readyState === 4 && request.status === 200) {
            // Перерисовка контента

            // Очистка таблицы от предыдущих данных
            table_head.innerHTML = '';
            table_body.innerHTML = '';

            // Перерисовка страницы
            form_wrapper.innerHTML = request.responseText;

            // Очистка количества выведенных строк
            if (results_counter_node) {
                results_counter_node.innerText = '';
            }
        }
        else if (request.readyState === 4 && request.status !== 200) {
            alert('Не удалось загрузить страницу.', 'danger');
        }
    });

    request.send();
}

/**
 * Валидирует поля формы и отправляет запрос на составленный адрес api.
 */
function getReport() {
    let reportname = window.pagename;
    let app = window.app;

    const form = document.getElementById('formInput');
    const loading_icon = document.getElementById('loading-icon');

    let api_request = `/${app}/api/data?name=${reportname}`;

    // Валидация формы
    let error_catched = false;

    if (form != null) {
        let nodes = form.querySelectorAll('[data-validate]');

        nodes.forEach(node => {
            if (node.value != '') {
                node.classList.remove('is-invalid');
                api_request += `&${node.id}=${node.value}`;
            }
            else {
                node.classList.add('is-invalid');
                error_catched = true;
            }
        });

        const checkbox_nodes = form.querySelectorAll('[checkbox]');

        checkbox_nodes.forEach(node => {
            if (node.checked) {
                api_request += `&${node.id}=True`;
            }
            else {
                api_request += `&${node.id}=False`;
            }
        });
    }

    // Отправление запроса
    if (!error_catched) {
        // Отображение иконки загрузки отчета
        if (loading_icon != null)
            loading_icon.classList.remove('d-none');

        const request = new XMLHttpRequest();
        request.open('GET', api_request);

        request.setRequestHeader('Content-Type', 'application/x-www-form-url');
        request.addEventListener('readystatechange', () => {
            if (request.readyState === 4) {
                // Исчезновение иконки загрузки отчета
                if (loading_icon != null)
                    loading_icon.classList.add('d-none');

                if (request.status === 200)
                    drawTable(request.responseText);
                else
                    alert('Произошла ошибка! Проверьте параметры отчета или свяжитесь со специалистом.', 'danger');
            }
        });

        request.send();
    }
}

/**
 * Отрисовывает таблицу по полученным данным.
 * @param {string} json_string
 */
function drawTable(json_string) {
    const regex = new RegExp('<a .*>.*<\/a>');

    const print_button = document.getElementById('print-button');
    const results_counter_node = document.getElementById('results-counter');

    let results_counter = 0;

    // Очищение таблицы от предыдущих данных
    table_head.innerHTML = '';
    table_body.innerHTML = '';

    // Отображение кнопки печати
    print_button.classList.remove('d-none');

    // Заполнение таблицы
    const json_data = JSON.parse(json_string);
    const columns_data = json_data.columns;
    const entity_data = json_data.data;

    let tr = document.createElement('tr');
    for (let column in columns_data) {
        let td = document.createElement('td');
        for (let param in columns_data[column].parameters) {
            td.setAttribute(param, columns_data[column].parameters[param]);
        }

        td.textContent = columns_data[column].value;
        tr.appendChild(td);
    }

    table_head.appendChild(tr);

    for (let entity in entity_data) {
        results_counter++;
        let tr = document.createElement('tr');
        for (let property in entity_data[entity]) {
            let td = document.createElement('td');

            let entity_data_type = typeof (entity_data[entity][property].value);

            if (entity_data_type == 'string' && entity_data[entity][property].value.match(regex)) {
                let a = document.createElement('a');
                a.innerHTML = entity_data[entity][property].value;
                td.appendChild(a);
                tr.appendChild(td);
            }
            else {
                td.textContent = entity_data[entity][property].value;
                tr.appendChild(td);
            }
        }
        table_body.appendChild(tr);
    }

    let results_counter_string = `${getNoun(results_counter, 'Выведен', 'Выведено', 'Выведено')} ${results_counter} ${getNoun(results_counter, 'результат', 'результата', 'результатов')}`;
    if (results_counter_node) {
        results_counter_node.innerText = results_counter_string;
        table_wrapper.classList.remove('mt-4');
    }
    else {
        table_wrapper.classList.add('mt-4');
        console.log(results_counter_string);
    }
}

/**
 * 
 * @param {number} number - Число для которого нужно просклонять слово
 * @param {string} nominative - Слово в именительном падеже (... один ...)
 * @param {string} genitive - Слово в родительном падеже (... два ...)
 * @param {string} genitive_plural - Слово в родительном падеже множественного числа (... пять ...)
 * @returns Слово в нужном склонении
 */
function getNoun(number, nominative, genitive, genitive_plural) {
    let n = Math.abs(number);
    n %= 100;

    if (n >= 5 && n <= 20)
        return genitive_plural;

    n %= 10;

    if (n === 1)
        return nominative;

    if (n >= 2 && n <= 4)
        return genitive;

    return genitive_plural;
}
