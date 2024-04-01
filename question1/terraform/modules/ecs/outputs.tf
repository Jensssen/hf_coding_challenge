output "load_balancer_ip" {
  value = aws_lb.application_load_balancer.dns_name
}