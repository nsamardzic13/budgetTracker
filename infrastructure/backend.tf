terraform {
  backend "s3" {
    bucket  = "tf-my-backend-bucket"
    encrypt = true
    key     = "${var.project_name}-terraform.tfstate"
    region  = "eu-central-1"
  }
}