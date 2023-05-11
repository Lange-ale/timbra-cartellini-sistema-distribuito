<script>
    import {
        auth_token,
        email_login,
        password_login,
        email_searched,
        uuid_worker,
        name,
        surname, 
        entrance_time,
        exit_time, 
        admin_role, 
        last_is_an_entry, 
        logs 
    } from './store.js';
    import { SERVER_IP } from './config.js';

    let user_action = null
    let actual_time = Date().toString().split(' ')[4]
    function update_time(){
        actual_time = Date().toString().split(' ')[4]
    }
    setInterval(update_time, 1000)

    async function set_token(){
        let token = null
        await fetch( SERVER_IP + '/token', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: $email_login,
                password: $password_login
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                console.log(data.error)
                return
            }
            auth_token.set(data.token)
            uuid_worker.set(data.uuid_worker)
            console.log(data)
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
            if (data.error) {
                console.log(data.error)
                return
            }
            name.set(data.name)
            surname.set(data.surname)
            entrance_time.set(data.entrance_time)
            exit_time.set(data.exit_time)
            admin_role.set(data.is_admin)
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
            if (data.error) {
                console.log(data.error)
                return
            }
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
            if (data.error) {
                console.log(data.error)
                return
            }
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

    async function timbra(){
        await fetch( SERVER_IP + '/timbra', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'token': $auth_token
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                console.log(data.error)
                return
            }
            console.log(data)
            last_is_an_entry.set(data.is_entry)
            user_action = "Sei " + (data.is_entry ? "entrato" : "uscito") + " alle " + data.time
            set_worker_logs()
        })
    }
</script>

<main class="text-white min-h-1000">
    
            
            <br> <br> <br>
            
            {#if $auth_token == null}
            <div class="hero">
                <div class="hero-content flex-col">
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
                            <input type="text" placeholder="Email" bind:value={$email_login} class="input input-bordered" />
                        </div>
                        <div class="form-control">
                            <label class="label">
                                <span class="label-text"><b>Password</b></span>
                            </label>
                            <input type="password" placeholder="Password" bind:value={$password_login} class="input input-bordered" />
                        </div>
                        <div class="form-control mt-6">
                            <button class="btn btn-primary" on:click={get_worker_data}>Login</button>
                        </div>
                    </div>
                </div>
                </div>
            </div>
            {:else}
            <div class="flex flex-col w-full lg:flex-row">
                <div class="grid flex-grow place-items-center">
                <div class="title text-9xl text-center p-5">
                    { actual_time }
                </div>

                {#if $name != null}
                    <h1 class="title text-5xl text-center p-5">
                        Buongiorno { $name } { $surname }
                    </h1>
                {/if}
                
                {#if user_action==null}
                    {#if $last_is_an_entry == null}
                        <button class="btn loading"> Loading... </button>
                    {:else if $last_is_an_entry}
                        <button class="btn btn-error"
                            on:click={ () => { user_action = "button pressed" }, 
                                       timbra 
                                     }> Timbra uscita </button>
                    {:else}
                        <button class="btn btn-success"  
                            on:click={ () => { user_action = "button pressed" }, 
                                       timbra 
                                     }> Timbra entrata </button>
                    {/if}
                {:else if user_action=="button pressed"}
                    <button class="btn loading"> Loading... </button>
                {:else}
                    <p class="text-2xl text-center p-5"> {user_action} </p>
                {/if}

            </div>


            <div class="grid flex-grow place-items-center">

                {#if $logs != null}
                    <div class="border border-white rounded-lg p-1">
                        <table class="table table-hover table-compact">
                            <thead class="text-primary">
                                <tr>
                                    <th> Azione </th>
                                    <th> Data </th>
                                    <th> Ora </th>
                                </tr>
                            </thead>
                            {#each $logs as log}
                                {#if log.is_entry}
                                    {#if log.time > $entrance_time}
                                        <tr class=" bg-error">
                                            <td> Entrata </td> 
                                            <td> {log.date} </td>
                                            <td> {log.time} </td>
                                        </tr>
                                    {:else}
                                        <tr>
                                            <td> Entrata </td>
                                            <td> {log.date} </td>
                                            <td> {log.time} </td>
                                        </tr>
                                    {/if}
                                {:else}
                                    <tr>
                                        <td> Uscita </td>   
                                        <td> {log.date} </td>
                                        <td> {log.time} </td>
                                    </tr>
                                {/if}
                            {/each}
                        </table>
                    </div>
                {/if}

                </div>
                </div>                
            {/if}
</main>
