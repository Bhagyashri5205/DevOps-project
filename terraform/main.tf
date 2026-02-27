provider "aws" {
  region = var.aws_region
}

# Secure Security Group
resource "aws_security_group" "devsecops_sg" {
  name        = "devsecops-secure-sg"
  description = "Allow limited SSH access"

  ingress {
    description = "SSH only from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]   #  NOT 0.0.0.0/0
  }

  egress {
    description = "Allow HTTPS only"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Secure EC2 Instance
resource "aws_instance" "devsecops_vm" {
  ami           = var.ami_id
  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.devsecops_sg.id]

  #  Encrypted root volume
  root_block_device {
    encrypted = true
  }

  #  Enforce IMDSv2
  metadata_options {
    http_tokens = "required"
  }

  tags = {
    Name = "DevSecOps-Dashboard-VM"
  }
}