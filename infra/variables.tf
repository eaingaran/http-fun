variable "project_id" {
  description = "Name of the Project"
  default = "expanded-aria-326609"
}
variable "cluster_name" {
  description = "The name for the GKE cluster"
  default     = "autopilot-cluster-1"
}
variable "region" {
  description = "The region to host the cluster in"
  default     = "us-central1"
}
variable "zone" {
  description = "The region to host the cluster in"
  default     = "us-central1-c"
}
