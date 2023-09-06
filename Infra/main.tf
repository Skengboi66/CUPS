# Configure the AWS provider
provider "aws" {
  region = "us-east-1" # Replace this with your desired AWS region
  access_key = 
  secret_key = 
}

# Create a new security group to allow SSH access (Port 22) and HTTP access (Port 80)
resource "aws_security_group" "ec2_instance" {
  name        = "ec2-instance-sg"
  description = "Security group for EC2 instance"
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an EC2 instance
resource "aws_instance" "ec2_instance" {
  ami           = "ami-0c55b159cbfafe1f0" # Replace this with your desired AMI ID
  instance_type = "t2.micro"
  key_name      = "your_key_pair_name" # Replace this with your EC2 key pair name
  security_groups = [
    aws_security_group.ec2_instance.name,
  ]
}

# Output the public IP address of the EC2 instance
output "public_ip" {
  value = aws_instance.ec2_instance.public_ip
}