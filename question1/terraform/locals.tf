locals {
  bucket_name   = "demo-tf-state-5456879"
  table_name    = "demo-tf-state-5456879"
  region        = "us-east-1"
  ecr_repo_name = "app-repo"

  hf_demo_cluster_name         = "hf-demo-cluster"
  availability_zones           = ["us-east-1a", "us-east-1b", "us-east-1c"]
  hf_demo_task_family          = "hf-demo-task"
  container_port               = 8080
  hf_demo_task_name            = "hf-demo-task"
  ecs_task_execution_role_name = "hf-demo-task-execution-role"

  application_load_balancer_name                = "cc-demo-app-alb"
  application_load_balancer_security_group_name = "cc-demo-app-alb-sg"
  target_group_name                             = "cc-demo-alb-tg"

  hf_demo_service_name = "hf_demo-service"
}