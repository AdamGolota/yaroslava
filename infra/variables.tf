variable "region" {
  description = "AWS region to deploy resources to"
  default     = "eu-central-1"
}

variable "prefix" {
  description = "Prefix to be assigned to resources."
  default     = "yaroslava-k8s"
}

variable "db_password" {
  description = "Password for the RDS database instance."
  default     = "samplepassword123"
}
