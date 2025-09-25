import React from 'react';
import { HeartIcon } from './icons/HeroIcons';

interface LoginPageProps {
  onLogin: () => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Left Pane (Branding) */}
      <div className="hidden lg:flex w-1/2 bg-blue-500 items-center justify-center p-12 text-white flex-col relative overflow-hidden">
        <div 
          className="absolute top-0 left-0 w-full h-full bg-cover bg-center opacity-10" 
          style={{ backgroundImage: "url('https://images.unsplash.com/photo-1584982233989-54c2a87c1266?q=80&w=2574&auto=format&fit=crop')" }}
        ></div>
        <div className="relative z-10 text-center">
            <HeartIcon className="h-24 w-24 text-white mx-auto" />
            <h1 className="mt-4 text-4xl font-bold tracking-tight">AYUSH EMR</h1>
            <p className="mt-2 text-lg opacity-80">Integrating Modern Care with Ancient Wisdom</p>
        </div>
      </div>

      {/* Right Pane (Login Form) */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12">
        <div className="w-full max-w-md">
          <div className="lg:hidden flex justify-center mb-8">
             <HeartIcon className="h-12 w-12 text-blue-500" />
          </div>
          <h2 className="text-3xl font-bold text-slate-800 mb-2">Welcome Back</h2>
          <p className="text-slate-500 mb-8">Sign in to continue to your dashboard.</p>

          <form onSubmit={(e) => { e.preventDefault(); onLogin(); }}>
            <div className="space-y-6">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-600">
                  Email Address
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  defaultValue="dr.sharma@ayush.clinic"
                  className="mt-1 block w-full px-4 py-3 border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white text-slate-900"
                  placeholder="you@example.com"
                  required
                  aria-label="Email Address"
                />
              </div>

              <div>
                <label htmlFor="password"className="block text-sm font-medium text-slate-600">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  defaultValue="password"
                  className="mt-1 block w-full px-4 py-3 border border-slate-300 rounded-md shadow-sm placeholder-slate-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white text-slate-900"
                  placeholder="••••••••"
                  required
                  aria-label="Password"
                />
              </div>
            </div>

            <div className="flex items-center justify-between mt-6">
                <div className="flex items-center">
                    <input id="remember-me" name="remember-me" type="checkbox" className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded" />
                    <label htmlFor="remember-me" className="ml-2 block text-sm text-slate-900">
                        Remember me
                    </label>
                </div>

                <div className="text-sm">
                    <a href="#" className="font-medium text-blue-600 hover:text-blue-500">
                        Forgot your password?
                    </a>
                </div>
            </div>


            <div className="mt-8">
              <button
                type="submit"
                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
              >
                Sign In
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;