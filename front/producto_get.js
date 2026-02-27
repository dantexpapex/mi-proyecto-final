const url = "http://localhost:8000/producto/";

const contenedor = document.getElementById("data");

const CargaData = (datos) => {
    for (let i = 0; i < data.length; i++) {
        resultado+= 
        `<li>
        <p>Id: ${datos[i].id_producto}</p>
        <p>Tipo: ${datos[i].id_tipo}</p>
        <p>Descripcion: ${datos[i].descripcion}</p>
        <p>Precio Compra: ${datos[i].precio_compra}</p>
        <p>Precio Venta: ${datos[i].precio_venta}</p>
        <p>Cantidad: ${datos[i].cantidad}</p>
        <p>Activo: ${datos[i].activo}</p>
        </li>`;
    contenedor.innerHTML = resultado;
}
}
fetch(url,
    {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => { console.log(data);
                    console.log(response.status);
    })
    .catch(error => console.log('Error.message'));