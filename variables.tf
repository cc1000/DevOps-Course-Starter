variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}

variable "app-authentication-disabled" { default = true }
variable "app-flask-secret-key" {}
variable "app-oauth-api-base-uri" {}
variable "app-oauth-client-id" {}
variable "app-oauth-client-secret" {}
variable "app-oauth-provider-base-uri" {}
