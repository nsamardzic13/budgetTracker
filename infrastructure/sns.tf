resource "aws_cloudwatch_event_rule" "glue_job_failure_rule" {
  name        = "glue-job-failure-rule"
  description = "Trigger on Glue job state changes"
  event_pattern = jsonencode({
    source = ["aws.glue"],
    detail-type = ["Glue Job State Change"],
    detail = {
        "jobName": ["${aws_glue_job.tf_budget_tracker_glue.name}"],
        "state": ["FAILED", "ERROR", "STOPPED"]
    }
  })
}

resource "aws_sns_topic" "tf_budget_tracker_glue_sns" {
  name = "tf-budget-tracker-glue-sns"
}

resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  topic_arn = aws_sns_topic.tf_budget_tracker_glue_sns.arn
  protocol  = "email"
  endpoint  = var.sns_email_address
}

resource "aws_cloudwatch_event_target" "glue_failure_sns_target" {
  target_id = "glue-sns-target"
  rule      = aws_cloudwatch_event_rule.glue_job_failure_rule.name
  arn       = aws_sns_topic.tf_budget_tracker_glue_sns.arn
}