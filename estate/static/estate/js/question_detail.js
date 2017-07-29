$(function(){

    var $likeBtns = $(".like-btn");

    var $clickedBtn;
    var $voterForms = $('.vote-form');
    var user = $('#user');
    $voterForms.each(function(i,e){
        $(e).on('submit',function(evt){
            evt.preventDefault();
            var $form = $(evt.currentTarget)
            var url = $form.attr('action');
            var data = $form.serialize();
            if(user.data('isAuthenticated')){
                $.post(url, data, function (_data) {
                    if(_data.status != "Failed" && _data.status != "No Update"){
                        var id = $form.data('id');
                        $('#like'+id).text(_data.likes)
                        $('#dislike'+id).text(_data.dislikes);
                        $clickedBtn.siblings().toggleClass('like-btn-clicked', false);
                        $clickedBtn.toggleClass('like-btn-clicked');
                    }

                });
            }

        });
    });

    $likeBtns.each(function (i,e) {
        $(e).click(function(evt){
            $clickedBtn = $(evt.currentTarget);
            var id = $(evt.currentTarget).data('id');
            var bool = $(evt.currentTarget).data('bool');

            var $voteForm = $("#voteForm"+id);
            $voteForm.find('#id_answer').val(id);
            $voteForm.find('#id_is_like').val(bool);
            $voteForm.submit();
        });
    });


});