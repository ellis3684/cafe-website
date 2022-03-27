$('.flip-btn').click(function() {
    $(this).closest('.card-container').toggleClass('hover');
    $(this).css('transform, rotateY(180deg)');
});
