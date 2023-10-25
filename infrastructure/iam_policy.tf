resource "aws_iam_role_policy_attachment" "SecretsManagerReadWrite" {
  role = aws_iam_role.tf_budget_tracker_role.name
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
}

resource "aws_iam_role_policy_attachment" "AWSGlueConsoleFullAccess" {
  role = aws_iam_role.tf_budget_tracker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
}

resource "aws_iam_role_policy_attachment" "AWSGlueServiceRole" {
  role = aws_iam_role.tf_budget_tracker_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy_attachment" "CloudWatchLogsFullAccess" {
  role = aws_iam_role.tf_budget_tracker_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
}

resource "aws_iam_role_policy_attachment" "AmazonS3FullAccess" {
  role = aws_iam_role.tf_budget_tracker_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "IAMFullAccess" {
  role = aws_iam_role.tf_budget_tracker_role.name
  policy_arn = "arn:aws:iam::aws:policy/IAMFullAccess"
}