const url = "http://localhost:8000/centros_salud/";

FormularioData.addEventListener('submit', (e) => {
    e.preventDefault();

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: FormularioData.nombre.value,
            direccion: FormularioData.direccion.value,
            zona: FormularioData.zona.value,
            telefono: FormularioData.telefono.value,
            latitud: Number(FormularioData.latitud.value) || 0,
            longitud: Number(FormularioData.longitud.value) || 0
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
            alert(data.mensaje || 'Centro de salud registrado con éxito');
            FormularioData.reset();
        })
        .catch(error => console.log(error));
});
