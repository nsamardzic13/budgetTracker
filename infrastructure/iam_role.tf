resource "aws_iam_role" "tf_budget_tracker_role" {
  name = "tf-budget-tracker-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal: {
          Service  : "glue.amazonaws.com" 
        }
      }
    ]
  })
}