const url = "http://localhost:8000/centros_salud/";

const contenedor = document.getElementById("data");

const CargaData = (datos) => {
    let resultado = "";
    for (let i = 0; i < datos.length; i++) {
        resultado +=
            `<li>
        <p>ID: ${datos[i].id_centro}</p>
        <p>Nombre: ${datos[i].nombre}</p>
        <p>Dirección: ${datos[i].direccion}</p>
        <p>Zona: ${datos[i].zona}</p>
        <p>Teléfono: ${datos[i].telefono}</p>
        <p>Latitud: ${datos[i].latitud}</p>
        <p>Longitud: ${datos[i].longitud}</p>
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
