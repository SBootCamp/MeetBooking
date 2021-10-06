$(document).ready(function () {
          // отслеживаем событие отправки формы
          $('#bookingForm').submit(function () {
              // создаем AJAX-вызов
              $.ajax({
                  data: {
                      // start_time = $().serialize(),
                      csrfmiddlewaretoken: '{{ csrf_token }}',
                  },
                  type: $(this).attr('method'),
                  url: "{% url 'booking' %}",
                  success: function (response) {
                      alert("Вы успешно забронировали время");
                  },
                  error: function (response) {
                      alert(response.responseJSON.errors);
                      console.log(response.responseJSON.errors)
                  }
              });
              return false;
          });
      })