variable "nifi_url" {
  description = "URL of the NiFi instance"
  type        = string
  default     = "http://localhost:8080"
}

variable "template_dir" {
  description = "Path to the directory containing NiFi templates"
  type        = string
  default     = "/path/to/your/project/nifi_templates"
}
