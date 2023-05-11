import { writable } from 'svelte/store'

export const auth_token = writable(null)
export const admin_role = writable(false)
export const email_login = writable('')
export const password_login = writable('')
export const email_searched = writable('')
export const uuid_worker = writable('')
export const name = writable('')
export const surname = writable('')
export const entrance_time = writable('')
export const exit_time = writable('')
export const last_is_an_entry = writable(null)
export const logs = writable(null)


export function logout() {
    auth_token.set(null)
    admin_role.set(false)
    email_login.set('')
    password_inserted.set('')
    name.set('')
    surname.set('')
}