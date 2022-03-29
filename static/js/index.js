//Provides the cafe card flip function on the index.html page
$('.flip-btn').click(function() {
    $(this).closest('.card-container').toggleClass('hover');
    $(this).css('transform, rotateY(180deg)');
});



//Replaces browser input validation with Bootstrap validation for the search by location search bar in home route navbar
(function () {
  'use strict'
  var forms = document.querySelectorAll('.needs-validation')
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }
        form.classList.add('was-validated')
      }, false)
    })
})()
