const fetch = require('node-fetch');

async function index(req, res, next) {
  const code = req.query.code;
  if (code) {
    const resp = await fetch(`https://oauth.vk.com/access_token?code=${code}&client_id=7473462&client_secret=FHVipzM41rE4s56agi2L&redirect_uri=http://localhost:3000`);
    const access = await resp.json();
    const accessToken = access.access_token;
    const expires = new Date(Date.now() + +access.expires_in);
    res.cookie('access-token', accessToken, { expires });
  }

  res.render('index', { title: 'HTTP-API | Главная', name: 'index' });
}

module.exports = index;
