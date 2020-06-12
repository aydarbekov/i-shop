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

function compareAddSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    // $('#add-to-favorites-' + productPk).addClass('d-none');
    // $('#delete-from-favorites-' + productPk).removeClass('d-none');
}

function compareDeleteSuccess(data) {
    console.log(data);
    let productPk = data.pk;
    // $('#add-to-favorites-' + productPk).removeClass('d-none');
    // $('#delete-from-favorites-' + productPk).addClass('d-none');
}

function compareAdd(e) {
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
        .done(compareAddSuccess)
        .fail(console.log);
    location.reload()
}

function compareDelete(e) {
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
        .done(compareDeleteSuccess)
        .fail(console.log);
}

function setUpCompareButtons() {
    $('.compare-add').click(compareAdd);
    $('.compare-delete').click(compareDelete);
}
$(document).ready(setUpCompareButtons);