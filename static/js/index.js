
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

            console.log(response);
            let data = response.data;

            if(data.bool){

                if(data.resultado.error ===  undefined) {
    
                    if(!(data.resultado.nombre == "" || data.resultado.nombre == undefined || data.resultado.nombre == null)){
                        
                        llenarDatos(data.resultado, dni);
                        
                        Swal.fire('Exitoso!', 'Resultado: ' + data.resultado.nombre, 'success');

                    } else {
                        Swal.fire('Advertencia!', castError("failed"), 'warning');
                    }
                    
                } else {
                    Swal.fire('Advertencia!', castError(data.resultado.error), 'warning');
                }
            
            } else {
                Swal.fire('Advertencia!', castError(data.resultado), 'warning');
            }
        },
        error: function(error){
            console.log(error);
        }
    })

}

function castError(value){
    
    switch (value) {
    
        case "Invalid dni":
            return "DNI Inválido";
    
        case "failed":
            return "Persona no encontrada";
    
        default:
            return value;
    
    }

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

    let nombres = document.getElementById('id_nombres_texto');
    let apellidoMaterno = document.getElementById('id_apellidoMaterno_texto');
    let apellidoPaterno = document.getElementById('id_apellidoPaterno_texto');

    if(nombres.value.trim() == "")
        nombres.style.border = '2px solid red';
    else
        nombres.style.border = '2px solid green';

    if(apellidoMaterno.value.trim() == "")
        apellidoMaterno.style.border = '2px solid red';
    else
        apellidoMaterno.style.border = '2px solid green';

    if(apellidoPaterno.value.trim() == "")
        apellidoPaterno.style.border = '2px solid red';
    else
        apellidoPaterno.style.border = '2px solid green';

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

function submitFormAndOpenNewTab() {
    var form = document.getElementById('myForm');
    form.submit();
    window.open('', '_blank');
}