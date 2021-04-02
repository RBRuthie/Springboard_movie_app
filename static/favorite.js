
const IMGPATH = "https://image.tmdb.org/t/p/w1280"


const main = document.getElementById("main")
const form = document.getElementById("form")


// function to clear the screen from previously populatged fields
function colocarPelicula(movies){
  container.innerHTML = "";
  movies.forEach((movie) => {
    // pulling fields from API
    const { poster_path, title, vote_average, overview, id } = movie;

    const peliculaElemento = document.createElement("div");
    peliculaElemento.classList.add("movie");

    peliculaElemento.innerHTML =
    `
        <img
            src="${IMGPATH + poster_path}"
            alt="${title}"
        />

        <div class="movie-info">
          <span class="${viewerRatings
          (vote_average)}">${vote_average}</span>
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

// calling the function
colocarPelicula(favorites)


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