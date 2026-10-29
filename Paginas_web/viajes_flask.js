document.addEventListener('DOMContentLoaded', function() {
    const tarjetas = document.querySelectorAll('.destino-card, .promocion-card, .reserva-card, .contacto-form');
    const sinMovimiento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if ('IntersectionObserver' in window && !sinMovimiento) {
        const observador = new IntersectionObserver(function(entradas) {
            entradas.forEach(function(entrada) {
                if (entrada.isIntersecting) {
                    entrada.target.classList.add('visible');
                    observador.unobserve(entrada.target);
                }
            });
        }, { threshold: 0.15 });

        tarjetas.forEach(function(tarjeta) {
            tarjeta.classList.add('aparecer');
            observador.observe(tarjeta);
        });
    }

    const contactoForm = document.getElementById('contactoForm');

    contactoForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const nombre = contactoForm.querySelector('input[name="nombre"]').value;
        const email = contactoForm.querySelector('input[name="email"]').value;
        const mensaje = contactoForm.querySelector('textarea[name="mensaje"]').value;

        alert(`¡Mensaje enviado con éxito!\n\nGracias por contactarnos, ${nombre}.\nHemos recibido tu mensaje:\n\n${mensaje}\n\nTe responderemos pronto al email: ${email}`);

        contactoForm.reset();
    });

    const reservaForm = document.getElementById('reservaForm');
    const cantidadPasajes = reservaForm.querySelector('.numero');
    const botonMenos = reservaForm.querySelector('.menos');
    const botonMas = reservaForm.querySelector('.mas');
    const totalElement = document.getElementById('total');
    const precioPorPasaje = 1500;
    let cantidad = 1;

    botonMas.addEventListener('click', function() {
        cantidad++;
        cantidadPasajes.textContent = cantidad;
        actualizarTotal();
    });

    botonMenos.addEventListener('click', function() {
        if (cantidad > 1) {
            cantidad--;
            cantidadPasajes.textContent = cantidad;
            actualizarTotal();
        }
    });

    function actualizarTotal() {
        const total = cantidad * precioPorPasaje;
        totalElement.textContent = total;
        totalElement.classList.remove('cambio');
        void totalElement.offsetWidth;
        totalElement.classList.add('cambio');
    }

    function generarCSV(datos) {
        const encabezado = "Destino,Cantidad de Pasajes,Fecha,Horario,Nombre,Email,Telefono,Total (USD),Fecha de Reserva";
        const fila = [
            datos.destino.charAt(0).toUpperCase() + datos.destino.slice(1),
            datos.cantidad,
            datos.fecha,
            datos.hora + 'hs',
            datos.nombre,
            datos.email,
            datos.telefono,
            '$' + datos.total,
            new Date().toLocaleString()
        ].map(dato => {
            return '"' + String(dato).replace(/"/g, '""') + '"';
        }).join(",");
        const contenido = encabezado + "\r\n" + fila + "\r\n";

        const archivo = new Blob(
            ["\uFEFF" + contenido],
            { type: "text/csv;charset=utf-8;" }
        );

        const enlace = document.createElement("a");
        enlace.href = URL.createObjectURL(archivo);
        enlace.download = `reserva_${datos.nombre.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
        enlace.click();
        URL.revokeObjectURL(enlace.href);
    }

    reservaForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const destino = reservaForm.querySelector('select[name="destino"]').value;
        const fecha = reservaForm.querySelector('input[name="fecha"]').value;
        const hora = reservaForm.querySelector('select[name="hora"]').value;
        const nombre = reservaForm.querySelector('input[name="nombre"]').value;
        const email = reservaForm.querySelector('input[name="email"]').value;
        const telefono = reservaForm.querySelector('input[name="telefono"]').value;
        const total = cantidad * precioPorPasaje;

        const datosReserva = {
            destino: destino,
            cantidad: cantidad,
            fecha: fecha,
            hora: hora,
            nombre: nombre,
            email: email,
            telefono: telefono,
            total: total
        };

        generarCSV(datosReserva);

        alert(`¡Reserva realizada con éxito!\n\nDetalles de la reserva:\n\nDestino: ${destino.charAt(0).toUpperCase() + destino.slice(1)}\nCantidad de pasajes: ${cantidad}\nFecha: ${fecha}\nHorario: ${hora}hs\nCliente: ${nombre}\nEmail: ${email}\nTeléfono: ${telefono}\nTotal: $${total} USD\n\nSe ha descargado un archivo CSV con los datos de tu reserva.`);

        reservaForm.reset();
        cantidad = 1;
        cantidadPasajes.textContent = '1';
        actualizarTotal();
    });

    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId.startsWith('#')) {
                e.preventDefault();
                const targetSection = document.querySelector(targetId);
                if (targetSection) {
                    targetSection.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});
