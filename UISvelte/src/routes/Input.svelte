<script>
    import { 
        email, 
        password_inserted, 
        auth_token, 
        name,
        surname,
        entrance_time,
        last_is_an_entry,
        exit_time,
        logs
    } from './store.js';
    import { SERVER_IP } from './config.js';

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
            entrance_time.set(data.entrance_time)
            exit_time.set(data.exit_time)
            console.log(data)
        })
    }

    async function set_last_is_an_entry(){
        await fetch( SERVER_IP + '/logs/last_is_an_entry', {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            'token': $auth_token
            }
        })
        .then(res => res.json())
        .then(data => {
            last_is_an_entry.set(data.last_is_an_entry)
        })
    }

    async function set_worker_logs(){
        await fetch( SERVER_IP + '/logs', {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json',
            'token': $auth_token
            }
        })
        .then(res => res.json())
        .then(data => {
            logs.set(data.logs)
            console.log(data)
        })
    }

    async function get_worker_data(){
        await set_token()
        if ($auth_token == null) {
            alert('Credenziali errate')
            return
        }
        set_worker_logs()
        await set_worker_data()
        await set_last_is_an_entry()
    }
</script>

<main>
    <h1 class="text-white text-5xl" style="text-align: center;"><b>LOG IN</b></h1>

    <br>
    <p class="text-white text-2xl" style="text-align: center;">
    Inserisci le tue credenziali
    </p>

    <br>
    <div class="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100 text-black">
        <div class="card-body">
            <div class="form-control">
                <label class="label">
                    <span class="label-text"><b>Email</b></span>
                </label>
                <input type="text" placeholder="email" bind:value={$email} class="input input-bordered" />
            </div>
            <div class="form-control">
                <label class="label">
                    <span class="label-text"><b>Password</b></span>
                </label>
                <input type="password" placeholder="password" bind:value={$password_inserted} class="input input-bordered" />
            </div>
            <div class="form-control mt-6">
                <button class="btn btn-primary" on:click={get_worker_data}>Login</button>
            </div>
        </div>
    </div>
</main>