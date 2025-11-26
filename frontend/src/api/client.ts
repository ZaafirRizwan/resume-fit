import axios from 'axios'
import { JobCreate } from '../types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
})

export const api = {
    uploadResume: async (file: File) => {
        const formData = new FormData()
        formData.append('file', file)
        const response = await apiClient.post('/resumes/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
        return response.data
    },

    createJob: async (data: JobCreate) => {
        const response = await apiClient.post('/jobs/', data)
        return response.data
    },

    createAnalysis: async (resumeId: string, jobId: string) => {
        const response = await apiClient.post('/analyses/', {
            resume_id: resumeId,
            job_id: jobId,
        })
        return response.data
    },

    getAnalysis: async (id: string) => {
        const response = await apiClient.get(`/analyses/${id}`)
        return response.data
    },
}
