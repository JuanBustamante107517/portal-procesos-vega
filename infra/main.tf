# 1. Definimos el proveedor (AWS)
provider "aws" {
  region = "us-east-1"  # Norte de Virginia (la región estándar)
}

# 2. Creamos la VPC (Tu red privada principal)
resource "aws_vpc" "main_vpc" {
  cidr_block           = "10.0.0.0/16" # Rango de IPs (65,536 direcciones)
  enable_dns_hostnames = true
  
  tags = {
    Name = "PortalVega-VPC" # Así aparecerá en la consola de AWS
    Project = "PortalVega"
  }
}

# 3. Creamos una Subred Pública (Donde vivirá el Frontend)
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.1.0/24" # Rango más pequeño (256 IPs)
  availability_zone       = "us-east-1a"  # Zona A
  map_public_ip_on_launch = true          # Asigna IP pública automática

  tags = {
    Name = "PortalVega-Public-Subnet"
  }
}

# 4. Creamos el Internet Gateway (La puerta para salir a Internet)
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "PortalVega-IGW"
  }
}

# 5. Creamos una Tabla de Enrutamiento (El mapa para el tráfico)
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0" # Todo el tráfico de internet...
    gateway_id = aws_internet_gateway.igw.id # ...se va por el Gateway
  }

  tags = {
    Name = "PortalVega-Public-RT"
  }
}

# 6. Asociamos la Subred con la Tabla de Enrutamiento
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# --- LO NUEVO PARA EL DESPLIEGUE FINAL ---

# 7. Security Group (El Firewall para abrir puertos 8001 y 5173)
resource "aws_security_group" "portal_sg" {
  name        = "portal_vega_sg"
  description = "Permitir trafico Web y API"
  vpc_id      = aws_vpc.main_vpc.id  # Conectado a TU VPC creada arriba

  # Puerto Frontend (React)
  ingress {
    from_port   = 5173
    to_port     = 5173
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Puerto Backend (Django)
  ingress {
    from_port   = 8001
    to_port     = 8001
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH (Para que entres a configurar si hace falta)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Salida libre a internet (Para descargar Docker, etc.)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "PortalVega-SG"
  }
}

# --- BUSCADOR AUTOMÁTICO DE AMI (Amazon Linux 2) ---
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# 8. Instancia EC2 (El servidor donde correrá Docker)
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.portal_sg.id]

  tags = {
    Name = "PortalVega-Server-PROD"
  }

  # Script de Automatización (Lo que pide el profesor)
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              amazon-linux-extras install docker -y
              service docker start
              usermod -a -G docker ec2-user
              curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              EOF
}

# 9. Output (La IP que le entregarás al profesor)
output "ip_publica_final" {
  description = "IP Publica para la entrega final"
  value       = aws_instance.app_server.public_ip
}