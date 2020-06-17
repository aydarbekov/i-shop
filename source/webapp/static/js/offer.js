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

function offerAddSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    $('#add-to-offer-' + productPk).addClass('d-none');
    $('#delete-from-offer-' + productPk).removeClass('d-none');
}

function offerDeleteSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    $('#add-to-offer-' + productPk).removeClass('d-none');
    $('#delete-from-offer-' + productPk).addClass('d-none');
}

function offerAdd(e) {
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
        .done(offerAddSuccess)
        .fail(console.log);
    location.reload()
}

function offerDelete(e) {
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
        .done(offerDeleteSuccess)
        .fail(console.log);
    location.reload()
}

function setUpOfferButtons() {
    $('.offer-add').click(offerAdd);
    $('.offer-delete').click(offerDelete);
}

$(document).ready(setUpOfferButtons);
