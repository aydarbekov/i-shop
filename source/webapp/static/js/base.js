dropdown_listener();
let dropdown = false;

function add_dropdown_toggle(){
    info_btns = $('.info-btn');
    for(let i = 0; i<info_btns.length; i++){
        info_btns[i].classList.add('dropdown-toggle')
    }
    dropdown = true
}
function remove_dropdown_toggle(){
    info_btns = $('.info-btn');
    for(let i = 0; i<info_btns.length; i++){
        info_btns[i].classList.remove('dropdown-toggle')
    }
    dropdown = false
}
function dropdown_listener(){
    info_btns = $('.info-btn');
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
if(document.documentElement.clientWidth <= 768) {
    add_dropdown_toggle();

}
$(window).resize(function() {
    if(document.documentElement.clientWidth <= 768) {
        if (!dropdown){
            add_dropdown_toggle()
        }
    }
    if(document.documentElement.clientWidth >= 768) {
        if (dropdown){
            remove_dropdown_toggle()
        }


    }
});