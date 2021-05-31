terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }

  backend "azurerm" {
    resource_group_name  = "CreditSuisse1_ChrisCairns_ProjectExercise"
    storage_account_name = "cc1000terraformstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

data "azurerm_resource_group" "main" {
  name = "CreditSuisse1_ChrisCairns_ProjectExercise"
}

provider "azurerm" {
  features {}
}

resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                 = "${var.prefix}-tododbuser-terraform"
  resource_group_name  = data.azurerm_resource_group.main.name
  location             = data.azurerm_resource_group.main.location
  offer_type           = "Standard"
  kind                 = "MongoDB"
  mongo_server_version = "4.0"

  # lifecycle {
  #   prevent_destroy = true
  # }

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-todo_app_terraform"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-cc1000-corndell-todo-app-terraform"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id

  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|cree1000/todo-app:latest"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "AUTHENTICATION_DISABLED"    = var.app-authentication-disabled
    "FLASK_SECRET_KEY"           = var.app-flask-secret-key
    "MONGO_CONNECTION_STRING"    = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "MONGO_DB_NAME"              = azurerm_cosmosdb_mongo_database.main.name
    "OAUTH_API_BASE_URI"         = var.app-oauth-api-base-uri
    "OAUTH_CLIENT_ID"            = var.app-oauth-client-id
    "OAUTH_CLIENT_SECRET"        = var.app-oauth-client-secret
    "OAUTH_PROVIDER_BASE_URI"    = var.app-oauth-provider-base-uri
  }
}
