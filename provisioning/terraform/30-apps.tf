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

# Staging stage
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
    AZURE_OAUTH_CLIENT_APPLICATION_IDS = "76ee9805-1ec6-47c8-a57d-df002c54e498"
  }
}

# # Production stage
# #
# # This resource relies on the Heroku Terraform provider being previously configured.
# #
# # Heroku source: https://devcenter.heroku.com/articles/how-heroku-works#defining-an-application
# # Terraform source: https://www.terraform.io/docs/providers/heroku/r/app.html
# resource "heroku_app" "bas-arctic-office-projects-api-prod" {
#   name   = "bas-arctic-projects-api-prod"
#   region = "eu"
#
#   config_vars {
#     REVERSE_PROXY_PATH = "/arctic-office-projects/testing"
#   }
# }

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
  size     = "free"
}

# # Production dyno
# #
# # This resource implicitly depends on the 'heroku_app.bas-arctic-office-projects-api-prod' resource.
# # This resource relies on the Heroku Terraform provider being previously configured.
# #
# # Heroku source: https://devcenter.heroku.com/articles/dyno-types
# # Terraform source: https://www.terraform.io/docs/providers/heroku/r/formation.html
# resource "heroku_formation" "bas-arctic-office-projects-api-prod" {
#   app      = "${heroku_app.bas-arctic-office-projects-api-prod.name}"
#   type     = "web"
#   quantity = 1
#   size     = "hobby"
# }

# Staging pipeline stage
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

# # Production pipeline stage
# #
# # This resource implicitly depends on the 'heroku_pipeline.bas-arctic-office-projects-api' resource.
# # This resource implicitly depends on the 'heroku_app.bas-arctic-office-projects-api-prod' resource.
# # This resource relies on the Heroku Terraform provider being previously configured.
# #
# # Heroku source: https://devcenter.heroku.com/articles/pipelines#adding-apps-to-a-pipeline
# # Terraform source: https://www.terraform.io/docs/providers/heroku/r/pipeline_coupling.html
# resource "heroku_pipeline_coupling" "bas-arctic-office-projects-api-prod" {
#   app      = "${heroku_app.bas-arctic-office-projects-api-prod.name}"
#   pipeline = "${heroku_pipeline.bas-arctic-office-projects-api.id}"
#   stage    = "production"
# }

