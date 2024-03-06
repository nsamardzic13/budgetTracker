variable "project_name" {
  description = "Name of the project"
  type = string
  default = "tf-budgettracker"
}

variable "sns_email_address" {
  type = string
  default = "nikola.samardzic1997+AWS@gmail.com"
}