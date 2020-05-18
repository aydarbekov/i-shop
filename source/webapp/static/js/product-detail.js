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