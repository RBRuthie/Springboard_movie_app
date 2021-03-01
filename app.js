

const APIURL =
'https://api.themoviedb.org/4/discover/movie?sort_by=popularity.desc&';

const IMGPATH = "https://image.tmdb.org/t/p/w1280";
const SEARCHAPI =     "https://api.themoviedb.org/4/search/movie?";

const main = document.getElementById("main");
const form = document.getElementById("form");
const search = document.getElementById("search");

// getting favorite movie list
getMovies(APIURL);

async function getMovies(url) {
  const resp = await fetch(url);
  const respData = await resp.json();

  console.log(respData);

  showMovies(respData.results);
}

function showMovies(movies){
  // clear the screen, previous populated field
  container.innerHTML = "";

  movies.forEach((movie) => {
    // pulling fields from API
    const { poster_path, title, vote_average, overview } = movie;

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




function getClassByRate(vote) {
  if (vote >= 8) {
      return "green";
  } else if (vote >= 5) {
      return "blue";
  } else {
      return "orange";
  }
}





form.addEventListener("submit", (e) => {
  e.preventDefault();

  const searchTerm = search.value;

  if (searchTerm) {
      getMovies(SEARCHAPI + searchTerm);

      search.value = "";
  }
});



