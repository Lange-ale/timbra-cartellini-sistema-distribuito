<script>
import { 
  email, 
  password_inserted, 
  auth_token, 
  name,
  surname
  } from './store.js';
import { SERVER_IP } from './config.js';

let visibile = false;

async function set_token(){
  let token = null
  await fetch( SERVER_IP + '/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: $email,
      password: $password_inserted
    })
  })
  .then(res => res.json())
  .then(data => {
    auth_token.set(data.token)
  })
  .catch(err => console.log(err))
}

async function set_worker_data(){
  await fetch( SERVER_IP + '/worker', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'token': $auth_token
    }
  })
  .then(res => res.json())
  .then(data => {
    name.set(data.name)
    surname.set(data.surname)
    console.log(data)
  })
}

async function get_worker_data(){
  await set_token()
  if ($auth_token == null) {
    visibile = false
    alert('Credenziali errate')
    return
  }
  await set_worker_data()
  visibile = true
}
  
</script>

<main class="min-h-screen" style="background-color: rgb(30 41 59);">
  <div class="hero">
    <div class="hero-body">
      <h1 class="text-white text-5xl">TIMBRA CARTELLINI</h1>

      <p class="text-white">
        Inserisci il numero di matricola
      </p>

      <p>
        <input type="text" placeholder="Email" bind:value={$email} />
        <input type="password" placeholder="Password" bind:value={$password_inserted} />
      <button class="btn btn-primary" on:click={get_worker_data}>
        LogIn
      </button>
      </p>

      {#if visibile}
        <p class="text-white"> {$name} {$surname} </p>
      {/if}

    </div>
  </div>
</main>
