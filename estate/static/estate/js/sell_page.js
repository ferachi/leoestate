$(function () {
    $(".nav-pills a[data-toggle=tab]").on("click", function(e) {
        if ($(this).parent().hasClass("disabled")) {
            e.preventDefault();
            return false;
        }
    });

    var $radios = $('.estimate-option input[type="radio"]');
    $radios.on('change',function (evt) {
        var $radio = $(evt.currentTarget);
        var id = $radio.attr('id');
        if(id == 'sellRadio'){
            $('#formContainer').css('background-color', 'lavender');
        }
        else if(id=='estimateRadio'){
            $('#formContainer').css('background-color', 'aliceblue');
        }
    });




    var $stepOneSubmitBtn = $('#stepOneSubmitBtn');
    $stepOneSubmitBtn.on('click', function(evt){
        var data = $clientForm.serialize();
        var $btn = $(evt.currentTarget);
        var $errorField = $('.form-field-error');
        $errorField.hide();
        $errorField.text("");
        $errorField.siblings().removeClass('has-error');
        $.post($clientForm.attr('action'), data, function(data){
            if(data.success){
                // move to next tab
                var nextTab = $('#myTabs a:eq(1)');
                nextTab.tab('show');
                // nextTab.parent().addClass('active');
                nextTab.parent().removeClass('disabled');
                $('#myTabs a:eq(0)').parent().addClass('disabled');
            }
            else{
                if($btn.attr('id') == 'stepOneSubmitBtn'){
                    var errors = JSON.parse(data.errors);
                    if(Object.keys(errors).length > 1 && data.status == "Failed"){
                        Object.keys(errors).forEach(function(key){
                            if(key != 'year_constructed')
                            {
                                var errorKey = key.replace(/_([a-z])/g,function(match, letter){
                                        return letter.toUpperCase();
                                    }) + "Error";
                                var $errorParagraph = $('#'+ errorKey);
                                $errorParagraph.show();
                                $errorParagraph.text(errors[key][0]['message']);
                                $errorParagraph.siblings().addClass('has-error');
                            }
                        });
                    }
                    else{
                        // move to next tab
                        var nextTab = $('#myTabs a:eq(1)');
                        nextTab.tab('show');
                        // nextTab.parent().addClass('active');
                        nextTab.parent().removeClass('disabled');
                        $('#myTabs a:eq(0)').parent().addClass('disabled');
                    }
                }


            }
        })
    });

    var $stepTwoSubmitBtn = $('#stepTwoSubmitBtn');
    $stepTwoSubmitBtn.on('click', function(evt){
        var facilitiesString = '&client-facilities=';
        $(".inline-checkbox:checked").each(function(i,v){
            facilitiesString += this.value.trim().replace(/\s/g, "%20");
            if(i < $(".inline-checkbox:checked").length - 1) facilitiesString += ","
        });
        var data = customSerialize($clientForm,['client-facilities']) + facilitiesString;
        var $btn = $(evt.currentTarget);
        var $errorField = $('.form-field-error');
        $errorField.hide();
        $errorField.text("");
        $errorField.siblings().removeClass('has-error');
        $.post($clientForm.attr('action'), data, function(data){
            if(data.success){
                // move to next tab
                var nextTab = $('#myTabs a:eq(2)');
                nextTab.tab('show');
                nextTab.parent().removeClass('disabled');
                $('#myTabs a:eq(1)').parent().addClass('disabled');
            }
            else{
                if($btn.attr('id') == 'stepTwoSubmitBtn'){
                    console.log(data);
                    var errors = JSON.parse(data.errors);
                    Object.keys(errors).forEach(function(key){
                        var errorKey = key.replace(/_([a-z])/g,function(match, letter){
                                return letter.toUpperCase();
                            }) + "Error";
                        var $errorParagraph = $('#'+ errorKey);
                        $errorParagraph.show();
                        $errorParagraph.text(errors[key][0]['message']);
                        $errorParagraph.siblings().addClass('has-error');
                    });
                }
            }
        })
    });

    var $stepOneBackBtn = $('#stepOneBackBtn');
    $stepOneBackBtn.on('click', function (evt) {
        var prevTab = $('#myTabs a:eq(0)');
        prevTab.tab('show');
        prevTab.parent().removeClass('disabled');
        $('#myTabs a:eq(1)').parent().addClass('disabled');
    });

    var $stepTwoBackBtn = $('#stepTwoBackBtn');
    $stepTwoBackBtn.on('click', function (evt) {
        var prevTab = $('#myTabs a:eq(1)');
        prevTab.tab('show');
        prevTab.parent().removeClass('disabled');
        $('#myTabs a:eq(2)').parent().addClass('disabled');
    });


    $.get('/api/schedules/', function(data){
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
            $('#id_book-schedule_date').val(selectedDate.format("YYYY-MM-DD HH:mm:ss"));
            $('#displaySelectedTime strong').text(selectedDate.format("h:mm A"));
            $('#displaySelectedDate strong').text(selectedDate.format("dddd, DD MMMM YYYY"));
        })

        $('#bookingTime').on('change',function(evt){
            var $option = $(evt.currentTarget).find('option:selected');
            selectedDate = moment(selectedDate.format("MM/DD/YYYY ") + $option.text());
            $('#id_book-schedule_date').val(selectedDate.format("YYYY-MM-DD HH:mm:ss"));
            $('#displaySelectedTime strong').text(selectedDate.format("h:mm A"));
            $('#displaySelectedDate strong').text(selectedDate.format("dddd, DD MMMM YYYY"));
        });

    });
    $('#id_book-schedule_date').attr('type','hidden');
    var $dateTimePicker = $('#id_book-schedule_date').parent().addClass('date').attr('id', 'datetimepicker1');
    var $clientForm = $('#clientForm');

    $clientForm.submit(function(evt){
        evt.preventDefault();
        var $errorField = $('.form-field-error');
        $errorField.hide();
        $errorField.text("");
        $errorField.siblings().removeClass('has-error');

        var facilitiesString = '&client-facilities=';
        $(".inline-checkbox:checked").each(function(i,v){
            facilitiesString += this.value.trim().replace(/\s/g, "%20");
            if(i < $(".inline-checkbox:checked").length - 1) facilitiesString += ","
        });
        var data = customSerialize($clientForm,['client-facilities']) + facilitiesString;
        $.post($clientForm.attr('action'), data, function(data){
            if(data.success && data.status == "Complete"){
                $('#formsHolder').toggle();
                $('#finish').toggle();
            }
            else{
                var errors = JSON.parse(data.errors);
                Object.keys(errors).forEach(function(key){
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

    $("#thankYouBtn").on('click', function(evt){

        var tab = $('#myTabs a:eq(0)');
        tab.tab('show');
        tab.parent().removeClass('disabled');
        $('#myTabs a:eq(2)').parent().addClass('disabled');
        $('#clientForm')[0].reset();
        $('#formsHolder').show();
        $('#finish').hide();

    });

    $('#clientForm').on('reset',function(){
         var $errorField = $('.form-field-error');
        $errorField.hide();
        $errorField.css('display','none');
        $errorField.text("");
        $errorField.siblings().removeClass('has-error');
    })
});


function customSerialize(jForm,excludeFieldList){
    var initData = jForm.serializeArray();
    var _excludeList = excludeFieldList || [];
    var serializedString = "";
    if(!Array.isArray(_excludeList)){
        _excludeList = [];
    }
    for(var i=0; i < initData.length; i++){
        var err = -1;
        for(var j in initData[i]){
            err = _excludeList.findIndex(function (elem) {
                return elem == initData[i][j];
            });
            if(err != -1) break;
        }
        if(err != -1) continue;
        serializedString += stringifyObject(initData[i]);
        serializedString = i == initData.length - 1 ? serializedString : serializedString + "&";
    }
    return serializedString;

    function stringifyObject(obj){
        return obj['name'].trim() +"="+ obj['value'].trim().replace(/\s/g, "%20");
    }
}