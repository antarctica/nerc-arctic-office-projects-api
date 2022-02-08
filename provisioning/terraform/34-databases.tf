#
# This file is used to define data storage resources for applications

# Staging instance database
#
# This resource implicitly depends on the "heroku_app.bas-arctic-office-projects-api-stage" resource.
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/addon.html
resource "heroku_addon" "database-stage" {
  app  = "${heroku_app.bas-arctic-office-projects-api-stage.name}"
  plan = "heroku-postgresql:hobby-basic"
}

# Production instance database
#
# This resource implicitly depends on the "heroku_app.bas-arctic-office-projects-api-prod" resource.
# This resource relies on the Heroku Terraform provider being previously configured.
#
# Heroku source: https://devcenter.heroku.com/articles/heroku-postgresql#provisioning-heroku-postgres
# Terraform source: https://www.terraform.io/docs/providers/heroku/r/addon.html
resource "heroku_addon" "database-prod" {
  app  = "${heroku_app.bas-arctic-office-projects-api-prod.name}"
  plan = "heroku-postgresql:hobby-dev"
}
