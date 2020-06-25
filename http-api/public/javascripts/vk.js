const accessToken = getCookie('access-token');
if (!accessToken || accessToken === 'undefined') {
  document.location.href = '/redirect';
}

const downloadButton = document.getElementById('downloadButton');
const albumInput = document.getElementById('albumInput');

let album = '';

downloadButton.addEventListener('click', async (e) => {
  e.preventDefault();

  album = albumInput.value;

  const match = Array.from(album.matchAll(/https?:\/\/(www.)?vk.com\/album(-?\d+)_(\d+)/ig));

  if (!match.length) {
    return alert('Неверно введенная ссылка!');
  }

  let [ ,,ownerId, albumId ] = match[0];

  albumId = albumId === '0' ? 'profile' : albumId;
  albumId = albumId === '00' ? 'wall' : albumId;
  albumId = albumId === '000' ? 'saved' : albumId;

  const archiveRes = await fetch(`/api/fetch?ownerId=${ownerId}&albumId=${albumId}`);
  const archiveBlob = await archiveRes.blob();
  saveAs(archiveBlob, 'album.zip');
});