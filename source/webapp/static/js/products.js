// $( function() {
//     $( "#slider-range" ).slider({
//         range: true,
//         min: 0,
//         max: 500,
//         values: [ 75, 300 ],
//         slide: function( event, ui ) {
//             $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
//         }
//
//     });
//     $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
//         " - $" + $( "#slider-range" ).slider( "values", 1 ) );
// } );
$( ".filter-slider-appereance-btn" ).click(function() {
    let filter_block = $("#collapseExample1")[0];
    if (filter_block.style.display === '' || filter_block.style.display === 'none') {
        $( "#collapseExample1" )[0].style.animationName = 'widthchange';
        $( "#collapseExample1" )[0].style.left = '0';
        $( "#collapseExample1" )[0].style.display='block';
        $('.empty-collapse')[0].style.display = 'block';

    }else if (filter_block.style.display === 'block'){
        $( "#collapseExample1" )[0].style.animationName = 'widthchangenone';
        $( "#collapseExample1" )[0].style.left = '-280px';
        $('.empty-collapse')[0].style.display = 'none';
        setTimeout(function () {
            $( "#collapseExample1" )[0].style.display='none';
        }, 1000);
    }
});
$('.empty-collapse').click(function() {
    $( ".filter-slider-appereance-btn" ).click();
});

$( function() {
    $( "#slider-range" ).slider({
        range: true,
        min: 0,
        max: 3000,
        values: [ 15, 1000 ],
        slide: function( event, ui ) {
            $( "#amount" ).val( ui.values[ 0 ]+" с."  +  " - " + ui.values[ 1 ] + " с." );
            var array_elements = jQuery.makeArray($(".products"));
            var array_price = jQuery.makeArray($(".product-price"));
            var array_elements_length = array_elements.length;
            var array = [];
            var price_array = [];
            var min_value = ui.values[0];
            var max_value = ui.values[1];
            for(var i=0; i<array_elements_length; i++) {
                array.push(parseInt(array_elements[i].getAttribute('id')));
                price_array.push(parseInt(array_price[i].getAttribute('id')));
            }
            // var for_show = [];
            let product_show = [];
            console.log(product_show, "THIS IS PRODUCT SHOW");
            var product_hide = [];
             console.log(product_hide, "THIS IS PRODUCT Hide");
            for (i in price_array) {
                if (price_array[i] >= min_value && price_array[i] <= max_value) {
                    // for_show.push(price_array[i]);
                    product_show.push(array[i]);
                    console.log(product_show, "PRODUCT SHOW ADDED ARRAY");
                 // $('.product-pk-element-'+product_show[i]).show();
                }
                else {
                    product_hide.push(array[i]);
                    console.log(product_hide, "PRODUCT HIDE ADDED ARRAY");
                    // $('.product-pk-element-'+product_hide[i]).hide();
                }
}
            for (i in product_show){
                $('.product-pk-element-'+product_show[i]).show();
            }
            for (i in product_hide){
                $('.product-pk-element-'+product_hide[i]).hide();
            }
        }


    });
    $( "#amount" ).val(  $( "#slider-range" ).slider( "values", 0 ) + " с." +
        " - " + $( "#slider-range" ).slider( "values", 1 ) + " с." );
} );