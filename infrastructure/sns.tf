resource "aws_cloudwatch_event_rule" "tf_glue_job_failure_rule" {
  name        = "${var.project_name}-glue-job-failure-rule"
  description = "Trigger on Glue job state changes"
  event_pattern = jsonencode({
    source      = ["aws.glue"],
    detail-type = ["Glue Job State Change"],
    detail = {
      "jobName" : ["${aws_glue_job.tf_budget_tracker_glue.name}"],
      "state" : ["FAILED", "ERROR", "STOPPED"]
    }
  })
}

resource "aws_sns_topic" "tf_budget_tracker_glue_sns" {
  name = "${tf-budgettracker}-glue-sns"
}

resource "aws_sns_topic_subscription" "user_updates_sqs_target" {
  topic_arn = aws_sns_topic.tf_budget_tracker_glue_sns.arn
  protocol  = "email"
  endpoint  = var.sns_email_address
}

resource "aws_cloudwatch_event_target" "tf_glue_failure_sns_target" {
  target_id = "tf-glue-sns-target"
  rule      = aws_cloudwatch_event_rule.tf_glue_job_failure_rule.name
  arn       = aws_sns_topic.tf_budget_tracker_glue_sns.arn
}

resource "aws_sns_topic_policy" "default" {
  arn    = aws_sns_topic.tf_budget_tracker_glue_sns.arn
  policy = data.aws_iam_policy_document.sns_topic_policy.json
}

data "aws_iam_policy_document" "sns_topic_policy" {
  statement {
    effect  = "Allow"
    actions = ["SNS:Publish"]

    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }

    resources = [aws_sns_topic.tf_budget_tracker_glue_sns.arn]
  }
}