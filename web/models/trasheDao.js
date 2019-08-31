// @ts-check
const CosmosClient = require('@azure/cosmos').CosmosClient
const debug = require('debug')('trashe:trasheDao')

// For simplicity we'll set a constant partition key
const partitionKey = '0'
class TrasheDao {
  /**
  * Manages reading, from Cosmos DB
  * @param {CosmosClient} cosmosClient
  * @param {string} databaseId
  * @param {string} containerId
  */
  constructor(cosmosClient, databaseId, containerId) {
    this.client = cosmosClient
    this.databaseId = databaseId
    this.collectionId = containerId

    this.database = null
    this.container = null
  }

  async init() {
    debug('Setting up the database...')
    const dbResponse = await this.client.databases.createIfNotExists({
      id: this.databaseId
    })
    this.database = dbResponse.database
    debug('Setting up the database...done!')
    debug('Setting up the container...')
    const coResponse = await this.database.containers.createIfNotExists({
      id: this.collectionId
    })
    this.container = coResponse.container
    debug('Setting up the container...done!')
  }

  async find(querySpec) {
    debug('Querying for items from the database')
    if (!this.container) {
      throw new Error('Collection is not initialized.')
    }
    const {
      resources
    } = await this.container.items.query(querySpec).fetchAll()
    return resources
  }

  async getItem(itemId) {
    debug('Getting an item from the database')
    const {
      resource
    } = await this.container.item(itemId, partitionKey).read()
    return resource
  }
}

module.exports = TrasheDao