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

/* Notify to device */
function notify_device(device_id){
    $.post("/notify_device", { device_id: device_id },
      function callback(data){
           /* TODO: Display Modal message not an alert*/
           alert(data);
      });
}


function change_device_from_tab(device_id, to){
    var row = $('#row-id-' + device_id);
    row.remove();

    var tbody = (to == 'checkedin')? $("#checkedin-body"):$("#checkedout-body");
    tbody.append(row);

    if (to == 'checkedin'){
        swap_buttons(row, 'Check Out', 'Just Returned!', function () { check_out_device(device_id)});
    }else{
        swap_buttons(row, 'Check In', $('#user_nickname').val(), function () { check_in_device(device_id)});
    }
}

function swap_buttons(row, new_button_txt, second_row_txt, new_function) {
    row.children('td').eq(3).html(second_row_txt);
    row.find('button').html(new_button_txt);
    row.find('button').removeProp('onclick');
    row.find('button').unbind('click');
    row.find('button').bind('click', new_function);
}


function enable_client(){
    $('#client').prop('disabled',!$('#belongs_to_client').is(':checked'));
}


function filter_by(text){

    var regex = new RegExp( text + "\.*", 'gi');
    $('tr[id^="row-id"]').each(function(index, row){
      $(row).show();
      var assetId = $($(row).find("td")[0]).html();
      var text = $($(row).find("td")[1]).html();
      if (!assetId.match(regex) &&
          !text.match(regex)){
         $(row).hide()
      }
  });
}

function add_me_to_the_queue(device_id){

}

/* Making sure the device info is loaded everytime */
$('[data-load-remote]').on('click',function(e) {
    e.preventDefault();
    var $this = $(this);
    var remote = $this.data('load-remote');
    if(remote) {
        $($this.data('remote-target')).load(remote);
    }
});