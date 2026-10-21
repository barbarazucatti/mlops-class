variable "region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "Perfil do AWS CLI (~/.aws/credentials)"
  type        = string
  default     = "default"
}

variable "nome" {
  description = "Prefixo dos recursos e alias do host SSH"
  type        = string
  default     = "mlops-aula4"
}

# Conta no plano gratuito só aceita tipos Free Tier; o maior é m7i-flex.large (2 vCPU / 8 GB).
# Airflow + Elasticsearch + BERT ficam apertados em 8 GB, por isso o user_data cria swap.
# Com conta no plano pago, prefira t3.xlarge (4 vCPU / 16 GB, ~US$ 0,17/h).
variable "instance_type" {
  description = "Tipo da instância EC2"
  type        = string
  default     = "m7i-flex.large"
}

variable "disco_gb" {
  description = "Tamanho do disco raiz (imagens Docker + modelo HF)"
  type        = number
  default     = 50
}
