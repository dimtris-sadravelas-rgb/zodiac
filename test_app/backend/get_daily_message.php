<?php

header("Content-Type: application/json; charset=UTF-8");

require_once "db.php";

$zodiac = trim($_GET["zodiac"] ?? "");

if ($zodiac === "") {
    echo json_encode([
        "success" => false,
        "message" => "Missing zodiac"
    ]);
    exit;
}

try {
    $sql = "
        SELECT message
        FROM daily_messages
        WHERE zodiac = :zodiac
        ORDER BY message_date DESC
        LIMIT 1
    ";

    $stmt = $pdo->prepare($sql);
    $stmt->execute([
        ":zodiac" => $zodiac
    ]);

    $message = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($message) {
        echo json_encode([
            "success" => true,
            "message" => $message["message"]
        ]);
    } else {
        echo json_encode([
            "success" => true,
            "message" => "Δεν υπάρχει διαθέσιμο ημερήσιο μήνυμα για σήμερα."
        ]);
    }

} catch (PDOException $e) {
    http_response_code(500);

    echo json_encode([
        "success" => false,
        "message" => "Could not load daily message"
    ]);
}
