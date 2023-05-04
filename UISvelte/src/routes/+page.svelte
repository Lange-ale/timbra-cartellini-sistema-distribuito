<script>
    import { 
        auth_token, 
        name, 
        surname, 
        last_is_an_entry, 
        entrance_time, 
        exit_time, 
        logs 
    } from './store.js';
    import { SERVER_IP } from './config.js';
    import Input from './Input.svelte';

    let user_action = null
    let actual_time = Date().toString().split(' ')[4]
    function update_time(){
        actual_time = Date().toString().split(' ')[4]
    }
    setInterval(update_time, 1000)


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
            console.log(data)
            last_is_an_entry.set(data.is_entry)
            user_action = "Sei " + (data.is_entry ? "entrato" : "uscito") + " alle " + data.time
        })

    }
</script>

<main class="text-white">
    <div class="hero">
        <div class="hero-content flex-col lg:flex-row-reverse">
            
            <br> <br> <br>
            
            {#if $auth_token == null}
                <Input />
            {:else}
                <div class="title text-9xl text-center p-5">
                    { actual_time }
                </div>


                <h1 class="title text-5xl text-center p-5">
                    Buongiorno { $name } { $surname }
                </h1>
                
                {#if user_action==null}
                    {#if $last_is_an_entry == null}
                        <button class="btn loading min-w-full"> Loading... </button>
                    {:else if $last_is_an_entry}
                        <button class="btn btn-error min-w-full"
                            on:click={ () => { user_action = "button pressed" }, 
                                       timbra 
                                     }> Timbra uscita </button>
                    {:else}
                        <button class="btn btn-success min-w-full"  
                            on:click={ () => { user_action = "button pressed" }, 
                                       timbra 
                                     }> Timbra entrata </button>
                    {/if}
                {:else if user_action=="button pressed"}
                    <button class="btn loading"> Loading... </button>
                {:else}
                    <p class="text-2xl text-center p-5"> {user_action} </p>
                {/if}

                <div class="border border-white rounded-lg p-1">
                    <table class="table table-hover table-compact">
                        <thead class="text-secondary">
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
</main>
