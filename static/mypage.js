
const IMGPATH = "https://image.tmdb.org/t/p/w1280";
      

const main = document.getElementById("main");
const form = document.getElementById("form");
const search = document.getElementById("search");


// function to clear the screen from previously populated fields
function colocarPelicula(movies, favorites){
  container.innerHTML = "";

  movies.forEach((movie) => {
    // pulling fields from API
    const { poster_path, title, vote_average, overview, id } = movie;

    const peliculaElemento = document.createElement("div")
    peliculaElemento.classList.add("movie")

    peliculaElemento.innerHTML =
    `
        <img
            src="${IMGPATH + poster_path}"
            alt="${title}"
        />

        <div class="movie-info">
            <a onclick="toggleFavorite(this, '${id}', user_id)" class="btn-star" href="#">
                <i
                   id="star-icon"
                   class="fa-star ${favorites.includes(id) ? 'fa' : 'far'}"
                   title="Click to toggle favorites">
                </i>
            </a>
            <span class="${viewerRatings(vote_average)}">${vote_average}</span>
        </div>

        
        <div class="movie-title"> 
            <h3>${title}</h3>
        </div>

        <div class="overview-my-page">
            <h3>Overview:</h3>
            ${overview}
        </div>

`;

    container.appendChild(peliculaElemento);
});
}

// call function & passing two variables
colocarPelicula(movies, favorites);


// toggle star to add movies to favorite
function toggleFavorite(element, id, user){
 const star = element.getElementsByTagName('i')[0]
 $.ajax({
    url: '/favorite',
    type: star.classList.contains('far') ? 'POST' : 'DELETE',
    data: JSON.stringify({user,movie:id}),
    dataType: 'text',
    contentType: 'application/json',
    success:function(data, status, unused){
      console.log(data)
      if (star.classList.contains('far')) {
        star.classList.remove('far')
        star.classList.add('fa')
        favorites.push(id)
      } else {
        star.classList.remove('fa')
        star.classList.add('far')
        favorites.splice(favorites.indexOf(id), 1)
      }
    }
 })
}


// form eventlistner & if statement for taking term 
// from search bar & matchingquering the API
form.addEventListener("submit", (e) => {
  e.preventDefault();
  
  if (search.value) {
    $.ajax({
        url: '/search',
        type: 'POST',
        data: JSON.stringify({query: search.value}),
        dataType: 'json',
        contentType: 'application/json',
        success:function(data, status, unused){
          colocarPelicula(data.results, favorites);
          search.value = "";
        }
     })
  }
});




// function for movie ratings
function viewerRatings(vote) {
  if (vote >= 8) {
      return "green";
  } else if (vote >= 5) {
      return "blue";
  } else {
      return "orange";
  }
}



