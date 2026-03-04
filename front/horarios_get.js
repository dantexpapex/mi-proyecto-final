const url = "http://localhost:8000/horarios/";

const contenedor = document.getElementById("data");

const CargaData = (datos) => {
    let resultado = "";
    for (let i = 0; i < datos.length; i++) {
        resultado +=
            `<li>
        <p>ID Horario: ${datos[i].id_horario}</p>
        <p>ID Médico: ${datos[i].id_medico}</p>
        <p>Día de la Semana: ${datos[i].dia_semana}</p>
        <p>Hora Inicio: ${datos[i].hora_inicio}</p>
        <p>Hora Fin: ${datos[i].hora_fin}</p>
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
