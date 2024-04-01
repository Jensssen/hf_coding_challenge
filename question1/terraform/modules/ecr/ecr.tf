resource "aws_ecr_repository" "hf_demo" {
  name = var.ecr_repo_name
}