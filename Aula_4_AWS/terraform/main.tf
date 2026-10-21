terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 3.4"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = var.aws_profile
}

# --- Seu IP público (para liberar o SSH só para você) ---
data "http" "meu_ip" {
  url = "https://checkip.amazonaws.com"
}

locals {
  meu_ip_cidr  = "${chomp(data.http.meu_ip.response_body)}/32"
  pasta_remota = "/home/ubuntu/Aula_4"
}

# --- Imagem Ubuntu 24.04 LTS mais recente (parâmetro público da Canonical) ---
data "aws_ssm_parameter" "ubuntu_ami" {
  name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
}

# --- Par de chaves SSH gerado pelo Terraform ---
resource "tls_private_key" "ssh" {
  algorithm = "ED25519"
}

resource "aws_key_pair" "this" {
  key_name   = "${var.nome}-key"
  public_key = tls_private_key.ssh.public_key_openssh
}

resource "local_sensitive_file" "chave_privada" {
  content         = tls_private_key.ssh.private_key_openssh
  filename        = pathexpand("~/.ssh/${var.nome}.pem")
  file_permission = "0600"
}

# --- Security group: apenas SSH a partir do seu IP ---
# As portas das aplicações (8080, 8501, 3000, 9200) são acessadas via
# port forwarding do VSCode Remote-SSH, então não ficam expostas na internet.
resource "aws_security_group" "this" {
  name        = "${var.nome}-sg"
  description = "SSH apenas do IP do aluno"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [local.meu_ip_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# --- Instância EC2 ---
resource "aws_instance" "this" {
  ami                    = nonsensitive(data.aws_ssm_parameter.ubuntu_ami.value)
  instance_type          = var.instance_type
  key_name               = aws_key_pair.this.key_name
  vpc_security_group_ids = [aws_security_group.this.id]
  user_data              = file("${path.module}/user_data.sh")

  root_block_device {
    volume_size = var.disco_gb
    volume_type = "gp3"
  }

  tags = {
    Name = var.nome
  }
}

# --- Envia o projeto para a instância (funciona em macOS, Linux e Windows) ---
# Para reenviar depois: terraform apply -replace=terraform_data.projeto
resource "terraform_data" "projeto" {
  triggers_replace = aws_instance.this.id

  connection {
    type        = "ssh"
    host        = aws_instance.this.public_ip
    user        = "ubuntu"
    private_key = tls_private_key.ssh.private_key_openssh
  }

  # Espera o user_data terminar de instalar o Docker
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait > /dev/null || true",
      "docker --version",
      "mkdir -p ${local.pasta_remota}",
    ]
  }

  provisioner "file" {
    source      = "${path.module}/../moduloairflow"
    destination = local.pasta_remota
  }

  provisioner "file" {
    source      = "${path.module}/../moduloapp"
    destination = local.pasta_remota
  }

  provisioner "file" {
    source      = "${path.module}/../dashboardgrafana"
    destination = local.pasta_remota
  }

  provisioner "file" {
    source      = "${path.module}/../docker-compose.yaml"
    destination = "${local.pasta_remota}/docker-compose.yaml"
  }

  provisioner "file" {
    source      = "${path.module}/../.env"
    destination = "${local.pasta_remota}/.env"
  }

  provisioner "file" {
    source      = "${path.module}/../LEIAME.txt"
    destination = "${local.pasta_remota}/LEIAME.txt"
  }
}
