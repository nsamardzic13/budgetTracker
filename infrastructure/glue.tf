resource "aws_glue_job" "tf_budget_tracker_glue" {
  name = "tf-budget-tracker-glue"
  role_arn = aws_iam_role.tf_budget_tracker_role.arn
  glue_version = "3.0"
  max_capacity = "0.0625"
  command {
    name = "pythonshell"
    script_location = "s3://${aws_s3_bucket.tf_budget_tracker_bucket.bucket}/main.py"
    python_version = "3.9"
  }
  default_arguments = {
    "--additional-python-modules": "gspread,redmail,matplotlib,plotly,kaleido"
    "--extra-py-files" : "s3://${aws_s3_bucket.tf_budget_tracker_bucket.bucket}/helper.py"
  }
}

resource "aws_glue_trigger" "tf_budget_tracker_glue_trigger" {
  name = "tf-budget-tracker-glue-trigger"
  type = "SCHEDULED"
  schedule = "cron(00 07 ? * MON *)"

  actions {
    job_name = aws_glue_job.tf_budget_tracker_glue.name
  }
}