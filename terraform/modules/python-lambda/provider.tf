terraform {
  required_providers {
    archive = {
      source = "hashicorp/archive"
      version = "2.4.2"
    }
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.16"
    }
    null = {
      source = "hashicorp/null"
      version = "3.2.2"
    }
    random = {
      source = "hashicorp/random"
      version = "3.6.2"
    }
  }
}

/*
provider "archive" {}

provider "aws" {
  region = "us-west-2"
}

provider "null" {}

provider "random" {}
*/