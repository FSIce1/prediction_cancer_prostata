
function validationAnalisis(event){
    

    let titulo = document.getElementById('id_titulo');
    let descripcion = document.getElementById('id_descripcion');
    let imagen = document.getElementById('imagen');
    let dni = document.getElementById('id_dni_texto');
    let nombres = document.getElementById('id_nombres_texto');
    let apellidoMaterno = document.getElementById('id_apellidoMaterno_texto');
    let apellidoPaterno = document.getElementById('id_apellidoPaterno_texto');

    if(titulo.value.trim() == ""){
        titulo.style.border = '2px solid red';
        event.preventDefault();
    } else {
        titulo.style.border = '2px solid green';
    }

    if(descripcion.value.trim() == ""){
        descripcion.style.border = '2px solid red';
        event.preventDefault();
    } else {
        descripcion.style.border = '2px solid green';
    }

    if(imagen.value.trim() == ""){
        imagen.style.border = '2px solid red';
        event.preventDefault();
    } else {
        imagen.style.border = '2px solid green';
    }

    if(dni.value.trim() == ""){
        dni.style.border = '2px solid red';
        event.preventDefault();
    } else {
        dni.style.border = '2px solid green';
    }

    if(nombres.value.trim() == ""){
        nombres.style.border = '2px solid red';
        event.preventDefault();
    } else {
        nombres.style.border = '2px solid green';
    }

    if(apellidoMaterno.value.trim() == ""){
        apellidoMaterno.style.border = '2px solid red';
        event.preventDefault();
    } else {
        apellidoMaterno.style.border = '2px solid green';
    }

    if(apellidoPaterno.value.trim() == ""){
        apellidoPaterno.style.border = '2px solid red';
        event.preventDefault();
    } else {
        apellidoPaterno.style.border = '2px solid green';
    }

}