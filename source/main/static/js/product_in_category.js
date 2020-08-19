// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

function productAddSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    $('#product-in-category-add-' + productPk).addClass('d-none');
    $('#product-in-category-delete-' + productPk).removeClass('d-none');
}

function productDeleteSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    $('#product-in-category-add-' + productPk).removeClass('d-none');
    $('#product-in-category-delete-' + productPk).addClass('d-none');
}

function productAdd(e) {
    e.preventDefault();
    let link = $(e.target);
    let href = link.attr('href');
    let product_pk = link.data('product-pk');
    $.ajax({
        method: 'post',
        url: href,
        data: {'pk': product_pk},
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .done(productAddSuccess)
        .fail(console.log);
}

function productDelete(e) {
    e.preventDefault();
    let link = $(e.target);
    let href = link.attr('href');
    let product_pk = link.data('product-pk');
    $.ajax({
        method: 'post',
        url: href,
        data: {'pk': product_pk},
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .done(productDeleteSuccess)
        .fail(console.log);
}

function setUpProductButtons() {
    $('.product-in-category-add').click(productAdd);
    $('.product-in-category-delete').click(productDelete);
}

$(document).ready(setUpProductButtons);