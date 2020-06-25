const index = require('./controllers');
const redirect = require('./controllers/redirect');
const fetchAlbum = require('./controllers/fetcher');

function routes(app) {
  app.get('/', index);

  app.get('/redirect', redirect);

  app.get('/api/fetch', fetchAlbum);

  // Можем объединить разные http методы с одинаковым маршрутом
  // app
  //   .route('/notes')
  //   .get(list)
  //   .post(create);

  // app.get('/notes/:name', item);
}

module.exports = routes;