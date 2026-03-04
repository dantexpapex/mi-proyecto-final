const url = "http://localhost:8000/medicos/";

FormularioData.addEventListener('submit', (e) => {
    e.preventDefault();

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: FormularioData.nombre.value,
            apellido: FormularioData.apellido.value,
            numero_colegiatura: FormularioData.numero_colegiatura.value,
            id_especialidad: Number(FormularioData.id_especialidad.value),
            id_centro: Number(FormularioData.id_centro.value)
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
            alert(data.mensaje || 'Médico registrado con éxito');
            FormularioData.reset();
        })
        .catch(error => console.log(error));
});
