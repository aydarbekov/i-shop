function slick() {
    $('.category-cards').slick({
        centerMode: true,
        centerPadding: '60px',
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 2,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    centerMode: false,
                    slidesToShow: 3,
                    slidesToScroll: 2,
                    infinite: false,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    arrows: false,
                    centerMode: false,
                    slidesToShow: 2,
                    slidesToScroll: 2,
                    infinite: false,

                }
            }
        ]
    });
}
function godown() {
    const last = $('.category-card:last-child');
    const all = $('.slick-track').children();
    const a = $('.slick-track div:nth-child(4n)');
    let count_for_third = -20;
    let count_for_fourth = -10;
    for (let i = 0; i < a.length; i++) {
        a[i].previousSibling.style.position = 'absolute';
        a[i].previousSibling.style.top = '110%';
        count_for_third = count_for_third + 20;
        a[i].previousSibling.style.left = count_for_third + '%';
        a[i].style.position = 'absolute';
        a[i].style.top = '110%';
        count_for_fourth = count_for_fourth + 20;
        a[i].style.left = count_for_fourth + '%'
    }
    if (all.length % 4 === 3) {
        last[0].style.position = 'absolute';
        last[0].style.top = '110%';
        count_for_third = count_for_third + 20;
        last[0].style.left = count_for_third + '%';
    }
}
function goup() {
    const a = $('.slick-track div:nth-child(4n)');
    for (let i = 0; i < a.length; i++) {
        a[i].previousSibling.style.position = 'static';
        a[i].style.position = 'static';
    }
}
$(document).ready(function(){
    $('.cart').click(function() {
        $('.empty-collapse')[0].style.display = 'block';
        $('.cart-modal').slideToggle(500);
    });
    $('.empty-collapse').click(function() {
        $( ".cart" ).click();
        $('.empty-collapse')[0].style.display = 'none';

    });
    slick();
    if(document.documentElement.clientWidth < 768) {
        godown();
    }
    $(window).resize(function() {
        if(document.documentElement.clientWidth < 768) {
            godown();
        }
        if(document.documentElement.clientWidth >= 768) {
            goup();
        }
    });

});