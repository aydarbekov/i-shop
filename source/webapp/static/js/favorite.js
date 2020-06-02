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

function favoriteAddSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    $('#add-to-favorites-' + productPk).addClass('d-none').css('background-color', 'red');
    $('#delete-from-favorites-' + productPk).removeClass('d-none').css('background-color', 'white');
}

function favoriteDeleteSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    $('#add-to-favorites-' + productPk).removeClass('d-none');
    $('#delete-from-favorites-' + productPk).addClass('d-none');
}

function favoriteAdd(e) {
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
        .done(favoriteAddSuccess)
        .fail(console.log);
}

function favoriteDelete(e) {
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
        .done(favoriteDeleteSuccess)
        .fail(console.log);
}

function setUpFavoriteButtons() {
    $('.favorite-add').click(favoriteAdd);
    $('.favorite-delete').click(favoriteDelete);
}

$(document).ready(setUpFavoriteButtons);
