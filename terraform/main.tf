provider "local" {}

resource "local_file" "example" {
  content  = "DevSecOps Pipeline Working Successfully"
  filename = "success.txt"
}