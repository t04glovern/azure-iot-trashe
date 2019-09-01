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
      query: "SELECT * FROM root r WHERE r.resolved=@resolved",
      parameters: [
        {
          name: "@resolved",
          value: false
        }
      ]
    };

    const items = await this.trasheDao.find(querySpec);
    res.render("index", {
      title: "Trashe List ",
      trashe: items
    });
  }

  async resolveTrashe(req, res) {
    const resolvedTrashes = Object.keys(req.body);
    const trashes = [];

    resolvedTrashes.forEach(trashe => {
      trashes.push(this.trasheDao.updateItem(trashe));
    });

    await Promise.all(trashes);

    res.redirect("/");
  }
}

module.exports = TrasheList;
