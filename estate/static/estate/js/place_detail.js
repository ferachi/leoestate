$(function(){
    var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
    var $grid = $('.grid').imagesLoaded( function() {
        // init Masonry after all images have loaded
        $('.grid').show();
        $grid.masonry({
            // options
            itemSelector: '.grid-item',
            columnWidth: 150
        });
    });
    $('#pictureModal').modal({
        show:false
    });

    var $imgBtns = $('.img-btn');
    var images = $('.img-btn').find('img').toArray();

    $imgBtns.each(function(i,e){
        $(e).click(function(evt){
            var $img = $(evt.currentTarget).find('img');
            $('#modalImage').attr('src',$img.attr('src') );
            $('#modalImage').data('pos',$img.data('pos') );
            $('#modalTitle').text($img.attr('alt'));
        });
    });
    var $imgChangeBtns = $('#row .es-btn');
    $imgChangeBtns.each(function(i,e){
        $(e).click(function(evt){
            console.log(evt.currentTarget.id);
            var currentIndex = $('#modalImage').data('pos');
            var index;
            if(evt.currentTarget.id ==  "leftBtn")
                index = currentIndex > 1 ? currentIndex - 2 : images.length - 1;
            else
                index = currentIndex < images.length ? currentIndex : 0;
            var $myImg = $(images[index]);
            $('#modalImage').addClass('animated fadeOut')
                .one(animationEnd, function(){
                    $('#modalImage').attr('src',$myImg.attr('src'));
                    $('#modalImage').data('pos', $myImg.data('pos'));
                    $('#modalTitle').text($myImg.attr('alt'));
                    $('#modalImage').removeClass('animated fadeOut');
                    $('#modalImage').addClass('animated fadeIn').one(animationEnd,function(){
                        $('#modalImage').removeClass('animated fadeIn')
                    });

                });

        });
    });

    loadQuestions();
});



function loadQuestions(){
    var index = 0;
    var questionCount = 5;
    var rCount;

    // show main questions and detach from div
    var $questions = $(".main-question").show().detach();
    var limit = index + questionCount ;
    limit = limit < $questions.length ? limit : $questions.length;

    // show the first few questions based on questionCount
    for(var i = index; i < limit; i++){
        $('#qsAndAs').append($questions[i]);
    }
    index = limit;
    if(limit != $questions.length){
        rCount = $questions.length - index;
        $('#remainingCount').text(' ('+ rCount + ')');
    }
    else{
        $('#loadQuestionsBtn').addClass('disabled');
    }



    // load more questions with button
    $('#loadQuestionsBtn').click(function (e) {
        var limit = index + questionCount;
        limit = limit < $questions.length ? limit : $questions.length;
        // load if limit is less than total length
        if(limit <= $questions.length){
            for(var i = index; i < limit; i++){
                $('#qsAndAs').append($questions[i]);
            }

        }
        index = limit;
        if(limit == $questions.length){
            $(this).addClass('disabled');// else disable button
            $('#remainingCount').text('');
        }
        else{
            rCount = $questions.length - index;
            $('#remainingCount').text(' ('+ rCount + ')');
        }





    })
}