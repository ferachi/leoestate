$(function(){
    moment.locale('fr');
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

    var selectedDate;
    $.get('/api/schedules/', function(data){
        console.log(data, "DATA")
        var dates = [];

        data.schedules.forEach(function(v){
            dates.push(moment(v['scheduled_date']));
        });
        var dateGroup = {};
        dates.forEach(function (m,i) {
            var key = m.format('DD/MM/YYYY');
            var val = m.format('h:mm A');
            console.log(val);
            if(dateGroup[key]){
                dateGroup[key].push(val);
            }else{
                dateGroup[key] = [val];

            }
        });

        $('#datetimepicker1').datetimepicker({
            format : 'DD/MM/YYYY',
            inline : true,
            sideBySide:true,
            enabledDates: dates,
            locale:'fr',

        });
        $('#datetimepicker1').on("dp.change",function(e){
            $("#bookingTime").empty();
            var times = dateGroup[e.date.format('DD/MM/YYYY')];
            times.forEach(function (time) {
                $("#bookingTime").append("<option value='"+time+"'>"+time+"</option>");
            });
            var time = times[0];
            selectedDate = moment(e.date.format("MM/DD/YYYY ") + time);

            $('#notSelected').hide();
            $('#dateSelected').show();
            console.log(selectedDate);
            $('#id_schedule_date').val(selectedDate.format("YYYY-MM-DD HH:mm:ss"));
            $('#displaySelectedTime strong').text(selectedDate.format("h:mm A"));
            $('#displaySelectedDate strong').text(selectedDate.format("dddd, DD MMMM YYYY"));
        })

        $('#bookingTime').on('change',function(evt){
            var $option = $(evt.currentTarget).find('option:selected');
            selectedDate = moment(selectedDate.format("MM/DD/YYYY ") + $option.text());
            $('#id_schedule_date').val(selectedDate.format("YYYY-MM-DD HH:mm:ss"));
            $('#displaySelectedTime strong').text(selectedDate.format("h:mm A"));
            $('#displaySelectedDate strong').text(selectedDate.format("dddd, DD MMMM YYYY"));
            console.log(selectedDate);
        });

    });
    var $bookingForm = $('#bookingForm');

    $bookingForm.submit(function(evt){
        evt.preventDefault();
        var $errorField = $('.form-field-error');
        $errorField.hide();
        $errorField.text("");
        $errorField.siblings().removeClass('has-error');

        var data = $bookingForm.serialize();
        $.post($bookingForm.attr('action'), data, function(data){
            console.log(data.success)
            if(data.success){
                $('#formWindow').hide();
                $('#successWindow').show();
                $('#successBtn').click(function(e){
                    setTimeout(function () {
                        $('#successWindow').hide();
                        $bookingForm[0].reset();
                        $('#formWindow').show();
                    }, 1000);

                })
            }
            else{

                var errors = JSON.parse(data.errors);console.log(errors);
                Object.keys(errors).forEach(function(key){
                    console.log(key);
                    var errorKey = key.replace(/_([a-z])/g,function(match, letter){
                            return letter.toUpperCase();
                        }) + "Error";
                    var $errorParagraph = $('#'+ errorKey);
                    $errorParagraph.show();
                    $errorParagraph.text(errors[key][0]['message']);
                    $errorParagraph.siblings().addClass('has-error');
                });
            }
        })
    });
    $('#id_schedule_date').attr('type','hidden');
    var $dateTimePicker = $('#id_schedule_date').parent().addClass('date').attr('id', 'datetimepicker1');
    
    var $downloadForm = $("#myDownloadForm");
    $("#downloadBtn").click(function(evt){
        evt.preventDefault();
       $downloadForm.submit();
    });
    $downloadForm.submit(function(evt){
        evt.preventDefault();
        var data = $downloadForm.serialize();
       $.post($downloadForm.attr('action'),data, function(_data){
           if(_data.success){
               window.location = $("#downloadBtn").attr('href');
           }

       });
    });
    
});



function loadQuestions(){
    var index = 0;
    var questionCount = 1;
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
        $('#loadQuestionsBtn').show();
    }
    else{
        $('#loadQuestionsBtn').hide();
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