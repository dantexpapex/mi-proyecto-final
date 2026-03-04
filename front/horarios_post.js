const url = "http://localhost:8000/horarios/";

FormularioData.addEventListener('submit', (e) => {
    e.preventDefault();

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            id_medico: Number(FormularioData.id_medico.value),
            dia_semana: FormularioData.dia_semana.value,
            hora_inicio: FormularioData.hora_inicio.value,
            hora_fin: FormularioData.hora_fin.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
            alert(data.mensaje || 'Horario registrado con éxito');
            FormularioData.reset();
        })
        .catch(error => console.log(error));
});
