import { defineStore } from "pinia"
import type { InterfaceUser } from "@/Services/Interfaces"

const AUTH_KEY = "kutlynk_auth"
const TOKEN_KEY = "kutlynk_session_token"

function getStoredUser(): InterfaceUser | null {
    const stored = localStorage.getItem(AUTH_KEY)

    if (!stored) {
        return null
    }

    try {
        return JSON.parse(stored)
    } catch {
        localStorage.removeItem(AUTH_KEY)

        return null
    }
}

function getStoredToken(): string | null {
    return localStorage.getItem(TOKEN_KEY)
}

export const useAuthStore = defineStore("auth", {
    state: () => ({
        user: getStoredUser() as InterfaceUser | null,
        token: getStoredToken() as string | null
    }),

    getters: {
        isAuthenticated: (state): boolean => {
            return state.user !== null && Boolean(state.token)
        }
    },

    actions: {
        authenticate(user: InterfaceUser, token?: string) {
            this.user = user
            this.token = token ?? this.token

            localStorage.setItem(
                AUTH_KEY,
                JSON.stringify(user)
            )

            if (token) {
                localStorage.setItem(TOKEN_KEY, token)
            }
        },

        setToken(token: string | null) {
            this.token = token

            if (token) {
                localStorage.setItem(TOKEN_KEY, token)
            } else {
                localStorage.removeItem(TOKEN_KEY)
            }
        },

        logout() {
            this.user = null
            this.token = null

            localStorage.removeItem(AUTH_KEY)
            localStorage.removeItem(TOKEN_KEY)
        }
    }
})