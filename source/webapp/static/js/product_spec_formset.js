function setSpecsFormId(form, formsNumber) {
    let formId = 'specs-' + formsNumber;
    let oldId = form.prop('id');
    form.prop('id', formId);

    let fields = ['name', 'value', 'id'];
    fields.forEach(function(field) {
        let element = form.find('#id_' + oldId + '-' + field);
        let fieldName = formId + '-' + field;
        element.prop('name', fieldName);
        element.prop('id', 'id_' + fieldName);
    });

    let deleteButton = form.find('.btn-danger');
    deleteButton.data('id', formId);
}

function formSpecsReset(form) {
    let formId = form.prop('id');
    form.removeClass('d-none');

    let fields = ['name', 'value', 'id'];
    fields.forEach(function(field) {
        let element = form.find('#id_' + formId + '-' + field);
        element.val('');
    });

    let deleteCheckbox = form.find('#id_' + formId + '-' + 'DELETE');
    deleteCheckbox.prop('checked', false);

    let errors = form.find('.text-danger');
    errors.remove();

    let deleteButton = form.find('.btn-danger');
    deleteButton.off('click');
    deleteButton.click(deleteSpecsForm);
}

let newForm =$("#specs_forms .form-row").first().clone();

function addSpecsForm (event) {
    let totalFormsInput = $("#id_speсifications-TOTAL_FORMS");
    let maxFormsInput = $("#id_speсifications-MAX_NUM_FORMS");
    console.log(maxFormsInput);
    let totalForms = totalFormsInput.val();
    let maxForms = maxFormsInput.val();
    if(totalForms === maxForms) {
        alert('Максимальное количество добавлено!');
    } else{
        let firstForm = newForm.clone();
        setSpecsFormId(firstForm, totalForms);
        formSpecsReset(firstForm);
        $("#specs_forms").append(firstForm);
        totalFormsInput.val(parseInt(totalForms) + 1);
    }
}

function deleteSpecsForm(event) {
    let totalFormsInput = $("#id_speсifications-TOTAL_FORMS");
    // let minFormsInput = $("#id_images-MIN_NUM_FORMS");
    let totalForms = totalFormsInput.val();
    // let minForms = minFormsInput.val();
    // if(totalForms === minForms) {
    //     alert('В заказе должно быть хотя бы ' + minForms + " товар(а/ов).");
    // } else
    // {
        let formId = $(event.target).data('id');
        console.log(formId);
        let form = $("#" + formId);
        console.log(form);
        let idInput = form.find('#id_' + formId + '-id');
        if (idInput.val()) {
            let deleteCheckbox = form.find('#id_' + formId + '-DELETE');
            form.addClass('d-none');
            deleteCheckbox.prop('checked', true);
        } else {
            form.remove();
            totalFormsInput.val(parseInt(totalForms) - 1);
        }

        let forms = $("#specs_forms .form-row");
        for(let i = 0; i < forms.length; i++) {
            setFormId($(forms[i]), i);
        }
    // }
}

$(document).ready(function() {
    $('#add_specs_form').click(addSpecsForm);
    $('#specs_forms button.btn-danger').click(deleteSpecsForm)
});