#
# This file is used to define Terraform provider resources

# Heroku provider
#
# Provider for experiments and prototypes
#
# See https://www.terraform.io/docs/providers/aws/index.html#authentication for how to
# configure credentials to use this provider.
#
# AWS source: https://heroku.com
# Terraform source: https://www.terraform.io/docs/providers/heroku/index.html
provider "heroku" {
  version = "~> 1.3"
}

# AWS provider
#
# The BAS preferred public cloud provider.
#
# See https://www.terraform.io/docs/providers/aws/index.html#authentication for how to
# configure credentials to use this provider.
#
# AWS source: https://aws.amazon.com/
# Terraform source: https://www.terraform.io/docs/providers/aws/index.html
provider "aws" {
  version = "~> 1.34"

  region = "eu-west-1"
}
