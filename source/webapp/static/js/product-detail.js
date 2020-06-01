$('.input-number__minus').on('click', function () {
    let total = $(this).next();
    if (total.val() > 1) {
        total.val(+total.val() - 1);
    };
});
$('.input-number__plus').on('click', function () {
    let total = $(this).prev();
    total.val(+total.val() + 1);
});
document.querySelectorAll('.input-number__input').forEach(function (el) {
    el.addEventListener('input', function () {
        this.value = this.value.replace(/[^\d]/g, '');
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// const baseUrl = 'http://localhost:8000/api-v2/';
//
// function getFullPath(path) {
//     path = path.replace(/^\/+|\/+$/g, '');
//     console.log(path, "THIS IS PATH");
//     path = path.replace(/\/{2,}/g, '/');
//     console.log(path, "THIS IS PATH");
//     return baseUrl + path + '/';
// }

function cartAddSuccess(data) {
    console.log(data);
}

function cartAdd(e) {
    e.preventDefault();
    let link = $(e.target);
    let href = link.attr('href');
    let product_pk = link.data('product-pk');
    let qtyFormsInput = $("#gty-" + product_pk);
    let qty = qtyFormsInput.val();
    $.ajax({
        method: 'post',
        url: href,
        data:  {'pk':product_pk, 'qty':qty},
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .done(cartAddSuccess)
        .fail(console.log);
}


function setUpCartButtons() {
    $('.cartadd').click(cartAdd);
}
$(document).ready(setUpCartButtons);
// $(document).ready(getFullPath);