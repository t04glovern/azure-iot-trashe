const TrasheDao = require("../models/trasheDao");

class TrasheList {
  /**
   * Handles the various APIs for displaying and managing trashe
   * @param {TrasheDao} trasheDao
   */
  constructor(trasheDao) {
    this.trasheDao = trasheDao;
  }
  async showTrashe(req, res) {
    const querySpec = {
      query: "SELECT * FROM root r"
    };

    const items = await this.trasheDao.find(querySpec);
    res.render("index", {
      title: "Trashe List ",
      trashe: items
    });
  }
}

module.exports = TrasheList;