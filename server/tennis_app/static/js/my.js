function show_form() {
const formContainer = document.querySelector('.table_form')
  formContainer.classList.add('show-form');
}


function remove_form() {
const formContainer = document.querySelector('.table_form')
  formContainer.classList.remove('show-form');
}


function get_free_tables(){
       var date = document.getElementById('id_date').value;
       var duration = document.getElementById('id_duration').value;
       var time = document.getElementById('id_time').value;
       var selectElement = document.getElementById("id_tableID");
       while (selectElement.options.length > 0) {
                selectElement.remove(0);
       }
       
       const url = "/api/order_list_view?date="+date+"&time="+time+":00&duration="+duration;

       $.get(url, function(data, status){
       if(data['free_tablies'].length){
       var newOption = document.createElement("option");
            newOption.value = -1;
            newOption.text = "------";
            selectElement.add(newOption);
       data['free_tablies'].forEach(function(item, index, array){
            var newOption = document.createElement("option");
            newOption.value = item['id'];
            newOption.text = "Стол №"+item['id']+" ("+item['price']+"рублей)";
            selectElement.add(newOption);
            //console.log(item['id'], item['price']);
       });
}
       });

}

function get_price() {

       var duration = document.getElementById('id_duration').value;
      var table = document.getElementById("id_tableID").options.selectedIndex;
       var trener = document.getElementById("id_trenerID").value;

       var sel = document.getElementById("id_tableID");
      // var val = sel.options[sel.selectedIndex].value;
    //    alert(val);

       console.log(duration, table, trener);
       const url = "/api/get_price?duration="+duration+"&table="+table+"&trener="+trener;

       $.get(url, function(data, status){

            console.log(data['price']);
            var price = document.getElementById("IDprice")
            price.innerHTML =  data['price'];
       });
}


function get_seans(){
       var date = document.getElementById('date').value;
       var table = document.getElementById('table').value;
       var mytable = document.getElementById('myTable');
       if(date===""){
                div = document.getElementById("message");
                div.innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                              <strong>Ошибка!</strong> Выберите дату.
                              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                              </button>
                            </div>`;
       }
       else if(table===""){
                div = document.getElementById("message");
                div.innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                              <strong>Ошибка!</strong> Выберите стол.
                              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                              </button>
                            </div>`;
       }
       else{


       const url = "/api/get_orders/?date="+date+"&tableID="+table;
       console.log(url);
       var rowCount = mytable.rows.length;

        for (var i = rowCount - 1; i > 0; i--) {
            mytable.deleteRow(i); // Удаляем строку с текущим индексом
        }
       $.get(url, function(data, status){
       if(data.length){
       data.forEach(function(item, index, array){
       console.log(item)
            var row = mytable.insertRow(-1);
            var cell1 = row.insertCell(0); // Вставляем новую ячейку в эту строку
            var cell2 = row.insertCell(1);
            cell1.innerHTML = item['time']; // Задаем содержимое ячейки
            cell2.innerHTML = item['endtime']
       });
}
else{
div = document.getElementById("message");
                div.innerHTML = `<div class="alert alert-primary alert-dismissible fade show" role="alert">
                              <strong>Внимание!</strong> Стол абсолютно свободен.
                              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                              </button>
                            </div>`;
}
       });}
}




function f1(trenerID){

        const formContainer = document.querySelector('.table_form')
        formContainer.classList.add('show-form');
        const trener_field = document.getElementById('id_trenerID');
        trener_field.value = trenerID;
        }

function show_hide_password(target, id){
    var input = document.getElementById(id);
    if(input.getAttribute('type')=='password') {
        target.src = '/static/image/hide.png';
        input.setAttribute('type', 'text');

    } else {
        target.src = '/static/image/open.png';
        input.setAttribute('type', 'password');
    }
    return false;
}

