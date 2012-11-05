/**
 * Created with PyCharm.
 * User: bakeneko
 * Date: 11/3/12
 * Time: 12:29 PM
 * To change this template use File | Settings | File Templates.
 */

/*
* Yeah, I know this should be jquery plug ins. :S
* */
/*Checkout a device*/
function check_out_device(device_id){
    $.post("/checkout_device", { device_id: device_id },
      function callback(data){
          console.log(data);
          change_device_from_tab(device_id,"checkedout");
      });
}


/*Checkin a device*/
function check_in_device(device_id){
    $.post("/checkin_device", { device_id: device_id },
      function callback(data){
          change_device_from_tab(device_id,"checkedin");
      });
}



function change_device_from_tab(device_id, to){
    var row = $('#row-id-' + device_id);
    row.remove();

    var tbody = (to == 'checkedin')? $("#checkedin-body"):$("#checkedout-body");
    tbody.append(row);

    if (to == 'checkedin'){
        swap_buttons(row, 'Checkout', 'Just Returned!', function () { check_out_device(device_id)});
    }else{
        swap_buttons(row, 'Check it in', 'myself!!', function () { check_in_device(device_id)});
    }
}

function swap_buttons(row, new_button_txt, second_row_txt, new_function) {
    row.children('td').eq(1).html(second_row_txt);
    row.find('button').html(new_button_txt);
    row.find('button').removeProp('onclick');
    row.find('button').unbind('click');
    row.find('button').bind('click', new_function);
}


function enable_client(){
    $('#client').prop('disabled',!$('#belongs_to_client').is(':checked'));
}

$('[data-load-remote]').on('click',function(e) {
    e.preventDefault();
    var $this = $(this);
    var remote = $this.data('load-remote');
    if(remote) {
        $($this.data('remote-target')).load(remote);
    }
});