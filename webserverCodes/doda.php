 <?php

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

