import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Upload, FileText, ArrowRight, Loader2 } from 'lucide-react'
import { api } from '../api/client'

export default function Home() {
    const navigate = useNavigate()
    const [file, setFile] = useState<File | null>(null)
    const [jobDescription, setJobDescription] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0])
        }
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!file || !jobDescription) {
            setError('Please provide both a resume and a job description.')
            return
        }

        setLoading(true)
        setError('')

        try {
            // 1. Upload Resume
            const resume = await api.uploadResume(file)

            // 2. Create Job
            const job = await api.createJob({
                title: "Job Description", // You might want to extract this or ask user
                raw_text: jobDescription,
            })

            // 3. Start Analysis
            const analysis = await api.createAnalysis(resume.id, job.id)

            // 4. Redirect
            navigate(`/analysis/${analysis.id}`)
        } catch (err) {
            console.error(err)
            setError('An error occurred during analysis. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-extrabold text-gray-900 sm:text-5xl sm:tracking-tight lg:text-6xl">
                    Optimize Your Resume for <span className="text-primary-600">Any Job</span>
                </h1>
                <p className="mt-5 max-w-xl mx-auto text-xl text-gray-500">
                    Upload your resume and a job description to get an instant AI-powered match score and tailored improvement suggestions.
                </p>
            </div>

            <div className="bg-white shadow sm:rounded-lg overflow-hidden">
                <div className="px-4 py-5 sm:p-6">
                    <form onSubmit={handleSubmit} className="space-y-8">
                        {error && (
                            <div className="bg-red-50 border-l-4 border-red-400 p-4">
                                <div className="flex">
                                    <div className="ml-3">
                                        <p className="text-sm text-red-700">{error}</p>
                                    </div>
                                </div>
                            </div>
                        )}

                        <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
                            {/* Resume Upload */}
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Resume (PDF)</label>
                                <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md hover:border-primary-500 transition-colors">
                                    <div className="space-y-1 text-center">
                                        {file ? (
                                            <div className="flex flex-col items-center">
                                                <FileText className="mx-auto h-12 w-12 text-primary-500" />
                                                <p className="text-sm text-gray-900 font-medium">{file.name}</p>
                                                <button
                                                    type="button"
                                                    onClick={() => setFile(null)}
                                                    className="text-xs text-red-600 hover:text-red-800 mt-2"
                                                >
                                                    Remove
                                                </button>
                                            </div>
                                        ) : (
                                            <>
                                                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                                                <div className="flex text-sm text-gray-600">
                                                    <label
                                                        htmlFor="file-upload"
                                                        className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                                                    >
                                                        <span>Upload a file</span>
                                                        <input
                                                            id="file-upload"
                                                            name="file-upload"
                                                            type="file"
                                                            className="sr-only"
                                                            accept=".pdf"
                                                            onChange={handleFileChange}
                                                        />
                                                    </label>
                                                    <p className="pl-1">or drag and drop</p>
                                                </div>
                                                <p className="text-xs text-gray-500">PDF up to 10MB</p>
                                            </>
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Job Description */}
                            <div>
                                <label htmlFor="job-description" className="block text-sm font-medium text-gray-700">
                                    Job Description
                                </label>
                                <div className="mt-1">
                                    <textarea
                                        id="job-description"
                                        name="job-description"
                                        rows={8}
                                        className="input-field h-[184px] resize-none"
                                        placeholder="Paste the job description here..."
                                        value={jobDescription}
                                        onChange={(e) => setJobDescription(e.target.value)}
                                    />
                                </div>
                            </div>
                        </div>

                        <div className="flex justify-center">
                            <button
                                type="submit"
                                disabled={loading}
                                className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="animate-spin -ml-1 mr-3 h-5 w-5" />
                                        Analyzing...
                                    </>
                                ) : (
                                    <>
                                        Analyze Fit
                                        <ArrowRight className="ml-3 -mr-1 h-5 w-5" />
                                    </>
                                )}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}
