/**
 * Составляет Excel-файл из отрисованной таблицы и отправляет запрос на сохранение.
 */
function saveReport(type, fun, dl) {
    var elt = document.getElementById('table');
    var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet" });
    return dl ?
        XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }) :
        XLSX.writeFile(wb, fun || ('report.' + (type || 'xlsx')));
}