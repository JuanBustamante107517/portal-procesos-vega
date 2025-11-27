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