const url = "http://localhost:8000/citas/";

FormularioData.addEventListener('submit', (e) => {
    e.preventDefault();

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            id_paciente: Number(FormularioData.id_paciente.value),
            id_medico: Number(FormularioData.id_medico.value),
            fecha: FormularioData.fecha.value,
            hora: FormularioData.hora.value,
            estado: FormularioData.estado.value,
            motivo: FormularioData.motivo.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
            alert(data.mensaje || 'Cita registrada con éxito');
            FormularioData.reset();
        })
        .catch(error => console.log(error));
});
