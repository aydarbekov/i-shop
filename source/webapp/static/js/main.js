// // const baseUrl = 'http://localhost:8000/api/v2/';
// //
// // function getFullPath(path) {
// //     path = path.replace(/^\/+|\/+$/g, '');
// //     path = path.replace(/\/{2,}/g, '/');
// //     return baseUrl + path + '/';
// // }
// //
// // function makeRequest(path, method, auth = true, data = null) {
// //     let settings = {
// //         url: getFullPath(path),
// //         method: method,
// //         dataType: 'json'
// //     };
// //     if (data) {
// //         settings['data'] = JSON.stringify(data);
// //         settings['contentType'] = 'application/json';
// //     }
// //     if (auth) {
// //         settings.headers = {'Authorization': 'Token ' + getToken()};
// //     }
// //     return $.ajax(settings);
// // }
// //
// // function saveToken(token) {
// //     localStorage.setItem('authToken', token);
// // }
// //
// // function getToken() {
// //     return localStorage.getItem('authToken');
// // }
// //
// // function removeToken() {
// //     localStorage.removeItem('authToken');
// // }
// //
// // function logIn(username, password) {
// //     const credentials = {username, password};
// //     let request = makeRequest('login', 'post', false, credentials);
// //     request.done(function (data, status, response) {
// //         console.log('Received token');
// //         saveToken(data.token);
// //     }).fail(function (response, status, message) {
// //         console.log('Could not get token');
// //         console.log(response);
// //     });
// // }
// //
// // $(document).ready(function () {
// //     let token = getToken();
// //     if (!token) logIn('admin', 'admin');
// // });
//
//
// /* Код с Лабораторной ESDP */
//
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
//
// function favoritesAddSuccess(data) {
//     console.log(data);
//     let adPk = data.pk;
//     $('#add-to-favorites-' + adPk).addClass('d-none');
//     $('#delete-from-favorites-' + adPk).removeClass('d-none');
// }
//
// function favoritesDeleteSuccess(data) {
//     console.log(data);
//     let adPk = data.pk;
//     $('#add-to-favorites-' + adPk).removeClass('d-none');
//     $('#delete-from-favorites-' + adPk).addClass('d-none');
// }
//
// function favoritesAdd(e) {
//     e.preventDefault();
//     let link = $(e.target);
//     let href = link.attr('href');
//     let ad_pk = link.data('ad-pk');
//     $.ajax({
//         method: 'post',
//         url: href,
//         data: {'pk': ad_pk},
//         headers: {
//             'X-CSRFToken': getCookie('csrftoken')
//         }
//     })
//         .done(favoritesAddSuccess)
//         .fail(console.log);
// }
//
// function favoritesDelete(e) {
//     e.preventDefault();
//     let link = $(e.target);
//     let href = link.attr('href');
//     let ad_pk = link.data('ad-pk');
//     $.ajax({
//         method: 'post',
//         url: href,
//         data: {'pk': ad_pk},
//         headers: {
//             'X-CSRFToken': getCookie('csrftoken')
//         }
//     })
//         .done(favoritesDeleteSuccess)
//         .fail(console.log);
// }
//
// function setUpFavoriteButtons() {
//     $('.favorites-add').click(favoritesAdd);
//     $('.favorites-delete').click(favoritesDelete);
// }
//
// $(document).ready(setUpFavoriteButtons);

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
let a = $('.slick-track div:nth-child(4n)');
let dropdown = false;

function godown() {
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
}
function goup() {
    for (let i = 0; i < a.length; i++) {
        a[i].previousSibling.style.position = 'static';
        a[i].style.position = 'static';
    }
}
let info_btns = $('.info-btn');
function add_dropdown_toggle(){
    for(let i = 0; i<info_btns.length; i++){
        info_btns[i].classList.add('dropdown-toggle')
    }
    dropdown = true
}
function remove_dropdown_toggle(){
    for(let i = 0; i<info_btns.length; i++){
        info_btns[i].classList.remove('dropdown-toggle')
    }
    dropdown = false
}
function dropdown_listener(){
    for(let i = 0; i<info_btns.length; i++){
        info_btns[i].addEventListener("click", function(){
            if (!info_btns[i].parentElement.classList.contains('dropup')){
                info_btns[i].parentElement.classList.add('dropup');
            } 	else {
                info_btns[i].parentElement.classList.remove('dropup');
            }
        });
    }
}
$(document).ready(function(){
    dropdown_listener();
    slick();
    if(document.documentElement.clientWidth < 768) {
        godown();
        add_dropdown_toggle();

    }
    $(window).resize(function() {
        if(document.documentElement.clientWidth < 768) {
            godown();
            if (!dropdown){
                add_dropdown_toggle()
            }
        }
        if(document.documentElement.clientWidth >= 768) {
            if (dropdown){
                remove_dropdown_toggle()
            }
            goup();


        }
    });

});