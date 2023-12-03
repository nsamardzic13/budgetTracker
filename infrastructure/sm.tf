resource "aws_secretsmanager_secret" "service_account" {
  name = "google-service-account"
}

resource "aws_secretsmanager_secret_version" "service_account_version" {
  secret_id     = aws_secretsmanager_secret.service_account.id
  secret_string = file("../service_account.json")
}