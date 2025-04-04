# RW
#./add_user.sh adm-<user_name> cluster-admin
# RO
#./add_user.sh <user_name> view

#!/bin/bash -x

USER=$1
ROLE=$2
USAGE="USAGE: add_user.sh <username> <cluster-role>\n
Example: brand cluster-admin"
if [[ $USER == "" || $ROLE == "" ]];then
    echo -e $USAGE
    exit 1
fi

# create user
cat << EOF > ${USER}_${ROLE}.yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: $USER
  namespace: kube-system

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: $USER
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: $ROLE
subjects:
  - kind: ServiceAccount
    name: $USER
    namespace: kube-system
---
apiVersion: v1
kind: Secret
metadata:
  name: $USER
  namespace: kube-system
  annotations:
    kubernetes.io/service-account.name: $USER
type: kubernetes.io/service-account-token

EOF
kubectl apply -f ${USER}_${ROLE}.yaml
#kubectl create token $USER --bound-object-kind Secret --bound-object-name $USER --namespace kube-system

# get kubectl config
SERVICE_ACCOUNT_NAME=${USER}
CONTEXT=$(kubectl config current-context)
NAMESPACE=kube-system

NEW_CONTEXT=${USER}
KUBECONFIG_FILE="kubeconfig-${USER}"


SECRET_NAME=$(kubectl get serviceaccount ${SERVICE_ACCOUNT_NAME} \
  --context ${CONTEXT} \
  --namespace ${NAMESPACE} \
  -o jsonpath='{.secrets[0].name}')
#TOKEN_DATA=$(kubectl get secret ${SECRET_NAME} \
#  --context ${CONTEXT} \
#  --namespace ${NAMESPACE} \
#  -o jsonpath='{.data.token}')

TOKEN_DATA=$(kubectl create token $USER --bound-object-kind Secret --bound-object-name $USER --namespace kube-system --duration=99999h)
#TOKEN=$(echo ${TOKEN_DATA} | base64 -d)

TOKEN=$(echo ${TOKEN_DATA})
# Create dedicated kubeconfig
# Create a full copy
kubectl config view --raw > ${KUBECONFIG_FILE}.full.tmp
# Switch working context to correct context
kubectl --kubeconfig ${KUBECONFIG_FILE}.full.tmp config use-context ${CONTEXT}
# Minify
kubectl --kubeconfig ${KUBECONFIG_FILE}.full.tmp \
  config view --flatten --minify > ${KUBECONFIG_FILE}.tmp
# Rename context
kubectl config --kubeconfig ${KUBECONFIG_FILE}.tmp \
  rename-context ${CONTEXT} ${NEW_CONTEXT}
# Create token user
kubectl config --kubeconfig ${KUBECONFIG_FILE}.tmp \
  set-credentials ${CONTEXT}-${NAMESPACE}-token-user \
  --token ${TOKEN}
# Set context to use token user
kubectl config --kubeconfig ${KUBECONFIG_FILE}.tmp \
  set-context ${NEW_CONTEXT} --user ${CONTEXT}-${NAMESPACE}-token-user
# Set context to correct namespace
kubectl config --kubeconfig ${KUBECONFIG_FILE}.tmp \
  set-context ${NEW_CONTEXT} --namespace ${NAMESPACE}
# Flatten/minify kubeconfig
kubectl config --kubeconfig ${KUBECONFIG_FILE}.tmp \
  view --flatten --minify > ${KUBECONFIG_FILE}
# Remove tmp
rm ${KUBECONFIG_FILE}.full.tmp
rm ${KUBECONFIG_FILE}.tmp
rm ${USER}_${ROLE}.yaml