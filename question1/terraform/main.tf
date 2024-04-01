terraform {
  required_version = "~> 1.7"

  backend "s3" {
    bucket         = "demo-tf-state-5456879"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "demo-tf-state-5456879"
    encrypt        = true
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

module "tf-state" {
  source      = "./modules/tf-state"
  bucket_name = local.bucket_name
  table_name  = local.table_name
}

module "ecrRepo" {
  source        = "./modules/ecr"
  ecr_repo_name = local.ecr_repo_name
}

module "ecsCluster" {
  source = "./modules/ecs"

  hf_demo_cluster_name = local.hf_demo_cluster_name
  availability_zones   = local.availability_zones

  hf_demo_task_family          = local.hf_demo_task_family
  ecr_repo_url                 = module.ecrRepo.repository_url
  container_port               = local.container_port
  hf_demo_task_name            = local.hf_demo_task_name
  ecs_task_execution_role_name = local.ecs_task_execution_role_name

  application_load_balancer_name                = local.application_load_balancer_name
  application_load_balancer_security_group_name = local.application_load_balancer_security_group_name
  target_group_name                             = local.target_group_name
  hf_demo_service_name                          = local.hf_demo_service_name
}
