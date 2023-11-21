
function buscar_por_dni(dni){
    
    let data = new FormData();
    data.append('dni', dni);

    $.ajax({
        type: "POST",
        url: "/analisis/buscar_por_dni/",
        data: data,
        processData:false,
        contentType : false,
        dataType: "json",
        headers : {
            "X-CSRFToken": getCookie("csrftoken")
        },
        ContentType: "application/json",
        success: function(response){

            let data = response.data;

            if(data.bool){

                // if(data.resultado.message ===  undefined){
                //     Swal.fire('Servicio!', data.resultado.error, 'warning');
                // }
                console.log(data.resultado)
                if(data.resultado.error ===  undefined) {
                    
                    llenarDatos(data.resultado, dni);
                    
                    Swal.fire('Persona Encontrada!', 'Resultado: ' + data.resultado.nombre, 'success');
                    
                } else {
                    Swal.fire('Persona no encontrada!', data.resultado.error, 'warning');
                }
            
            } else {
                Swal.fire('Persona no encontrada!', data.resultado, 'warning');
            }
        },
        error: function(error){
            console.log(error);
        }
    })

}

function llenarDatos(resultado, dni){

    document.getElementById("id_dni").value = dni;
    document.getElementById('id_dni_texto').disabled = true;

    document.getElementById("id_nombres").value = resultado.nombres; 
    document.getElementById("id_nombres_texto").value = resultado.nombres; 
    document.getElementById('id_nombres_texto').disabled = true;

    document.getElementById("id_apellidoMaterno").value = resultado.apellidoMaterno; 
    document.getElementById("id_apellidoMaterno_texto").value = resultado.apellidoMaterno; 
    document.getElementById('id_apellidoMaterno_texto').disabled = true;

    document.getElementById("id_apellidoPaterno").value = resultado.apellidoPaterno; 
    document.getElementById("id_apellidoPaterno_texto").value = resultado.apellidoPaterno; 
    document.getElementById('id_apellidoPaterno_texto').disabled = true;

}

function getCookie(c_name){
    if (document.cookie.length > 0){
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1){
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

window.addEventListener("keydown", (event) => {
    if (event.keyCode === 13) {
        let dni = document.getElementById("id_dni_texto").value; 
        buscar_por_dni(dni);
    }
})