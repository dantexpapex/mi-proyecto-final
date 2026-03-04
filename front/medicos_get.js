const url = "http://localhost:8000/medicos/";

const contenedor = document.getElementById("data");

const CargaData = (datos) => {
    let resultado = "";
    for (let i = 0; i < datos.length; i++) {
        resultado +=
            `<li>
        <p>ID: ${datos[i].id_medico}</p>
        <p>Nombre: ${datos[i].nombre} ${datos[i].apellido}</p>
        <p>N° Colegiatura: ${datos[i].numero_colegiatura}</p>
        <p>ID Especialidad: ${datos[i].id_especialidad}</p>
        <p>ID Centro: ${datos[i].id_centro}</p>
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
