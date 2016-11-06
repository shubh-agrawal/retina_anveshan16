<?php

global $CLat; 
$dbhost = 'localhost';
$dbuser = 'shubhagr_retina';
$dbpass = 'anveshan_doda';
$dbname = 'shubhagr_dodadb';
$conn=mysqli_connect($dbhost,$dbuser,$dbpass,$dbname);
                      
if(!$conn){
            	      
die(mysql_error());

}



if(isset($_GET['user_cur_lat'])&&isset($_GET['user_cur_long'])&&isset($_GET['gesture'])&&isset($_GET['user_tar_lat'])&&isset($_GET['user_tar_long'])){
                                    

$CLat = $_GET['user_cur_lat'];
$CLong = $_GET['user_cur_long'];
$gesture= $_GET['gesture'];
$TLat = $_GET['user_tar_lat'];
$TLong = $_GET['user_tar_long'];

              	 
$sql = "INSERT INTO dodalogtable (targetLati, targetLongi, currentLati, currentLongi, gesture) VALUES ($TLat, $TLong, $CLat, $CLong, $gesture)";

if (mysqli_query($conn, $sql)) {
    echo "New record created successfully";
    echo "Target Latitude : " . $TLat . "  Target Longitude : " . $TLong . "  Current Latitude : " . $CLat . "  Current Longitude : " . $CLong . "  Gesture : " . $gesture . " | ";
} else {
    echo "Maiyya Chud Gayi : " . $sql . "<br>" . mysqli_error($conn);
}


}
else
{
    echo " Badi Wali Chudi Hai | Dhang se daalo request" ;
}
mysqli_close($conn);
			
?>

<html>
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCDSBgT0i8uM-pk8J62gon4jwkHpn14dT0&callback=initMap" type="text/javascript"></script>

<script type="text/javascript">

var customIcons = {
      restaurant: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png'
      },
      bar: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_red.png'
      }
    };



function myMap() {
  var map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(22.316273, 87.306028),
        zoom: 13,
        mapTypeId: 'roadmap'
      });
  var point = new google.maps.LatLng(
              parseFloat($CLat),
              parseFloat($CLong));

  var icon = customIcons[restaurant] || {};

  var marker = new google.maps.Marker({
            map: map,
            position: point,
            icon: icon.icon
          });
  
  var icon = customIcons[bar] || {};
  
  var point = new google.maps.LatLng(
              parseFloat($TLat),
              parseFloat($TLong));

  var marker = new google.maps.Marker({
            map: map,
            position: point,
            icon: icon.icon
          }); 


}
</script>

<body onload="myMap()">

<h1>            Retina Squared : Google Maps</h1>

<div id="map" style="width:100%;height:500px"></div>


</body>
</html>

