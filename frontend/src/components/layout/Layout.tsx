import { Outlet, Link } from 'react-router-dom'
import { FileText } from 'lucide-react'

export default function Layout() {
    return (
        <div className="min-h-screen flex flex-col">
            <header className="bg-white border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16">
                        <div className="flex">
                            <Link to="/" className="flex-shrink-0 flex items-center">
                                <FileText className="h-8 w-8 text-primary-600" />
                                <span className="ml-2 text-xl font-bold text-gray-900">ResumeFit AI</span>
                            </Link>
                        </div>
                        <div className="flex items-center">
                            <Link to="/login" className="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium">
                                Log in
                            </Link>
                            <Link to="/register" className="ml-4 btn-primary text-sm">
                                Sign up
                            </Link>
                        </div>
                    </div>
                </div>
            </header>

            <main className="flex-1 bg-gray-50">
                <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                    <Outlet />
                </div>
            </main>

            <footer className="bg-white border-t border-gray-200">
                <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                    <p className="text-center text-sm text-gray-500">
                        &copy; {new Date().getFullYear()} ResumeFit AI. All rights reserved.
                    </p>
                </div>
            </footer>
        </div>
    )
}
