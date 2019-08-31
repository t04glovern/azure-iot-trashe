# CosmosDB Webapp

## CosmosDB Deploy

```bash
cd templates/cosmos-db
./deploy.sh

# Your subscription ID can be looked up with the CLI using: az account show --out json
# Enter your subscription ID:
XXXXXXX-XXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXX

# Enter a resource group name
azure-iot-trashe

# Enter a name for this deployment:
azure-iot-trashe-cosmos-db

# You can lookup locations with the CLI using: az account list-locations
# Enter resource group location:
australiasoutheast
```

### Setup Application

Retrieve the connection string that will be used to connect to CosmosDB

*NOTE:* The account name was passed in as a parameter in [templates/cosmos-db/parameters.json](../templates/cosmos-db/parameters.json])

```bash
# Get the connection string for API account
az cosmosdb list-connection-strings \
    --name "trashe" \
    --resource-group "azure-iot-trashe"
```

Make a cope of `web/config.js.example` to `web/config.js` and update the fields with the data from your connection string query

```javascript
const config = {};

config.host = process.env.HOST || "https://trashe.documents.azure.com";
config.authKey = process.env.AUTH_KEY || "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
config.databaseId = "TrasheList";
config.containerId = "Items";

if (config.host.includes("https://localhost:")) {
  console.log("Local environment detected");
  console.log("WARNING: Disabled checking of self-signed certs. Do not have this code in production.");
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
  console.log(`Go to http://localhost:${process.env.PORT || '3000'} to try the sample.`);
}

module.exports = config;
```

### Run Web App

```bash
npm install
npm run start
```

## Attribution

* [Tutorial: Build a Node.js web app using the JavaScript SDK to manage a SQL API account in Azure Cosmos DB](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-nodejs-application)
