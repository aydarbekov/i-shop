// $(document).ready(function() {
    const pay_btn = $('.pay-btn').find('button');
    const agree = $('#agree');
    const pay_form = $("#pay-form");
    const empty_collapse = $('.empty-collapse-2');
    const modal_for_card = $('.modal-for-card')[0];

    agree.on('change', function() {
        if (agree.prop('checked') === true) {
            pay_btn[0].disabled = false
        }else {
            pay_btn[0].disabled = true
        }
    });
    let form_submit =  function (event){
        pay_form.submit();
    };
    let for_visa =  function (event){
        empty_collapse[0].style.display = 'block';
        modal_for_card.style.display='flex';
    };
    empty_collapse.click(function() {
        modal_for_card.style.display='none';
        empty_collapse[0].style.display = 'none';
    });

    pay_btn[0].addEventListener("click", form_submit);
    $('.method-radio input').on('change', function() {
        if ($('input[name=method]:checked', '.method-radio').val() === 'visa') {
            pay_btn[0].removeEventListener("click", form_submit);
            pay_btn[0].addEventListener("click", for_visa);
        }else if ($('input[name=method]:checked', '.method-radio').val() === 'cash') {
            pay_btn[0].removeEventListener("click", for_visa);
            pay_btn[0].addEventListener("click", form_submit);
        }

    });
// });
