<script>
    // Import our global CSS
    import "$lib/global.css"

    import { admin_role, auth_token, logout } from './store.js';
</script>

<div class="navbar bg-base-200">
    <div class="flex-none">
        <a href="/" class="btn btn-ghost text-xl"> TIMBRA CARTELLINI </a>
    </div>
    {#if $admin_role}
        <div class="flex-none">
            <a href="/" class="btn btn-ghost text-xl"> admin </a>
        </div>
    {/if}
    <div class="flex-1"></div>
    {#if $auth_token}
        <div class="flex-none">
            <button class="btn btn-ghost text-l" on:click={ logout }>
                <img src="https://img.icons8.com/ios-filled/50/000000/logout-rounded-left.png"/>
            </button>
        </div>
    {/if}
</div>

<slot></slot>