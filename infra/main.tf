terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google-beta" {
  # This file will be created from jenkins secret and will be cleaned up before build finishes.
  credentials = file("expanded-aria-326609-cd7b37395be6.json")

  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_container_cluster" "primary" {
  provider = google-beta
  project = var.project_id
  name     = var.cluster_name
  location = var.region

  # GKE Autopilot. Just a cluster is created and no nodes are created unless a deployment requires it.
  enable_autopilot = true
}
