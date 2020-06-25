function redirect(req, res, next) {
  res.render('redirect', { title: 'HTTP-API | Redirect' });
}

module.exports = redirect;