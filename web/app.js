const CosmosClient = require('@azure/cosmos').CosmosClient
const config = require('./config')
const TrasheList = require('./routes/trashelist')
const TrasheDao = require('./models/trasheDao')

const express = require('express')
const path = require('path')
const logger = require('morgan')
const cookieParser = require('cookie-parser')
const bodyParser = require('body-parser')

const app = express()

// view engine setup
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'jade')

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
  extended: false
}))
app.use(cookieParser())
app.use(express.static(path.join(__dirname, 'public')))

//Trashe App:
const cosmosClient = new CosmosClient({
  endpoint: config.host,
  key: config.authKey
})
const trasheDao = new TrasheDao(cosmosClient, config.databaseId, config.containerId)
const trasheList = new TrasheList(trasheDao)
trasheDao
  .init(err => {
    console.error(err)
  })
  .catch(err => {
    console.error(err)
    console.error(
      'Shutting down because there was an error setting up the database.'
    )
    process.exit(1)
  })

app.get('/', (req, res, next) => trasheList.showTrashe(req, res).catch(next))
app.post('/resolvetrashe', (req, res, next) =>
  trasheList.resolveTrashe(req, res).catch(next)
)
app.set('view engine', 'jade')

// catch 404 and forward to error handler
app.use(function (req, res, next) {
  const err = new Error('Not Found')
  err.status = 404
  next(err)
})

// error handler
app.use(function (err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message
  res.locals.error = req.app.get('env') === 'development' ? err : {}

  // render the error page
  res.status(err.status || 500)
  res.render('error')
})

module.exports = app
