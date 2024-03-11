variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "tf-budgettracker"
}

variable "additional_python_modules" {
  description = "Additional Python modules used in Glue"
  type = list(string)
  default = ["gspread","redmail","matplotlib","plotly","kaleido"]
}

variable "sns_email_address" {
  type    = string
  default = "nikola.samardzic1997+AWS@gmail.com"
}