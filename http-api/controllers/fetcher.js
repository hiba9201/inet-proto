const fetch = require('node-fetch');
const JSZip = require('jszip');





async function fetchAlbum(req, res, next) {
  const sizes = { 's': 0, 'm': 1, 'x': 2, 'y': 3, 'z': 4, 'w': 5 };
  let links = [];
  let offset = 0;
  let count = Infinity;
  let lastJobIndex = 0;
  let countResult = 0;
  let accessToken = '';

  accessToken = req.cookies['access-token'];

  if (!accessToken) {
    return res.redirect('/redirect');
  }

  const ownerId = req.query.ownerId;
  let albumId = req.query.albumId;

  albumId = albumId === '0' ? 'profile' : albumId;
  albumId = albumId === '00' ? 'wall' : albumId;
  albumId = albumId === '000' ? 'saved' : albumId;


  while (offset < count) {
    await fetchPhotos(ownerId, albumId);
  }

  generateZIP(res);

  async function fetchPhotos(ownerId, albumId) {
    try {
      const res = await fetch(`https://api.vk.com/method/photos.get?owner_id=${ownerId}&album_id=${albumId}&photo_sizes=1&access_token=${accessToken}&offset=${offset}&count=1000&v=5.103`);
      const photos = await res.json();

      offset += 1000;
      count = photos.response.count;
      photos.response.items.forEach(item => {
        const size = item.sizes.reduce((acc, img) => {
          return sizes[img.type] > sizes[acc] ? img.type : acc;
        }, 's');

        links.push(item.sizes.filter(s => s.type === size)[0].url);
      });
    } catch (e) {
      console.log(e)
    }
  }

  async function generateZIP(res) {
    const zip = new JSZip();

    for (let i = 0; i < 100; i++) {
      downloadAndAppend(links[lastJobIndex++], zip, res);
    }
  }

  async function downloadAndAppend(url, zip, res) {
    const filename = url.slice(url.lastIndexOf('/') + 1);

    let imgResponse;
    try {
      imgResponse = await fetch(url);
      const imgData = await imgResponse.blob();
      zip.file(filename, imgData.arrayBuffer(), { binary: true });
    } catch (e) {
      return await downloadAndAppend(url, zip, res);
    }

    countResult++;
    console.log(countResult + '/' + links.length);

    if (countResult === links.length) {
      console.log('Загрузка изображений завершена. Начинается архивация');
      const content = await zip.generateAsync({ type: 'arraybuffer' }, (meta) => {
        console.log(Math.floor(meta.percent) + '%');
      });

      return res.send(Buffer.from(content));
    }

    if (lastJobIndex < links.length) {
      await downloadAndAppend(links[lastJobIndex++], zip, res);
    }
  }
}


module.exports = fetchAlbum;