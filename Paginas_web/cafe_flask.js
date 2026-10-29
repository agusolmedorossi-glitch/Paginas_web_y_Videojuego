const productos = document.querySelectorAll(".producto");
const totalSpan = document.getElementById("total");
const btnConfirmar = document.getElementById("btnConfirmar");
const aviso = document.getElementById("aviso");
const confirmacion = document.getElementById("confirmacion");
const pedidoForm = document.getElementById("pedidoForm");
const btnAceptar = document.querySelector(".btn-aceptar");
const btnRechazar = document.querySelector(".btn-rechazar");

function generarCSV(datos) {
  const encabezado = "Cliente,Telefono,Dia de Retiro,Horario,Nota,Productos,Total (ARS),Fecha de Pedido";
  const productosStr = datos.productos.map(p => `${p.name} (x${p.quantity})`).join(' | ');
  const fila = [
    datos.nombre,
    datos.telefono,
    datos.dia,
    datos.horario,
    datos.nota || 'Sin nota',
    productosStr,
    '$' + datos.total.toLocaleString("es-AR"),
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
  enlace.download = `pedido_cafe_${datos.nombre.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.csv`;
  enlace.style.visibility = 'hidden';
  document.body.appendChild(enlace);
  enlace.click();
  document.body.removeChild(enlace);
  URL.revokeObjectURL(enlace.href);
}

function actualizarTotal() {
  let total = 0;
  let cantidadTotal = 0;

  productos.forEach(function (producto) {
    const precio = Number(producto.dataset.precio);
    const cantidad = Number(producto.querySelector(".numero").textContent);
    const subtotal = precio * cantidad;

    producto.querySelector(".subtotal").textContent = "$" + subtotal.toLocaleString("es-AR");
    total += subtotal;
    cantidadTotal += cantidad;
  });

  totalSpan.textContent = total.toLocaleString("es-AR");

  // Habilitar/deshabilitar botón según si hay productos
  btnConfirmar.disabled = cantidadTotal === 0;

  // Mostrar/ocultar aviso
  aviso.style.display = cantidadTotal === 0 ? "block" : "none";
}

productos.forEach(function (producto) {
  const numero = producto.querySelector(".numero");

  producto.querySelector(".mas").addEventListener("click", function () {
    numero.textContent = Number(numero.textContent) + 1;
    actualizarTotal();
  });

  producto.querySelector(".menos").addEventListener("click", function () {
    const actual = Number(numero.textContent);
    if (actual > 0) {
      numero.textContent = actual - 1;
      actualizarTotal();
    }
  });
});

pedidoForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const total = Number(totalSpan.textContent.replace(/\./g, "").replace(/,/g, ""));

  if (total === 0) {
    return;
  }

  const formData = new FormData(pedidoForm);

  const order = {
    customer: {
      name: formData.get("name"),
      phone: formData.get("phone"),
    },
    pickup: {
      day: formData.get("day"),
      time: formData.get("time"),
    },
    note: formData.get("note"),
    products: [],
    total: total,
  };

  // Recopilar productos seleccionados
  productos.forEach(function (producto) {
    const nombre = producto.querySelector("h3").textContent;
    const precio = Number(producto.dataset.precio);
    const cantidad = Number(producto.querySelector(".numero").textContent);

    if (cantidad > 0) {
      order.products.push({
        name: nombre,
        quantity: cantidad,
        unitPrice: precio,
      });
    }
  });

  const datosPedido = {
    nombre: order.customer.name,
    telefono: order.customer.phone,
    dia: order.pickup.day,
    horario: order.pickup.time,
    nota: order.note,
    productos: order.products,
    total: order.total
  };

  generarCSV(datosPedido);

  console.log("Pedido generado:", order);

  // Mostrar confirmación
  confirmacion.style.display = "block";

  // Ocultar confirmación después de 5 segundos
  setTimeout(function () {
    confirmacion.style.display = "none";
  }, 5000);
});

// Botones de términos y condiciones
btnAceptar.addEventListener("click", function () {
  alert("¡Gracias por aceptar nuestros términos y condiciones! Puedes continuar con tu pedido.");
});

btnRechazar.addEventListener("click", function () {
  alert("Debes aceptar los términos y condiciones para realizar un pedido.");
});

// Inicializar estado
actualizarTotal();

// ===== Mejoras visuales =====

// Animación de aparición al hacer scroll
const elementosRevelar = document.querySelectorAll(
  "section, .menu, .destacados li, footer li"
);

if ("IntersectionObserver" in window) {
  const observador = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (entrada) {
      if (entrada.isIntersecting) {
        entrada.target.classList.add("visible");
        observador.unobserve(entrada.target);
      }
    });
  }, { threshold: 0.12 });

  elementosRevelar.forEach(function (elemento) {
    elemento.classList.add("revelar");
    observador.observe(elemento);
  });
}

// Resaltar el link del menú según la sección visible
const linksNav = document.querySelectorAll(".nav-links a");

function marcarLinkActivo() {
  let actual = "";
  document.querySelectorAll("section[id]").forEach(function (seccion) {
    if (window.scrollY >= seccion.offsetTop - 140) {
      actual = seccion.id;
    }
  });

  linksNav.forEach(function (link) {
    const activo = link.getAttribute("href") === "#" + actual;
    link.classList.toggle("activo", activo);
    if (activo) {
      link.setAttribute("aria-current", "true");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

window.addEventListener("scroll", marcarLinkActivo, { passive: true });
marcarLinkActivo();
