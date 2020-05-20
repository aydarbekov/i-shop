$( function() {
    $( "#slider-range" ).slider({
        range: true,
        min: 0,
        max: 500,
        values: [ 75, 300 ],
        slide: function( event, ui ) {
            $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
        }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
        " - $" + $( "#slider-range" ).slider( "values", 1 ) );
} );
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