
const IMGPATH = "https://image.tmdb.org/t/p/w1280";


const main = document.getElementById("main");
const form = document.getElementById("form");
const search = document.getElementById("search");
const starIcon = document.getElementById("fa-star");


// function to clear the screen from previously populatged fields
function showMovies(movies){
  container.innerHTML = "";

  movies.forEach((movie) => {
    // pulling fields from API
    const { poster_path, title, vote_average, overview, favorite } = movie;

    const movieEl = document.createElement("div");
    movieEl.classList.add("movie");

    movieEl.innerHTML =
    `
        <img
            src="${IMGPATH + poster_path}"
            alt="${title}"
        />

        <div class="movie-info">
            <h3>${title}</h3>
            <span class="${getClassByRate
            (vote_average)}">${vote_average}</span>
        </div>

    

        <div class="overview">
            <h3>Overview:</h3>
            ${overview}
        </div>
        `;

        container.appendChild(movieEl);
    });
}

// calling showmovie function
showMovies(movies);


// eventlistner & if statement for taking term 
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
          showMovies(data.results);
          search.value = "";
        }
     })
  }
});



// function for movie ratings
function getClassByRate(vote) {
  if (vote >= 8) {
      return "green";
  } else if (vote >= 5) {
      return "blue";
  } else {
      return "orange";
  }
}

