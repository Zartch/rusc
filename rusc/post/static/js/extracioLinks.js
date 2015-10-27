/**
 * Created by Zartch on 23/10/2015.
 */

$( document ).ready(function() {

    /* Script per convertir el multifield en select2*/
    $(".etiquetes").select2({tags: true});
    $('.select2-search__field').on("keydown", function(e) {
        $(".etiquetes").select2({data:[{id:0,text:"enhancement"}]});
    });

    //*****Extració de links*****///
    $(".id_text").keyup(function(e) {
        //Define variables
        var links = new Array;
        var text = $('#id_text').val();
        var regexp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
        var url;
        e.preventDefault();

        //Cicle que llegeix el text i affegeix un link al llistat en el cas de que la variable contingi un match amb el pattern del regxp
        //es llegeix el text sencer cada vegada que es pulsa una tecla
        while (matches = regexp.exec(text)) {
            url = matches[0];
            links.push(url);
        }

        //Creem gim una taula on posarem textbox per la url y la descripció del recurs
        //buidem els resultats anteriors, es mes facil que mirar els que existexen
        $("#div_recursos").empty();
        //agafem el element on voldrem colocarli els nous objectes
        var div_recursos = document.getElementById("div_recursos");
        //Creem la taula on posarem els recursos
        taula = document.createElement('table');

        //en el cas de que links contingui mes de un link
        if (links.length > 0) {
            //Per cada element de la llista de matcher hem de fer alguna cosa
            //comprobar que els links no existeixen ja, es mols més costos que eliminar i tornar a començar
            $("#links_results").empty();
            for (i = 0; i < links.length; i++) {
                ////*****  EXEMPLE BASIC, afegir un link a un div  ******////
                //Agafem el div de links i li afegim un link
                //var links_results = document.getElementById("links_results");
                //a = document.createElement('a');
                //a.href = '#'; // Insted of calling setAttribute
                //a.innerHTML = "Link:" + links[i] // <a>INNER_TEXT</a>
                //links_results.appendChild(a); // Append the link to the div..
                ////Per a introduir la url del link al formset(ja creat)
                //$("#id_form-0-url").val(url);
                ////*****  FINAL EXEMPLE BASIC  ******/////

                //Guardarém el formset per tal de que el usari pugui introduir els recursos no linkats al text
                //per tal de que la eliminació no afecti als recursos introduits manualment per el usuari
                //Definim el nou textbox de url
                textboxUrl = document.createElement('input');
                textboxUrl.className="form-control ";
                textboxUrl.name="form_recurs_"+i;
                textboxUrl.placeholder="URL";
                textboxUrl.type="text";
                textboxUrl.value = links[i];
                //Definim el nou textbox de descripció
                textboxDesc = document.createElement('input');
                textboxDesc.className="form-control ";
                textboxDesc.name="form_recurs_name_"+i;
                textboxDesc.id="form_recurs_name_"+i;
                textboxDesc.placeholder="Nom Recurs";
                textboxDesc.type="text";

                //Fem una petció en ajax per que no interrompi el curs de la execució esperant una resposta
                //La petició cridará a una vista de django que retornará el nom preposat per el recurs
                $.ajax({
                  type: "POST",
                  url: '/linkMeta/',
                  data: {'Link': links[i]},
                  indexValue : i,
                  //async:false,
                    success: function(data) {
                        //Actualitzém el nom del recurs.
                        //alert("#form_recurs_name_"+this.indexValue);
                        $("#form_recurs_name_"+this.indexValue).val(data);

                      },
                    error:function(data) {
                      $('#'+this.indexValue).value = data;
                      //alert("ERROR,"+this.indexValue+" ningun titulo encontrado. Assigne uno manualmente "+ data);
                      $("#form_recurs_name_"+this.indexValue).val(data);
                    }
                });

                //creem els elements que intrduirem a la taula i els afegim
                var tr = document.createElement('tr');
                tr.appendChild( document.createElement('td') );
                tr.appendChild( document.createElement('td') );
                tr.cells[0].appendChild(textboxDesc);
                tr.cells[1].appendChild(textboxUrl);
                //afegim els tr a la taula
                taula.appendChild(tr);

            }
            //afegim la taula en el div corresponent
            div_recursos.appendChild(taula);
        }
    });
});