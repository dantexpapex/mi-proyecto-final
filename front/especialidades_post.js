const url = "http://localhost:8000/especialidades/";

FormularioData.addEventListener('submit', (e) => {
    e.preventDefault();

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nombre: FormularioData.nombre.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
            alert(data.mensaje || 'Especialidad registrada con éxito');
            FormularioData.reset();
        })
        .catch(error => console.log(error));
});
