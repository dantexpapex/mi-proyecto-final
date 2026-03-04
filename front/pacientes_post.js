const url = "http://localhost:8000/pacientes/";

FormularioData.addEventListener('submit', (e) => {
    e.preventDefault();

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: FormularioData.nombre.value,
            apellido: FormularioData.apellido.value,
            fecha_nacimiento: FormularioData.fecha_nacimiento.value,
            genero: FormularioData.genero.value,
            telefono: FormularioData.telefono.value,
            direccion: FormularioData.direccion.value,
            email: FormularioData.email.value,
            seguro_medico: FormularioData.seguro_medico.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
            alert(data.mensaje || 'Paciente registrado con éxito');
            FormularioData.reset();
        })
        .catch(error => console.log(error));
});
