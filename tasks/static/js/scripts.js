$(document).ready(function() {

    var baseUrl = 'http://localhost:8000/';
    var deleBtn = $('.delete-btn');
    var searchBtn = $('#search-btn');
    var searchForm = $('#search-form');
    var filter = $('#filter');

    $(deleBtn).on('click', function(e) {
        e.preventDefault();

        var delLink = $(this).attr('href');
        var result = confirm('Quer deletar esta tarefa?');

        if (result) {
            window.location.href = delLink;
        }

    });

    $(searchBtn).on('click', function() {
        searchForm.submit()
    })

    $(filter).change(function() {
        filter = $(this).val();
        if (filter == 'none') {
            return;
        } 
        window.location.href = baseUrl + '?filter=' + filter;
    });
});

