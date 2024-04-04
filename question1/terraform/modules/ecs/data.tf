data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "sagemaker_access" {
  # Enables container debugging via ssh
  statement {
    effect    = "Allow"
    actions   = ["ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel"]
    resources = ["*"]
  }
  # Allow sagemaker endpoint access following least privileges
  statement {
    effect    = "Allow"
    actions   = ["sagemaker:InvokeEndpoint",
                "sagemaker:DescribeEndpoint",
                "sagemaker:DescribeEndpointConfig",
                "sagemaker:ListInferenceComponents",
                "sagemaker:ListTags"]
    resources = ["*"]
  }
  statement {
    effect    = "Allow"
    actions   = ["s3:GetObject"]
    resources = ["*"]
  }
}
