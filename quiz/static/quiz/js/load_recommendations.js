var paginate_by = 10
function loadRecommendations() {
    $('.load_recommendation_button').click(function(event){
    var load_button = $(this);
    var offset = load_button.data('offset');
    var feedback_id = load_button.data('feedback-id');
        $.ajax(load_button.data('url'), {
            'type': 'GET',
            'async': true,
            'dataType': 'json',
            'data': {
                'offset': offset,
                'feedback_id': feedback_id,
                'paginate_by': paginate_by,
            },
            'error': function(xhr, status, error) {
                console.log(error, status);
            },
            'success': function(data, status, xhr){
                 offset = (parseInt(offset) + paginate_by).toString();
                 load_button.data({'offset': offset});

                 var ul_item = load_button.prev();
                 $.each(data['recommendations'], function(index, recommendation) {
                    ul_item.append('<li>'+ recommendation +'</li>');
                 });

                 if(data['end'] === 'end') {
                   load_button.hide();
                 }
            }
        });
    });
}


$(document).ready(function(){
    loadRecommendations();
});
