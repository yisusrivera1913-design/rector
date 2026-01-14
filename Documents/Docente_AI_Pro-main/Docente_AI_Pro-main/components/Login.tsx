import React, { useState } from 'react';
import { School, UserCircle, Lock, ArrowRight, CheckCircle } from 'lucide-react';

interface LoginProps {
    onLogin: () => void;
}

export const Login: React.FC<LoginProps> = ({ onLogin }) => {
    // Auto-llenado para pruebas rápidas (Solicitado por usuario)
    const [email, setEmail] = useState('docente@guaimaral.edu.co');
    const [password, setPassword] = useState('123456');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError(null);

        // Mock Authentication Logic
        // In a real scenario, this would call an API
        setTimeout(() => {
            // Simular validación: Aceptamos cualquier email que parezca institucional o demo
            if (email && password.length > 3) {
                // Success
                onLogin();
            } else {
                setError("Credenciales inválidas. Inténtalo de nuevo.");
                setIsLoading(false);
            }
        }, 1500);
    };

    return (
        <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 relative overflow-hidden">
            {/* Dynamic Background */}
            <div className="absolute inset-0 pointer-events-none overflow-hidden">
                <div className="absolute -top-20 -left-20 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
                <div className="absolute top-40 -right-20 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
                <div className="absolute -bottom-20 left-1/2 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
            </div>

            <div className="bg-white/80 backdrop-blur-xl w-full max-w-md p-8 rounded-3xl shadow-2xl border border-white/50 relative z-10 animate-fade-in-up ring-1 ring-gray-100">

                <div className="text-center mb-8">
                    <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl mx-auto flex items-center justify-center text-white shadow-lg shadow-blue-500/30 mb-4 transform rotate-3 hover:rotate-0 transition-all duration-500">
                        <School size={40} />
                    </div>
                    <h1 className="text-3xl font-black text-slate-800 tracking-tight">Docente AI <span className="text-blue-600">Pro</span></h1>
                    <p className="text-slate-500 font-medium mt-2">Plataforma de Gestión Académica</p>
                </div>

                <form onSubmit={handleLogin} className="space-y-5">
                    <div className="space-y-1">
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Correo Institucional</label>
                        <div className="relative group">
                            <div className="absolute left-3 top-3.5 text-gray-400 group-focus-within:text-blue-500 transition-colors">
                                <UserCircle size={20} />
                            </div>
                            <input
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="docente@guaimaral.edu.co"
                                className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 outline-none transition-all font-medium text-slate-700"
                            />
                        </div>
                    </div>

                    <div className="space-y-1">
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Contraseña</label>
                        <div className="relative group">
                            <div className="absolute left-3 top-3.5 text-gray-400 group-focus-within:text-blue-500 transition-colors">
                                <Lock size={20} />
                            </div>
                            <input
                                type="password"
                                required
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500 outline-none transition-all font-medium text-slate-700"
                            />
                        </div>
                    </div>

                    {error && (
                        <div className="bg-red-50 text-red-600 text-sm font-bold p-3 rounded-lg flex items-center gap-2 border border-red-100 animate-shake">
                            <span className="bg-red-200 rounded-full p-0.5">✕</span> {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full bg-slate-900 hover:bg-black text-white py-4 rounded-xl font-bold text-lg shadow-xl shadow-slate-900/20 hover:shadow-2xl hover:-translate-y-1 transition-all active:scale-95 flex items-center justify-center gap-2"
                    >
                        {isLoading ? (
                            <span className="animate-pulse">Verificando...</span>
                        ) : (
                            <>
                                Ingresar al Sistema <ArrowRight size={20} />
                            </>
                        )}
                    </button>
                </form>

                <div className="mt-8 pt-6 border-t border-gray-100 text-center">
                    <p className="text-xs text-gray-400 font-medium">
                        Institución Educativa Guaimaral &copy; {new Date().getFullYear()} <br />
                        <span className="text-blue-400">Acceso exclusivo para docentes autorizados</span>
                    </p>
                </div>

            </div>
        </div>
    );
};
