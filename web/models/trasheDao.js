// @ts-check
const CosmosClient = require('@azure/cosmos').CosmosClient
const debug = require('debug')('trashe:trasheDao')

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

  async updateItem(itemId) {
    debug('Update an item in the database')

    const {
      resource: replaced
    } = await this.container
      .item(itemId, undefined)
      .replace({
        'id': itemId,
        'resolved': true
      })
    return replaced
  }
}

module.exports = TrasheDao
