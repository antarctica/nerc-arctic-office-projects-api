#
# This file is used to define AWS IAM users to which permissions can be assigned by policies, optionally via groups

# GitLab CI/CD user
#
# See '56-iam_policies.tf' for permission assignment
#
# This resource relies on the AWS Terraform provider being previously configured.
#
# AWS source: http://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html
# Terraform source: https://www.terraform.io/docs/providers/aws/r/iam_user.html
#
# Tags are not supported by this resource
resource "aws_iam_user" "bas-gitlab-arctic-office-projects-api" {
  name = "bas-gitlab-arctic-office-projects-api"
}
