terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">= 2.49"
        }
    }
}

provider "azurerm" {
    features {}
}

data "azurerm_resource_group" "main" {
    name = "CreditSuisse1_ChrisCairns_ProjectExercise"
    # location = "uksouth"
}

resource "azurerm_app_service_plan" "main" {
    name = "terraformed-asp"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    kind = "Linux"
    reserved = true

    sku {
        tier = "Basic"
        size = "B1"
    }
}

resource "azurerm_app_service" "main" {
    name = "cc1000-corndell-todo-app-terraform"
    location = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    app_service_plan_id = azurerm_app_service_plan.main.id

    site_config {
        app_command_line = ""
        linux_fx_version = "DOCKER|appsvcsample/pythonhelloworld:latest"
    }

    app_settings = {
        "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    }
}