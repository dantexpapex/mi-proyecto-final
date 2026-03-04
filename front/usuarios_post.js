const url = "http://localhost:8000/usuarios/";

FormularioData.addEventListener('submit', (e) => {
    e.preventDefault();

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: FormularioData.username.value,
            password_hash: FormularioData.password_hash.value,
            rol: FormularioData.rol.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Éxito:', data);
            alert(data.mensaje || 'Usuario registrado con éxito');
            FormularioData.reset();
        })
        .catch(error => console.log(error));
});
