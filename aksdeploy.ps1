# Generate a random number
$RAND = Get-Random

# Set it as an environment variable
$env:RAND = $RAND

# Print the random resource identifier
Write-Output "Random resource identifier will be: $RAND"

# Set Location
$env:LOCATION = "uksouth"
Write-Output "Location set to: $env:LOCATION"

# Create a resource group name using the random number
$env:RG_NAME = "myresourcegroup$RAND"
Write-Output "Resource group name: $env:RG_NAME"

# CREATE THE RESOURCE GROUP FIRST! (This was missing)
az group create --name $env:RG_NAME --location $env:LOCATION
Write-Output "Resource group $env:RG_NAME created"

# Setup AKS Cluster
$env:AKS_NAME = "myakscluster$RAND"
Write-Output "AKS cluster name: $env:AKS_NAME"

# Get the latest Kubernetes version available in the region
#env:K8S_VERSION=$(az aks get-versions -l $env:LOCATION --query "orchestrators[?default==\`$true\`].orchestratorVersion | [0]" -o tsv)

$env:K8S_VERSION=$(az aks get-versions -l $env:LOCATION `
--query "values[?isDefault==``true``].version | [0]" `
-o tsv)
Write-Output "Kubernetes version set to: $env:K8S_VERSION"

# create aks cluster
az aks create `
--resource-group $env:RG_NAME `
--name $env:AKS_NAME `
--location $env:LOCATION `
--tier standard `
--kubernetes-version $env:K8S_VERSION `
--os-sku AzureLinux `
--nodepool-name systempool `
--node-count 3 `
--load-balancer-sku standard `
--network-plugin azure `
--network-plugin-mode overlay `
--network-dataplane cilium `
--network-policy cilium `
--enable-managed-identity `
--enable-workload-identity `
--enable-oidc-issuer `
--enable-acns `
--generate-ssh-keys
Write-Output "AKS Cluster $env:AKS_NAME created successfully in resource group $env:RG_NAME"

# Connect to the cluster
az aks get-credentials `
--resource-group $env:RG_NAME `
--name $env:AKS_NAME `
--overwrite-existing
Write-Output "Connected to AKS Cluster $env:AKS_NAME"

# add user nodepool
az aks nodepool add `
--resource-group $env:RG_NAME `
--cluster-name $env:AKS_NAME `
--mode User `
--name userpool `
--node-count 1
Write-Output "User nodepool added to AKS Cluster $env:AKS_NAME"

# taint the system nodepool
az aks nodepool update `
--resource-group $env:RG_NAME `
--cluster-name $env:AKS_NAME `
--name systempool `
--node-taints CriticalAddonsOnly=true:NoSchedule
Write-Output "System nodepool tainted in AKS Cluster $env:AKS_NAME"

# Enable Key Vault integration in AKS
az aks enable-addons `
  --addons azure-keyvault-secrets-provider `
  --resource-group $env:RG_NAME `
  --name $env:AKS_NAME
Write-Output "Azure Key Vault Secrets Provider addon enabled in AKS Cluster $env:AKS_NAME"

# Generate a short random name (globally unique)
$env:KV_NAME = "ft-kv-$(Get-Random -Minimum 1000 -Maximum 9999)"
Write-Output "Key Vault name: $env:KV_NAME"

az keyvault create --name $env:KV_NAME `
  --resource-group $env:RG_NAME `
  --location $env:LOCATION
Write-Output "Azure Key Vault $env:KV_NAME created in resource group $env:RG_NAME"

# Get the Key Vault addon identity
$env:IDENTITY_CLIENT_ID = az aks show `
  --resource-group $env:RG_NAME `
  --name $env:AKS_NAME `
  --query "addonProfiles.azureKeyvaultSecretsProvider.identity.clientId" `
  -o tsv

Write-Output "Identity Client ID: $env:IDENTITY_CLIENT_ID"

# Get Key Vault scope
$env:KV_SCOPE = az keyvault show `
  --name $env:KV_NAME `
  --query "id" `
  -o tsv

# Assign Key Vault Secrets User role to the managed identity
az role assignment create `
  --role "Key Vault Secrets User" `
  --assignee $env:IDENTITY_CLIENT_ID `
  --scope $env:KV_SCOPE

Write-Output "✅ Permissions granted to managed identity"

# Get your Azure tenant ID
$env:TENANT_ID = az account show --query "tenantId" -o tsv
Write-Output "Tenant ID: $env:TENANT_ID"

az keyvault secret set --vault-name $env:KV_NAME `
  --name "DATABASE-URL" `
  --value "your-url-here"

az keyvault secret set --vault-name $env:KV_NAME `
  --name "AZURE-AI-API-KEY" `
  --value "your-key-here"

az keyvault secret set `
  --vault-name $KV_NAME `
  --name "POSTGRES-PASSWORD" `
  --value "your-url-here"

az keyvault secret set `
  --vault-name $env:KV_NAME `
  --name "AZURE-AI-API-KEY" `
  --value "your-url-here"

az keyvault secret set `
  --vault-name $env:KV_NAME `
  --name "AZURE-OPENAI-KEY" `
--value "your-url-here"

az keyvault secret set `
  --vault-name $env:KV_NAME `
  --name "AZURE-SEARCH-API-KEY" `
  --value "your-url-here"

Write-Output "✅ Key Vault $env:KV_NAME created with secrets"

# Create the secret-provider.yaml with your actual values
@"
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: finance-tracker-secrets-provider
  namespace: default
spec:
  provider: azure
  parameters:
    usePodIdentity: "false"
    useVMManagedIdentity: "true"
    userAssignedIdentityID: "$env:IDENTITY_CLIENT_ID"
    keyvaultName: "$env:KV_NAME"
    tenantId: "$env:TENANT_ID"
    objects: |
      array:
        - |
          objectName: DATABASE-URL
          objectType: secret
        - |
          objectName: POSTGRES-PASSWORD
          objectType: secret
        - |
          objectName: AZURE-AI-API-KEY
          objectType: secret
        - |
          objectName: AZURE-OPENAI-KEY
          objectType: secret
        - |
          objectName: AZURE-SEARCH-API-KEY
          objectType: secret
  secretObjects:
  - secretName: finance-tracker-secrets
    type: Opaque
    data:
    - objectName: DATABASE-URL
      key: DATABASE_URL
    - objectName: POSTGRES-PASSWORD
      key: POSTGRES_PASSWORD
    - objectName: AZURE-AI-API-KEY
      key: AZURE_AI_API_KEY
    - objectName: AZURE-OPENAI-KEY
      key: AZURE_OPENAI_KEY
    - objectName: AZURE-SEARCH-API-KEY
      key: AZURE_SEARCH_API_KEY
"@ | Out-File -FilePath "k8s/secret-provider.yaml" -Encoding UTF8

Write-Output "✅ SecretProviderClass YAML created"