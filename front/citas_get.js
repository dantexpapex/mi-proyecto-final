const url = "http://localhost:8000/citas/";

const contenedor = document.getElementById("data");

const CargaData = (datos) => {
    let resultado = "";
    for (let i = 0; i < datos.length; i++) {
        resultado +=
            `<li>
        <p>ID Cita: ${datos[i].id_cita}</p>
        <p>ID Paciente: ${datos[i].id_paciente}</p>
        <p>ID Médico: ${datos[i].id_medico}</p>
        <p>Fecha: ${datos[i].fecha}</p>
        <p>Hora: ${datos[i].hora}</p>
        <p>Estado: ${datos[i].estado}</p>
        <p>Motivo: ${datos[i].motivo}</p>
        </li>`;
    }
    contenedor.innerHTML = resultado;
}

fetch(url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
})
    .then(response => response.json())
    .then(data => {
        console.log(data);
        CargaData(data);
    })
    .catch(error => console.log(error.message));
