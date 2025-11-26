import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api/client'
import { CheckCircle, XCircle, AlertTriangle, Loader2 } from 'lucide-react'

import { Analysis, SkillMatch } from '../types'

export default function AnalysisResult() {
    const { id } = useParams<{ id: string }>()
    const [analysis, setAnalysis] = useState<Analysis | null>(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        if (!id) return

        const pollAnalysis = async () => {
            try {
                const data = await api.getAnalysis(id)
                setAnalysis(data)

                if (data.status === 'COMPLETED' || data.status === 'FAILED') {
                    setLoading(false)
                } else {
                    // Continue polling
                    setTimeout(pollAnalysis, 2000)
                }
            } catch (err) {
                console.error(err)
                setError('Failed to load analysis results.')
                setLoading(false)
            }
        }

        pollAnalysis()
    }, [id])

    if (loading && (!analysis || analysis.status !== 'COMPLETED')) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
                <Loader2 className="h-12 w-12 text-primary-600 animate-spin mb-4" />
                <h2 className="text-xl font-semibold text-gray-900">Analyzing your resume...</h2>
                <p className="text-gray-500 mt-2">This usually takes about 10-20 seconds.</p>
            </div>
        )
    }

    if (error || analysis?.status === 'FAILED') {
        return (
            <div className="text-center py-12">
                <XCircle className="mx-auto h-12 w-12 text-red-500" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">Analysis Failed</h3>
                <p className="mt-1 text-sm text-gray-500">{error || analysis?.error_message || 'Unknown error'}</p>
            </div>
        )
    }

    if (!analysis) return null

    const { match_score, raw_result_json } = analysis
    const { matched_skills, missing_skills, explanation } = raw_result_json || {}

    return (
        <div className="space-y-8">
            {/* Header Section */}
            <div className="bg-white shadow sm:rounded-lg p-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900">Analysis Results</h2>
                        <p className="text-sm text-gray-500">Analysis ID: {id}</p>
                    </div>
                    <div className="flex items-center">
                        <div className="relative h-24 w-24 flex items-center justify-center">
                            <svg className="h-full w-full transform -rotate-90" viewBox="0 0 36 36">
                                <path
                                    className="text-gray-200"
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="3"
                                />
                                <path
                                    className={`${(match_score || 0) >= 80 ? 'text-green-500' : (match_score || 0) >= 50 ? 'text-yellow-500' : 'text-red-500'
                                        }`}
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="3"
                                    strokeDasharray={`${match_score || 0}, 100`}
                                />
                            </svg>
                            <div className="absolute flex flex-col items-center">
                                <span className="text-2xl font-bold text-gray-900">{Math.round(match_score || 0)}%</span>
                                <span className="text-xs text-gray-500">Match</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Explanation */}
            <div className="bg-white shadow sm:rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">AI Insights</h3>
                <div className="prose max-w-none text-gray-500">
                    <p>{explanation}</p>
                </div>
            </div>

            {/* Skills Breakdown */}
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                {/* Matched Skills */}
                <div className="bg-white shadow sm:rounded-lg p-6">
                    <h3 className="text-lg font-medium text-green-700 mb-4 flex items-center">
                        <CheckCircle className="h-5 w-5 mr-2" />
                        Matched Skills
                    </h3>
                    <ul className="space-y-3">
                        {matched_skills?.map((skill: SkillMatch, idx: number) => (
                            <li key={idx} className="flex items-center justify-between text-sm">
                                <span className="font-medium text-gray-900 capitalize">{skill.job_skill}</span>
                                <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full text-xs">
                                    {skill.score ? Math.round(skill.score) : 0}% Match
                                </span>
                            </li>
                        ))}
                        {(!matched_skills || matched_skills.length === 0) && (
                            <p className="text-sm text-gray-500">No direct matches found.</p>
                        )}
                    </ul>
                </div>

                {/* Missing Skills */}
                <div className="bg-white shadow sm:rounded-lg p-6">
                    <h3 className="text-lg font-medium text-red-700 mb-4 flex items-center">
                        <AlertTriangle className="h-5 w-5 mr-2" />
                        Missing / Weak Skills
                    </h3>
                    <ul className="space-y-3">
                        {missing_skills?.map((skill: SkillMatch, idx: number) => (
                            <li key={idx} className="flex items-center justify-between text-sm">
                                <span className="font-medium text-gray-900 capitalize">{skill.job_skill}</span>
                                <span className={`px-2 py-1 rounded-full text-xs ${skill.type === 'must_have' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                                    }`}>
                                    {skill.type === 'must_have' ? 'Critical' : 'Bonus'}
                                </span>
                            </li>
                        ))}
                        {(!missing_skills || missing_skills.length === 0) && (
                            <p className="text-sm text-gray-500">No missing skills detected!</p>
                        )}
                    </ul>
                </div>
            </div>
        </div>
    )
}
