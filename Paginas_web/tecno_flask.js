document.addEventListener('DOMContentLoaded', function() {
    const productos = document.querySelectorAll('.producto-item');
    const totalElement = document.getElementById('total');
    const btnConfirmar = document.getElementById('btnConfirmar');
    const aviso = document.getElementById('aviso');
    const confirmacion = document.getElementById('confirmacion');
    const ordenarSelect = document.getElementById('ordenar');
    let total = 0;

    // Funcionalidad de cantidades
    productos.forEach(producto => {
        const precio = parseInt(producto.getAttribute('data-precio'));
        const botonMenos = producto.querySelector('.btn-menos');
        const botonMas = producto.querySelector('.btn-mas');
        const numero = producto.querySelector('.cant-numero');
        const subtotal = producto.querySelector('.prod-subtotal');
        let cantidad = 0;

        botonMas.addEventListener('click', function() {
            cantidad++;
            numero.textContent = cantidad;
            const subtotalValor = cantidad * precio;
            subtotal.textContent = '$' + subtotalValor.toLocaleString();
            actualizarTotal();
        });

        botonMenos.addEventListener('click', function() {
            if (cantidad > 0) {
                cantidad--;
                numero.textContent = cantidad;
                const subtotalValor = cantidad * precio;
                subtotal.textContent = '$' + subtotalValor.toLocaleString();
                actualizarTotal();
            }
        });

        // Permite reiniciar la cantidad interna al resetear la compra
        producto.addEventListener('reiniciar', function() {
            cantidad = 0;
        });

        function actualizarTotal() {
            total = 0;
            productos.forEach(prod => {
                const prodPrecio = parseInt(prod.getAttribute('data-precio'));
                const prodCantidad = parseInt(prod.querySelector('.cant-numero').textContent);
                total += prodPrecio * prodCantidad;
            });
            totalElement.textContent = total.toLocaleString();

            if (total > 0) {
                btnConfirmar.disabled = false;
                aviso.style.display = 'none';
            } else {
                btnConfirmar.disabled = true;
                aviso.style.display = 'block';
            }
        }
    });

    // Funcionalidad de ordenar productos
    ordenarSelect.addEventListener('change', function() {
        const valor = this.value;
        const productosArray = Array.from(productos);
        const container = document.querySelector('.productos-lista');

        productosArray.sort((a, b) => {
            switch(valor) {
                case 'precio-asc':
                    return parseInt(a.getAttribute('data-precio')) - parseInt(b.getAttribute('data-precio'));
                case 'precio-desc':
                    return parseInt(b.getAttribute('data-precio')) - parseInt(a.getAttribute('data-precio'));
                case 'nombre':
                    const nombreA = a.querySelector('.prod-info h3').textContent.toLowerCase();
                    const nombreB = b.querySelector('.prod-info h3').textContent.toLowerCase();
                    return nombreA.localeCompare(nombreB);
                default:
                    return 0;
            }
        });

        productosArray.forEach(prod => container.appendChild(prod));
    });

    function generarCSV(datos) {
        const encabezado = "Cliente,Email,Telefono,Direccion,Productos,Total (ARS),Fecha de Compra";
        const productosStr = datos.productos.map(p => `${p.nombre} (x${p.cantidad})`).join(' | ');
        const fila = [
            datos.nombre,
            datos.email,
            datos.telefono,
            datos.direccion,
            productosStr,
            '$' + datos.total.toLocaleString(),
            new Date().toLocaleString()
        ].map(dato => {
            return '"' + dato.replace(/"/g, '""') + '"';
        }).join(",");
        const contenido = encabezado + "\r\n" + fila + "\r\n";

        const archivo = new Blob(
            ["\uFEFF" + contenido],
            { type: "text/csv;charset=utf-8;" }
        );

        const enlace = document.createElement("a");
        enlace.href = URL.createObjectURL(archivo);
        enlace.download = `compra_tecno_${datos.nombre.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
        enlace.click();
        URL.revokeObjectURL(enlace.href);
    }

    // Confirmar compra
    btnConfirmar.addEventListener('click', function() {
        const campos = document.querySelectorAll('.datos-cliente input');
        const nombre = document.querySelector('input[name="name"]').value;
        const email = document.querySelector('input[name="email"]').value;
        const telefono = document.querySelector('input[name="phone"]').value;
        const direccion = document.querySelector('input[name="direccion"]').value;

        campos.forEach(campo => {
            campo.classList.toggle('invalido', !campo.value.trim());
        });

        if (!nombre || !email || !telefono || !direccion) {
            alert('Por favor, completa todos tus datos.');
            return;
        }

        // Recopilar productos seleccionados
        const productosComprados = [];
        productos.forEach(prod => {
            const nombreProd = prod.querySelector('.prod-info h3').textContent;
            const precio = parseInt(prod.getAttribute('data-precio'));
            const cantidad = parseInt(prod.querySelector('.cant-numero').textContent);

            if (cantidad > 0) {
                productosComprados.push({
                    nombre: nombreProd,
                    cantidad: cantidad,
                    precio: precio
                });
            }
        });

        const datosCompra = {
            nombre: nombre,
            email: email,
            telefono: telefono,
            direccion: direccion,
            productos: productosComprados,
            total: total
        };

        generarCSV(datosCompra);

        confirmacion.style.display = 'block';
        btnConfirmar.disabled = true;

        // Resetear formulario después de 3 segundos
        setTimeout(() => {
            productos.forEach(prod => {
                prod.querySelector('.cant-numero').textContent = '0';
                prod.querySelector('.prod-subtotal').textContent = '$0';
                prod.dispatchEvent(new Event('reiniciar'));
            });
            total = 0;
            totalElement.textContent = '0';
            document.querySelectorAll('input').forEach(input => input.value = '');
            btnConfirmar.disabled = true;
            aviso.style.display = 'block';
            confirmacion.style.display = 'none';
        }, 3000);
    });

    // Smooth scroll en navegación (menú de escritorio y móvil)
    const navLinks = document.querySelectorAll('nav a, .menu-movil a');

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
                cerrarMenu();
            }
        });
    });

    // Tema claro / oscuro
    const raiz = document.documentElement;
    const btnTema = document.getElementById('btnTema');

    function actualizarEtiquetaTema() {
        const esOscuro = raiz.classList.contains('dark');
        btnTema.setAttribute('aria-label', esOscuro ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
    }

    actualizarEtiquetaTema();
    btnTema.addEventListener('click', function() {
        const esOscuro = raiz.classList.toggle('dark');
        localStorage.setItem('tema', esOscuro ? 'oscuro' : 'claro');
        actualizarEtiquetaTema();
    });

    // Encabezado: fondo al hacer scroll
    const encabezado = document.getElementById('encabezado');

    function alHacerScroll() {
        encabezado.classList.toggle('con-scroll', window.scrollY > 12);
    }

    alHacerScroll();
    window.addEventListener('scroll', alHacerScroll, { passive: true });

    // Menú móvil
    const btnMenu = document.getElementById('btnMenu');
    const menuMovil = document.getElementById('menuMovil');

    function abrirCerrarMenu(abrir) {
        encabezado.classList.toggle('menu-abierto', abrir);
        btnMenu.setAttribute('aria-expanded', String(abrir));
        btnMenu.setAttribute('aria-label', abrir ? 'Cerrar menú' : 'Abrir menú');
        menuMovil.inert = !abrir;
    }

    function cerrarMenu() {
        abrirCerrarMenu(false);
    }

    btnMenu.addEventListener('click', function() {
        abrirCerrarMenu(!encabezado.classList.contains('menu-abierto'));
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') cerrarMenu();
    });

    window.matchMedia('(min-width: 768px)').addEventListener('change', function(e) {
        if (e.matches) cerrarMenu();
    });

    // Enlace activo según la sección visible
    const enlacesNav = document.querySelectorAll('nav a');

    if ('IntersectionObserver' in window) {
        const observadorSecciones = new IntersectionObserver(function(entradas) {
            entradas.forEach(entrada => {
                if (!entrada.isIntersecting) return;
                enlacesNav.forEach(enlace => {
                    enlace.classList.toggle('activo', enlace.getAttribute('href') === '#' + entrada.target.id);
                });
            });
        }, { rootMargin: '-45% 0px -50% 0px' });

        enlacesNav.forEach(enlace => {
            const seccion = document.querySelector(enlace.getAttribute('href'));
            if (seccion) observadorSecciones.observe(seccion);
        });
    }

    // Animación de aparición
    const elementosAparecer = document.querySelectorAll('.encabezado-seccion, .producto-card, .oferta-card, .compra-container, .contacto-info');

    elementosAparecer.forEach((el, i) => {
        el.classList.add('aparecer');
        el.style.transitionDelay = (i % 2) * 80 + 'ms';
    });

    if ('IntersectionObserver' in window) {
        const observadorAparecer = new IntersectionObserver(function(entradas, obs) {
            entradas.forEach(entrada => {
                if (entrada.isIntersecting) {
                    entrada.target.classList.add('visible');
                    obs.unobserve(entrada.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        elementosAparecer.forEach(el => observadorAparecer.observe(el));
    } else {
        elementosAparecer.forEach(el => el.classList.add('visible'));
    }

    // Año del pie
    document.getElementById('anio').textContent = new Date().getFullYear();
});
