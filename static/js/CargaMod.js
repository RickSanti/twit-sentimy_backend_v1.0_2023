$(document).ready(function () {
    $("#buscar_carga").submit(function (event) {
        // Prevent the default form submission
        // event.preventDefault();
        var myButton = document.getElementById('nuevo_boton');
        //myButton.textContent = 'Texto Modificado';
        myButton.style.display = 'inline-grid';

        /*setTimeout(function () {
            myButton.style.display = 'none';
        }, 8000); // 4000 milisegundos = 4 segundos*/

        // Usar Promesa y async/await para simular operación asíncrona
        /*async function esperar() {
            return new Promise(resolve => setTimeout(resolve, 4000)); // 4000 milisegundos = 4 segundos
        }

        // Ocultar el elemento después de esperar 4 segundos
        esperar().then(() => {
            myButton.style.display = 'none';
        });*/

        //display: inline-grid;

        // Show loading screen on form submission
        //$("#loading-screen").show();

        // Get the form data and submit the form using AJAX
        /* var formData = $(this).serialize();
        $.ajax({
            type: "POST",
            url: "/submit_form",  // Update with your actual Flask route
            data: formData,
            success: function (response) {
                // Hide the loading screen on successful form submission
                $("#loading-screen").hide();
                // Process the response if needed
            },
            error: function (error) {
                // Handle the error if the form submission fails
                console.error("Form submission error:", error);
            }
        });*/
    });
});