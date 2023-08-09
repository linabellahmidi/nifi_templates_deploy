provider "null" {
}

resource "null_resource" "kubectl_configure" {
  # This resource will configure kubectl to use the Minikube cluster
  provisioner "local-exec" {
    command = "minikube update-context"
  }
}

resource "null_resource" "get_ns" {
  depends_on = [null_resource.kubectl_configure]
  provisioner "local-exec" {
    command = "kubectl get ns"
  }
}

#resource "null_resource" "change_dir" {\
  #depends_on = [null_resource.get_ns]
  #provisioner "local-exec" {
    #command = "cmd.exe /c cd /d 'C:\\Users\\Achraf OUJJIR\\Desktop\\Nifikop\\nifi_templates_deploy'"
  #}
#}

resource "null_resource" "execute_script" {
  depends_on = [null_resource.kubectl_configure]
  provisioner "local-exec" {
    command = "C:/Python311/python.exe ./works_well/deploy_template.py"
  }
}

resource "null_resource" "finish_msg" {
  depends_on = [null_resource.execute_script]
  provisioner "local-exec" {
    command = "echo 'Terraform finished'"
  }
}