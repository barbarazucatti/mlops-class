output "ip_publico" {
  value = aws_instance.this.public_ip
}

output "ssh" {
  value = "ssh -i ${local_sensitive_file.chave_privada.filename} ubuntu@${aws_instance.this.public_ip}"
}

output "ssh_config" {
  description = "Cole no ~/.ssh/config para o VSCode Remote-SSH"
  value       = <<-EOT

    Host ${var.nome}
      HostName ${aws_instance.this.public_ip}
      User ubuntu
      IdentityFile ${local_sensitive_file.chave_privada.filename}
      LocalForward 8080 localhost:8080
      LocalForward 8501 localhost:8501
      LocalForward 3000 localhost:3000
      LocalForward 9200 localhost:9200
  EOT
}

output "pasta_projeto" {
  description = "Pasta do projeto na instância (abrir no VSCode Remote-SSH)"
  value       = local.pasta_remota
}
