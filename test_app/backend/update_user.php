<?php

header("Content-Type: application/json; charset=UTF-8");

require_once "db.php";

$input = json_decode(file_get_contents("php://input"), true);

if (!$input) {
    echo json_encode([
        "success" => false,
        "message" => "No JSON data received"
    ]);
    exit;
}

$user_id = intval($input["user_id"] ?? 0);
$first_name = trim($input["first_name"] ?? "");
$last_name = trim($input["last_name"] ?? "");
$gender = trim($input["gender"] ?? "");
$birth_date = trim($input["birth_date"] ?? "");
$zodiac = trim($input["zodiac"] ?? "");
$age = intval($input["age"] ?? -1);

if (
    $user_id <= 0 ||
    $first_name === "" ||
    $last_name === "" ||
    $gender === "" ||
    $birth_date === "" ||
    $zodiac === "" ||
    $age < 0
) {
    echo json_encode([
        "success" => false,
        "message" => "Invalid or missing fields"
    ]);
    exit;
}

try {
    $sql = "
        UPDATE users
        SET
            first_name = :first_name,
            last_name = :last_name,
            gender = :gender,
            birth_date = :birth_date,
            zodiac = :zodiac,
            age = :age
        WHERE id = :user_id
    ";

    $stmt = $pdo->prepare($sql);

    $stmt->execute([
        ":first_name" => $first_name,
        ":last_name" => $last_name,
        ":gender" => $gender,
        ":birth_date" => $birth_date,
        ":zodiac" => $zodiac,
        ":age" => $age,
        ":user_id" => $user_id
    ]);

    echo json_encode([
        "success" => true,
        "message" => "User updated successfully"
    ]);

} catch (PDOException $e) {
    http_response_code(500);

    echo json_encode([
        "success" => false,
        "message" => "User update failed"
    ]);
}
