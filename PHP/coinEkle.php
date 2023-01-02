<?php
$servername = "serverip";
$username = "username";
$password = "password";
$dbname = "dbname";

//$id=$_GET['id']; 
$coinName=$_GET['coinName']; 

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$sql = "insert into signals values (id, $coinName, 0)";
$result = $conn->query($sql);
$conn->close();
?>