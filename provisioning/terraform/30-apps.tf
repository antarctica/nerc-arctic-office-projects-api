#
# This file is used to define compute resources for applications

# Pipeline
#
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/pipelines
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/pipeline.html
resource "heroku_pipeline" "bas-arctic-office-projects-api" {
  name = "bas-arctic-office-projects-api"
}

# Staging app
#
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/how-heroku-works#defining-an-application
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/app.html
resource "heroku_app" "bas-arctic-office-projects-api-stage" {
  name   = "bas-arctic-projects-api-stage"
  region = "eu"

  config_vars {
    REVERSE_PROXY_PATH                 = "/arctic-office-projects/testing"
    AZURE_OAUTH_TENANCY                = "d14c529b-5558-4a80-93b6-7655681e55d6"
    AZURE_OAUTH_APPLICATION_ID         = "2b3f5c55-1a7d-4e26-a9a7-5b56b0f612f1"
    AZURE_OAUTH_CLIENT_APPLICATION_IDS = "${join(",", var.azure-oauth-client-application-ids-stage)}"
  }
}

variable "azure-oauth-client-application-ids-stage" {
  default = [
    "76ee9805-1ec6-47c8-a57d-df002c54e498",
    "8646223c-46aa-4bc3-a825-562cbea4911d",
    "e52f2b95-2cff-4a97-97c1-f154c79b5292",
    "9657cd94-0a8d-4e8b-b134-3d695e2bdc5f",
  ]
}

# Production app
#
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/how-heroku-works#defining-an-application
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/app.html
resource "heroku_app" "bas-arctic-office-projects-api-prod" {
  name   = "bas-arctic-projects-api-prod"
  region = "eu"

  config_vars {
    REVERSE_PROXY_PATH                 = "/arctic-office-projects"
    AZURE_OAUTH_TENANCY                = "b311db95-32ad-438f-a101-7ba061712a4e"
    AZURE_OAUTH_APPLICATION_ID         = "e82569d7-861c-4d38-b243-c9400925f2c4"
    AZURE_OAUTH_CLIENT_APPLICATION_IDS = "${join(",", var.azure-oauth-client-application-ids-prod)}"
  }
}

variable "azure-oauth-client-application-ids-prod" {
  default = [
    "8d8c9933-2eed-4520-906c-f40d556e0423"
  ]
}

# Staging dyno
#
# This resource implicitly depends on the 'heroku_app.bas-arctic-office-projects-api-stage' resource.
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/dyno-types
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/formation.html
resource "heroku_formation" "bas-arctic-office-projects-api-stage" {
  app      = "${heroku_app.bas-arctic-office-projects-api-stage.name}"
  type     = "web"
  quantity = 1
  size     = "hobby"
}

# Production dyno
#
# This resource implicitly depends on the 'heroku_app.bas-arctic-office-projects-api-prod' resource.
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/dyno-types
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/formation.html
resource "heroku_formation" "bas-arctic-office-projects-api-prod" {
  app      = "${heroku_app.bas-arctic-office-projects-api-prod.name}"
  type     = "web"
  quantity = 1
  size     = "hobby"
}

# Staging pipeline app
#
# This resource implicitly depends on the 'heroku_pipeline.bas-arctic-office-projects-api' resource.
# This resource implicitly depends on the 'heroku_app.bas-arctic-office-projects-api-stage' resource.
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/pipelines#adding-apps-to-a-pipeline
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/pipeline_coupling.html
resource "heroku_pipeline_coupling" "bas-arctic-office-projects-api-stage" {
  app      = "${heroku_app.bas-arctic-office-projects-api-stage.name}"
  pipeline = "${heroku_pipeline.bas-arctic-office-projects-api.id}"
  stage    = "staging"
}

# Production pipeline app
#
# This resource implicitly depends on the 'heroku_pipeline.bas-arctic-office-projects-api' resource.
# This resource implicitly depends on the 'heroku_app.bas-arctic-office-projects-api-prod' resource.
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/pipelines#adding-apps-to-a-pipeline
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/pipeline_coupling.html
resource "heroku_pipeline_coupling" "bas-arctic-office-projects-api-prod" {
  app      = "${heroku_app.bas-arctic-office-projects-api-prod.name}"
  pipeline = "${heroku_pipeline.bas-arctic-office-projects-api.id}"
  stage    = "production"
}
