$(document).ready(function () {
    // Función para actualizar el padding del elemento con class "principal"
    function updatePrincipalPadding() {
        if (window.innerWidth < 768) {
            $(".principal").css("padding-top", "105px");
            $(".principal").css("padding-left", "0");
        } else {
            $(".principal").css("padding-top", "82px");
            if ($(".sidebar").hasClass("hoverable")) {
                $(".principal").css("padding-left", "80px");
            } else {
                $(".principal").css("padding-left", "260px");
            }
        }
    }

    // Llamar a la función al cargar la página
    updatePrincipalPadding();

    // Manejar el evento hover en el sidebar comprimido
    $(".sidebar").on('mouseenter', function () {
        // Cuando el mouse sale, restaura el tamaño original del principal
        if (window.innerWidth >= 768) {
            $(".principal").css("padding-left", "260px");
        }
    });
    $(".sidebar").on('mouseleave', function () {
        // Cuando el mouse sale, restaura el tamaño original del principal
        updatePrincipalPadding();
    });

    // Manejar clic en el botón para expandir el sidebar
    $(".bottom").on('click', function () {
        if (window.innerWidth >= 768) {
            updatePrincipalPadding();
        }
    });

    // Manejar cambios en el tamaño de la ventana
    $(window).on('resize', function () {
        // Reevaluar el padding al cambiar el tamaño de la ventana
        updatePrincipalPadding();
    });

});

