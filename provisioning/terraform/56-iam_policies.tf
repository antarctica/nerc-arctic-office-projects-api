#
# This file is used to define and assign AWS IAM policies definining sets of permissions or restrictions to resources
# Policies can be applied to combinations of users, roles and groups as required

#    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *
#
# Policy definitions & assignments
#
#    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *    *

# BAS API Docs access policy
#
# Policy to upload documentation for a specific project
#
# Inline policy
#
# This resource implicitly depends on the 'aws_iam_user.bas-gitlab-arctic-office-projects-api' resource
# This resource relies on the AWS Terraform provider being previously configured.
#
# AWS source: http://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#customer-managed-policies
# Terraform source: https://www.terraform.io/docs/providers/aws/r/iam_user_policy.html
#
# Tags are not supported by this resource
resource "aws_iam_user_policy" "manage-api-documentation-bas-arctic-office-projects-api" {
  name   = "manage-api-documentation-bas-arctic-office-projects-api"
  user   = "${aws_iam_user.bas-gitlab-arctic-office-projects-api.name}"
  policy = "${file("70-resources/iam/policies/inline/bas-api-docs.json")}"
}
