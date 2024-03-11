resource "aws_s3_bucket" "tf_budget_tracker_bucket" {
  bucket = "tf-budget-tracker-bucket"
}

resource "aws_s3_object" "tf_budget_tracker_bucket_object_main" {
  bucket = aws_s3_bucket.tf_budget_tracker_bucket.id
  key    = "main.py"
  source = "../main.py"

}
resource "aws_s3_object" "tf_budget_tracker_bucket_object_helper" {
  bucket = aws_s3_bucket.tf_budget_tracker_bucket.id
  key    = "helper.py"
  source = "../helper.py"
}

resource "aws_s3_object" "tf_budget_tracker_bucket_object_config" {
  bucket = aws_s3_bucket.tf_budget_tracker_bucket.id
  key    = "config.json"
  source = "../config.json"
}

resource "aws_s3_object" "tf_budget_tracker_bucket_object_email" {
  bucket = aws_s3_bucket.tf_budget_tracker_bucket.id
  key    = "email_credentials.json"
  source = "../email_credentials.json"
}