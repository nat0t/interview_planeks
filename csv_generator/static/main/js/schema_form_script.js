window.onload = function () {
    // Adding row to form
    let columnForm = document.querySelectorAll(".column-form");
    let container = $("#schema-form");
    let addButton = $('#add-column');
    let totalForms = $("#id_schemadetails_set-TOTAL_FORMS");
    let formNum = columnForm.length - 1;

    addButton.on('click', addForm);

    function addForm(e){
        e.preventDefault();
        let newForm = columnForm[0].cloneNode(true);
        formNum++;
        newForm.innerHTML = newForm.innerHTML.replace(/schemadetails_set-(?<number>\d+)/g, `schemadetails_set-${formNum}`);
//        newForm.innerHTML = newForm.innerHTML.replace(/value=".*"/g, `value=""`);
        addButton.before(newForm);
        totalForms[0].setAttribute('value', `${formNum+1}`);
        };
};