window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};


const deleteVenueBtn = document.querySelector('.delete-venue');
if(deleteVenueBtn)
  deleteVenueBtn.onclick = function(e){
    const venue_id = e.target.dataset['id'];
    fetch('/venues/' + venue_id, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'text/plain'
      }
    })
    .then(function(){
      window.location.href = '/'
    })
    .catch(function(e){
      console.log(e)
    })
  }

const deleteArtistBtn = document.querySelector('.delete-artist');
if(deleteArtistBtn)
  deleteArtistBtn.onclick = function(e){
    const artist_id = e.target.dataset['id'];
    fetch('/artists/' + artist_id, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'text/plain'
      }
    })
    .then(function(){
      window.location.href = '/'
    })
    .catch(function(e){
      console.log(e)
    })
  }