import API from "@/Services/Index.serve"
import { BACKEND } from "@/Services/Routes"

import type {
    InterfaceLogIn,
    InterfaceSignUp,
    InterfaceUser
} from "@/Services/Interfaces"

import {
    validateEmail,
    validatePassword,
    validateUserName
} from "@/Services/Utils"

import { useAuthStore } from "@/Stores/Auth.store"

export function serveIsAuthenticated() {
    const auth = useAuthStore()
    const stored = localStorage.getItem('kutlynk_auth')
    return auth.isAuthenticated || Boolean(stored)
}

export async function serveSignUp(data: InterfaceSignUp) {

    const validation_errors = {
        username: "",
        email: "",
        password: ""
    }

    if (!validateUserName(data.username)) {
        validation_errors.username = "Invalid Username!"
    }

    if (!validateEmail(data.email)) {
        validation_errors.email = "Invalid Email!"
    }

    if (!validatePassword(data.password)) {
        validation_errors.password = "Weak Password!"
    }

    const hasErrors = Object.values(
        validation_errors
    ).some(Boolean)

    if (hasErrors) {
        return {
            success: false,
            message: 'Please correct the highlighted fields.',
            validation: validation_errors
        }
    }

    const response = await API<{ id: number; username: string; email: string; token: string }>(
        BACKEND.AUTH.SIGNUP,
        data,
        { method: 'POST' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    const user: InterfaceUser = {
        id: response.data.id,
        username: response.data.username,
        email: response.data.email
    }

    const auth = useAuthStore()
    auth.authenticate(user, response.data.token)

    return {
        success: true,
        message: response.message,
        data: user
    }
}



export async function serveLogIn(data: InterfaceLogIn) {

    const validation_errors = {
        email: "",
        password: ""
    }

    if (!validateEmail(data.email)) {
        validation_errors.email = "Invalid Email!"
    }

    if (!data.password) {
        validation_errors.password = "Password is required!"
    }

    const hasErrors = Object.values(
        validation_errors
    ).some(Boolean)

    if (hasErrors) {
        return {
            success: false,
            message: 'Please correct the highlighted fields.',
            validation: validation_errors
        }
    }

    const response = await API<{ userId: number; token: string }>(
        BACKEND.AUTH.LOGIN,
        data,
        { method: 'POST' }
    )

    if (!response.success) {
        throw new Error(response.message)
    }

    const auth = useAuthStore()
    auth.setToken(response.data.token)

    const userResponse = await API<{ id: number; username: string; email: string }>(
        '/auth/me',
        {},
        { method: 'GET' }
    )

    if (!userResponse.success) {
        throw new Error(userResponse.message)
    }

    auth.authenticate(
        {
            id: userResponse.data.id,
            username: userResponse.data.username,
            email: userResponse.data.email
        },
        response.data.token
    )

    return {
        success: true,
        message: response.message,
        data: userResponse.data
    }
}


