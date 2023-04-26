<script>
import {matricola} from './store.js';  

let visibile = false;

function get_worker_data(){
  fetch('http://localhost:5000/workers/' + $matricola)
    .then((response) => response.json())
    .then(json => {
    console.log(json);
  });
}
function toggle(){
 visibile = !visibile
}
</script>

<main class="min-h-screen" style="background-color: rgb(30 41 59);">
  <div class="hero">
    <div class="hero-body">
      <h1 class="text-white text-5xl">TIMBRA CARTELLINI</h1>

      <p class="text-white">
        Inserisci il numero di matricola
      </p>

      <input type="text" placeholder="Matricola" bind:value={$matricola} />

      <button class="btn btn-primary" on:click={get_worker_data()}>
        LogIn
      </button>

      <p class="text-white"> {$matricola} </p>
    </div>
  </div>
</main>
