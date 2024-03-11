resource "aws_s3_bucket" "tf_budget_tracker_bucket" {
  bucket = "tf-budget-tracker-bucket"
}

resource "aws_s3_object" "tf_budget_tracker_bucket_object_main" {
  bucket = aws_s3_bucket.tf_budget_tracker_bucket.id
  key    = "main.py"
  source = "../main.py"
  etag = "${filemd5("../main.py")}"

}
resource "aws_s3_object" "tf_budget_tracker_bucket_object_helper" {
  bucket = aws_s3_bucket.tf_budget_tracker_bucket.id
  key    = "helper.py"
  source = "../helper.py"
  etag = "${filemd5("../helper.py")}"
}

resource "aws_s3_object" "tf_budget_tracker_bucket_object_config" {
  bucket = aws_s3_bucket.tf_budget_tracker_bucket.id
  key    = "config.json"
  source = "../config.json"
  etag = "${filemd5("../config.json")}"
}

resource "aws_s3_object" "tf_budget_tracker_bucket_object_email" {
  bucket = aws_s3_bucket.tf_budget_tracker_bucket.id
  key    = "email_credentials.json"
  source = "../email_credentials.json"
  etag = "${filemd5("../email_credentials.json")}"
}