provider "aws" {
  region = "us-east-1"  # Mets la même région que ton ECR
}

# Créer un nouveau Key Pair
resource "aws_key_pair" "my_new_key" {
  key_name   = "MyNewKeyPair"
  public_key = file("MyNewKeyPair.pub")  # la clé publique générée sur ta VM
}

resource "aws_security_group" "sg" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # pour accéder à ton service
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "my_ec2" {
  ami           = "ami-03c1f788292172a4e"  # Ubuntu 22.04 LTS
  instance_type = "t3.micro"
  key_name      = aws_key_pair.my_new_key.key_name
  vpc_security_group_ids = [aws_security_group.sg.id]

  # user_data pour installer Docker et lancer le conteneur automatiquement
  user_data = <<-EOF
              #!/bin/bash
              apt update -y
              apt install -y docker.io unzip curl
              systemctl start docker
              systemctl enable docker

              # Installer AWS CLI v2
              curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
              unzip awscliv2.zip
              ./aws/install

              # Login ECR
              aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 859525219095.dkr.ecr.us-east-1.amazonaws.com

              # Lancer le conteneur
              docker run -d -p 3000:3000 859525219095.dkr.ecr.us-east-1.amazonaws.com/building_energy_predictor:latest
              EOF

  tags = {
    Name = "MyTerraformEC2"
  }
}

