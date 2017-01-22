<?php

global $CLat;
$dbhost = 'localhost';
$dbuser = 'shubhagr_retina';
$dbpass = 'anveshan_doda';
$dbname = 'shubhagr_dodadb';
$conn=mysqli_connect($dbhost,$dbuser,$dbpass,$dbname);


$latiarray  =  array();
$longiarray =  array();
$typearray  =  array();
$targetlatiarray  =  array();
$targetlongiarray =  array();
$originlatiarray  =  array();
$originlongiarray =  array();


if(!$conn){

die(mysql_error());

}



if(isset($_GET['user_cur_lat'])&&isset($_GET['user_cur_long'])&&isset($_GET['gesture'])&&isset($_GET['user_tar_lat'])&&isset($_GET['user_tar_long'])&&isset($_GET['user_start_lat'])&&isset($_GET['user_start_longi']))
{


$CLat = $_GET['user_cur_lat'];
$CLong = $_GET['user_cur_long'];
$gesture= $_GET['gesture'];
$TLat = $_GET['user_tar_lat'];
$TLong = $_GET['user_tar_long'];
$SLat = $_GET['user_start_lat'];
$SLong = $_GET['user_start_longi'];


$sql = "INSERT INTO dodalogtable (targetLati, targetLongi, originLati, originLongi, currentLati, currentLongi, gesture) VALUES ($TLat, $TLong, $SLat, $SLong, $CLat, $CLong, $gesture)";

if (mysqli_query($conn, $sql)) {
    echo "New record created successfully";
    echo "Target Latitude : " . $TLat . "  Target Longitude : " . $TLong . "  Current Latitude : " . $CLat . "  Current Longitude : " . $CLong . "  Gesture : " . $gesture . " | ";
} else {
    echo "New record not created " . $sql . "<br>" . mysqli_error($conn);
}


}

else
{
  $sql = "SELECT id, targetLati, targetLongi, originLati, originLongi, currentLati, currentLongi, gesture, timestamp FROM dodalogtable ORDER BY id DESC LIMIT 5";
  $result = $conn->query($sql);
  $counter = 0;
  if ($result->num_rows > 0) {
      // output data of each row
      while($row = $result->fetch_assoc()) {

          echo "id: " . $row["id"] . " | Last Entry made : " . $row["timestamp"] . "  | Current target Latitude : " . $row["targetLati"] . "  | Current target Longtitude : " . $row["targetLongi"] . "  |  Current Position : " . $row["currentLati"] . " : " . $row["currentLongi"] . "\r\n" ;
          array_push( $targetlatiarray  , $row["originLati"]  );
          array_push( $targetlongiarray , $row["originLongi"]  );
          array_push( $originlatiarray  , $row["targetLati"]  );
          array_push( $originlongiarray , $row["targetLongi"]  );

        $counter = $counter + 1;
        array_push( $latiarray , $row["currentLati"]  );
        array_push( $longiarray, $row["currentLongi"] );
        array_push( $typearray , $counter             );

      }
      // Start XML file, echo parent node



  } else {
      echo "0 results";
  }



}


mysqli_close($conn);

?>

<html>

<div id="dom" style="display: none;">
  <?php
  $z="|";
  for ($x = 0; $x <= 4; $x++)
  {
  echo htmlspecialchars($latiarray[$x]);
  echo htmlspecialchars($z);
  echo htmlspecialchars($longiarray[$x]);
  echo htmlspecialchars($z);
  echo htmlspecialchars($typearray[$x]);
  echo htmlspecialchars($z);
}
echo htmlspecialchars($targetlatiarray[0]);
echo htmlspecialchars($z);
echo htmlspecialchars($targetlongiarray[0]);
echo htmlspecialchars($z);
echo htmlspecialchars(6);
echo htmlspecialchars($z);
echo htmlspecialchars($originlatiarray[0]);
echo htmlspecialchars($z);
echo htmlspecialchars($originlongiarray[0]);
echo htmlspecialchars($z);
echo htmlspecialchars(7);
echo htmlspecialchars($z);

  ?>
</div>


<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCDSBgT0i8uM-pk8J62gon4jwkHpn14dT0&callback=initMap" type="text/javascript"></script>

<script type="text/javascript">



var customIcons = {
      1: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_blue.png'
      },
      2: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_red.png'
      },
      3: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_orange.png'
      },
      4: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_yellow.png'
      },
      5: {
        icon: 'http://labs.google.com/ridefinder/images/mm_20_green.png'
      }
    };


    function load() {



      var div = document.getElementById("dom");
      var myData = div.textContent;
      var array = myData.split("|");

      var latit = parseFloat(array[18]);
      var longit = parseFloat(array[19]);

          var infoWindow = new google.maps.InfoWindow;

                      var map = new google.maps.Map(document.getElementById("map"), {
                        center: new google.maps.LatLng(latit, longit),
                        zoom: 15,
                        mapTypeId: 'roadmap'
                      });
          // Change this depending on the name of your PHP file

var color = ['#FF0000','#FF9900','#FFF200','#99FF00','#00FFd0'];
var k = 0;
for (k=0; k < color.length; k++)
{
          var flightPlanCoordinates = [
           {lat: parseFloat(array[3*k]), lng: parseFloat(array[3*k+1])},
           {lat: parseFloat(array[3*(k+1)]), lng: parseFloat(array[3*(k+1)+1])}
           ];
         var flightPath = new google.maps.Polyline({
           path: flightPlanCoordinates,
           geodesic: true,
           strokeColor: color[k],
           strokeOpacity: 1.0,
           strokeWeight: 2
         });
         flightPath.setMap(map);
 }
        var type = ['1','2','3','4','5'];
        var j = 0;
        for (j=0; j < type.length; j++){
        var point = new google.maps.LatLng(parseFloat(array[3*j]),parseFloat(array[3*j+1]) );
        var icon = customIcons[type[j]] || {};
        var marker = new google.maps.Marker({
          map: map,
          position: point,
          icon: icon.icon
        });

        bindInfoWindow(marker, map, infoWindow,type[j]);
      }
        }
            function bindInfoWindow(marker, map, infoWindow, html) {
              google.maps.event.addListener(marker, 'click', function() {
                infoWindow.setContent(html);
                infoWindow.open(map, marker);
              });
            }

            function downloadUrl(url, callback) {
              var request = window.ActiveXObject ?
                  new ActiveXObject('Microsoft.XMLHTTP') :
                  new XMLHttpRequest;

              request.onreadystatechange = function() {
                if (request.readyState == 4) {
                  request.onreadystatechange = doNothing;
                  callback(request, request.status);
                }
              };

              request.open('GET', url, true);
              request.send(null);
            }

            function doNothing() {}


</script>

<head>
<meta http-equiv="refresh" content="400" >
</head>
<body onload="load()">

<h1> Retina Squared : Google Maps  </h1>
<p id="demo">
</p>

<div id="map" style="width:100%;height:500px"></div>


</body>
</html>
