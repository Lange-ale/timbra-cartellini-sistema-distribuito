import { writable } from 'svelte/store'

export const auth_token = writable(null)
export const admin_role = writable(true)
export const email = writable('')
export const password_inserted = writable('')
export const name = writable('')
export const surname = writable('')
export const entrance_time = writable('')
export const exit_time = writable('')
export const last_is_an_entry = writable(null)
export const logs = writable([])


export function logout() {
    auth_token.set(null)
    admin_role.set(false)
    email.set('')
    password_inserted.set('')
    name.set('')
    surname.set('')
}

