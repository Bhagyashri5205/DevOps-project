variable "aws_region" {
  default = "ap-south-1"
}

variable "ami_id" {
  description = "Amazon Linux AMI"
  default     = "ami-0f5ee92e2d63afc18"
}

variable "my_ip" {
  description = "Your public IP for SSH"
  type        = string
}