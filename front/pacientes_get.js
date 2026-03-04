const url = "http://localhost:8000/pacientes/";

const contenedor = document.getElementById("data");

const CargaData = (datos) => {
    let resultado = "";
    for (let i = 0; i < datos.length; i++) {
        resultado +=
        `<li>
        <p>ID: ${datos[i].id_paciente}</p>
        <p>Nombre: ${datos[i].nombre} ${datos[i].apellido}</p>
        <p>Fecha Nacimiento: ${datos[i].fecha_nacimiento}</p>
        <p>Género: ${datos[i].genero}</p>
        <p>Teléfono: ${datos[i].telefono}</p>
        <p>Dirección: ${datos[i].direccion}</p>
        <p>Email: ${datos[i].email}</p>
        <p>Seguro Médico: ${datos[i].seguro_medico}</p>
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
