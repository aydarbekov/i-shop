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

function cartAddSuccess(data) {
    console.log(data);
    // let productPk = data.pk;
    // $('#cat-add-' + productPk).addClass('d-none');
    // $('#cart-' + productPk).removeClass('d-none');
}

function cartDeleteSuccess(data) {
    console.log(data);
    // let productPk = data.pk;
    // $('#cart-add-' + productPk).removeClass('d-none');
    // $('#cart-' + productPk).addClass('d-none');
}

function cartAdd(e) {
    e.preventDefault();
    let link = $(e.target);
    let href = link.attr('href');
    let product_pk = link.data('product-pk');
    let qtyFormsInput = $("#gty-" + product_pk);
    let qtyForms = qtyFormsInput.val();
    qtyFormsInput.val(parseInt(qtyForms) + 1);
    let totalFormsInput = $(".total-" + product_pk);
    let totalForms = totalFormsInput.text();
    let priceFormsInput = $(".price-" + product_pk);
    let priceForms = priceFormsInput.text();
    totalFormsInput.text(parseInt(totalForms) + parseInt(priceForms) + ',00');
    let cartTotalFormsInput = $(".cart-total");
    let cartForms = cartTotalFormsInput.text();
    let deliverPriceInput = $(".cart-summ-delivery");
    let deliveryPrice = deliverPriceInput.text();
    cartTotalFormsInput.text(parseInt(cartForms) + parseInt(priceForms) + ',00');
    $.ajax({
        method: 'post',
        url: href,
        data: {'pk': product_pk},
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .done(cartAddSuccess)
        .fail(console.log);
}

function cartDelete(e) {
    e.preventDefault();
    let link = $(e.target);
    let href = link.attr('href');
    let product_pk = link.data('product-pk');
    let qtyFormsInput = $("#gty-" + product_pk);
    let qtyForms = qtyFormsInput.val();
    qtyFormsInput.val(parseInt(qtyForms) - 1);
    let totalFormsInput = $(".total-" + product_pk);
    let totalForms = totalFormsInput.text();
    let priceFormsInput = $(".price-" + product_pk);
    let priceForms = priceFormsInput.text();
    totalFormsInput.text(parseInt(totalForms) - parseInt(priceForms) + ',00');
    let cartTotalFormsInput = $(".cart-total");
    let cartForms = cartTotalFormsInput.text();
    let deliverPriceInput = $(".cart-summ-delivery");
    let deliveryPrice = deliverPriceInput.text();
    cartTotalFormsInput.text(parseInt(cartForms) - parseInt(priceForms) + ',00');
    if (qtyForms <= 1) $(".product-" + product_pk).remove();
    $.ajax({
        method: 'post',
        url: href,
        data: {'pk': product_pk},
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
        .done(cartDeleteSuccess)
        .fail(console.log);
}

function setUpCartButtons() {
    $('.cartadd').click(cartAdd);
    $('.cartdelete').click(cartDelete);
}

$(document).ready(setUpCartButtons);
