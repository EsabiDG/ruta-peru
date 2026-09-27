document.addEventListener('DOMContentLoaded', function () {

    const navbar = document.getElementById('navbar');
    if (navbar && !navbar.classList.contains('navbar-solid')) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 60) navbar.classList.add('scrolled');
            else navbar.classList.remove('scrolled');
        });
    }

    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => navLinks.classList.toggle('abierto'));
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => navLinks.classList.remove('abierto'));
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId.length < 2) return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const pos = target.getBoundingClientRect().top + window.scrollY - 80;
                window.scrollTo({ top: pos, behavior: 'smooth' });
            }
        });
    });

    const cuestionario = document.getElementById('cuestionario');
    if (!cuestionario) return;

    const pasos = cuestionario.querySelectorAll('.paso');
    const totalPasos = pasos.length;
    const btnAtras = document.getElementById('btnAtras');
    const btnContinuar = document.getElementById('btnContinuar');
    const btnFinalizar = document.getElementById('btnFinalizar');
    const progresoTexto = document.getElementById('progresoTexto');
    const progresoPorcentaje = document.getElementById('progresoPorcentaje');
    const progresoRelleno = document.getElementById('progresoRelleno');
    const overlay = document.getElementById('overlayAnalisis');

    let pasoActual = 0;

    cuestionario.querySelectorAll('.opcion').forEach(opcion => {
        const input = opcion.querySelector('input[type="checkbox"]');
        if (!input) return;

        if (input.checked) opcion.classList.add('seleccionada');

        input.addEventListener('change', () => {
            if (input.checked) opcion.classList.add('seleccionada');
            else opcion.classList.remove('seleccionada');
        });
    });

    function mostrarPaso(indice) {
        pasos.forEach((p, i) => p.style.display = (i === indice) ? 'block' : 'none');

        const porcentaje = Math.round(((indice + 1) / totalPasos) * 100);
        progresoTexto.textContent = `Pregunta ${indice + 1} de ${totalPasos}`;
        progresoPorcentaje.textContent = `${porcentaje}%`;
        progresoRelleno.style.width = `${porcentaje}%`;

        btnAtras.style.visibility = (indice === 0) ? 'hidden' : 'visible';

        if (indice === totalPasos - 1) {
            btnContinuar.style.display = 'none';
            btnFinalizar.style.display = 'inline-block';
        } else {
            btnContinuar.style.display = 'inline-block';
            btnFinalizar.style.display = 'none';
        }
    }

    function haySeleccionEnPaso(indice) {
        if (indice === totalPasos - 1) return true;
        return pasos[indice].querySelectorAll('input[type="checkbox"]:checked').length > 0;
    }

    btnContinuar.addEventListener('click', () => {
        if (!haySeleccionEnPaso(pasoActual)) {
            alert('Selecciona al menos una opción para continuar.');
            return;
        }
        if (pasoActual < totalPasos - 1) {
            pasoActual++;
            mostrarPaso(pasoActual);
        }
    });

    btnAtras.addEventListener('click', () => {
        if (pasoActual > 0) {
            pasoActual--;
            mostrarPaso(pasoActual);
        }
    });

    btnFinalizar.addEventListener('click', (e) => {
        const totalReales = cuestionario.querySelectorAll('input[type="checkbox"]:checked:not([value="ninguno"])').length;

        if (totalReales === 0) {
            e.preventDefault();
            alert('Debes seleccionar al menos un interés.');
            return;
        }

        if (overlay) overlay.classList.add('activo');
    });

    mostrarPaso(0);
});