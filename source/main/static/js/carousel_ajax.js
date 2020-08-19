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

function carouselAddSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    $('#carousel-add-' + productPk).addClass('d-none');
    $('#carousel-delete-' + productPk).removeClass('d-none');
}

function carouselDeleteSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    $('#carousel-add-' + productPk).removeClass('d-none');
    $('#carousel-delete-' + productPk).addClass('d-none');
}

function carouselAdd(e) {
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
        .done(carouselAddSuccess)
        .fail(console.log);
}

function carouselDelete(e) {
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
        .done(carouselDeleteSuccess)
        .fail(console.log);
}

function setUpCarouselButtons() {
    $('.carouseladd').click(carouselAdd);
    $('.carouseldelete').click(carouselDelete);
}

$(document).ready(setUpCarouselButtons);
