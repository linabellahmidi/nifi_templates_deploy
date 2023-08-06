variable "nifi_url" {
  description = "URL of the NiFi instance"
  type        = string
  default     = "http://localhost:8080"  # Hard-coded NiFi URL
}

variable "nifi_token" {
  description = "Authentication token for NiFi REST API"
  type        = string
  default     = "your-nifi-token"  # Hard-coded NiFi token
}

variable "template_dir" {
  description = "Path to the directory containing NiFi templates"
  type        = string
  default     = "/path/to/your/project/nifi_templates"  # Hard-coded template directory
}
