import React, { useState, useEffect } from 'react';
import { InputForm } from './components/InputForm';
import { SequencePreview } from './components/SequencePreview';
import { DidacticSequence, SequenceInput } from './types';
import { generateDidacticSequence } from './services/geminiService';
import { GraduationCap, Loader2, RefreshCw, AlertTriangle } from 'lucide-react';

import { Login } from './components/Login';

const initialInput: SequenceInput = {
  grado: '',
  area: '',
  tema: '',
  dba: '',
  sesiones: 2,
  ejeCrese: '',
};

function App() {
  // Auth State
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    return localStorage.getItem('guaimaral_auth') === 'true';
  });

  const [input, setInput] = useState<SequenceInput>(initialInput);
  const [sequence, setSequence] = useState<DidacticSequence | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loadingStep, setLoadingStep] = useState(0);

  const loadingMessages = [
    "Analizando el DBA y contexto...",
    "Diseñando estrategias pedagógicas...",
    "Estructurando actividades paso a paso...",
    "Creando rúbricas de evaluación...",
    "Finalizando documento..."
  ];

  const [lastGenTime, setLastGenTime] = useState(0);

  // 1. Cargar datos guardados al iniciar (Persistencia)
  useEffect(() => {
    const savedInput = localStorage.getItem('guaimaral_input');
    const savedSequence = localStorage.getItem('guaimaral_sequence');
    if (savedInput) {
      try { setInput(JSON.parse(savedInput)); } catch (e) { console.error("Error cargando input", e); }
    }
    if (savedSequence) {
      try { setSequence(JSON.parse(savedSequence)); } catch (e) { console.error("Error cargando sequence", e); }
    }
  }, []);

  // 2. Guardar datos automáticamente cuando cambian
  useEffect(() => {
    localStorage.setItem('guaimaral_input', JSON.stringify(input));
  }, [input]);

  useEffect(() => {
    if (sequence) {
      localStorage.setItem('guaimaral_sequence', JSON.stringify(sequence));
    }
  }, [sequence]);

  const handleLogin = () => {
    setIsAuthenticated(true);
    localStorage.setItem('guaimaral_auth', 'true');
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('guaimaral_auth');
    setSequence(null);
  };

  const handleGenerate = async (refinementConfig?: { instruction: string }) => {
    // 3. Security: Rate Limiting (Anti-Spam)
    const now = Date.now();
    if (now - lastGenTime < 10000 && !refinementConfig) { // Esperar 10s entre generaciones completas
      setError("Por seguridad, espera unos segundos antes de generar una nueva secuencia.");
      return;
    }
    setLastGenTime(now);

    setIsLoading(true);
    setError(null);
    try {
      const result = await generateDidacticSequence(input, refinementConfig?.instruction);
      setSequence(result);
    } catch (err) {
      console.error(err);
      setError(err instanceof Error ? err.message : "No pudimos generar la secuencia.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSequence(null);
    // No borramos input para que no pierda sus datos, solo la secuencia visual.
    // Si quisiera borrar todo: setInput(initialInput);
    localStorage.removeItem('guaimaral_sequence');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleEdit = () => {
    setSequence(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Auth Gate
  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-slate-50 text-gray-900 font-sans pb-20 relative selection:bg-blue-100 selection:text-blue-900">

      {/* Dynamic Background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20"></div>
        <div className="absolute top-0 -left-4 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
        <div className="absolute top-0 -right-4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-8 left-20 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
      </div>

      {/* Header */}
      <header className="relative z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50 sticky top-0 no-print transition-all duration-300 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          <div className="flex items-center gap-4 cursor-pointer group" onClick={handleReset}>
            <div className="bg-gradient-to-br from-blue-600 to-indigo-700 p-2.5 rounded-xl text-white shadow-lg shadow-blue-500/30 group-hover:scale-105 transition-transform duration-300">
              <GraduationCap size={26} />
            </div>
            <div>
              <h1 className="text-2xl font-black text-slate-800 tracking-tight leading-none group-hover:text-blue-700 transition-colors">
                I.E. Guaimaral
              </h1>
              <p className="text-xs text-slate-500 font-bold uppercase tracking-widest mt-0.5">
                Docente AI <span className="text-blue-600">Pro</span>
              </p>
            </div>
          </div>
          <div className="flex items-center gap-6">
            <button
              onClick={handleLogout}
              className="text-sm font-bold text-gray-500 hover:text-red-600 transition-colors hidden md:block"
            >
              Salir
            </button>
            {sequence && (
              <button
                onClick={handleReset}
                className="hidden md:flex items-center gap-2 text-sm font-medium text-slate-500 hover:text-blue-600 transition-colors bg-white/50 px-3 py-1.5 rounded-lg border border-transparent hover:border-gray-200 hover:shadow-sm hover:bg-white"
              >
                <RefreshCw size={16} />
                <span>Nueva Secuencia</span>
              </button>
            )}
            <div className="hidden md:flex items-center gap-2 px-4 py-1.5 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-full shadow-inner">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
              <span className="text-xs font-bold text-blue-800 uppercase tracking-wider">v2.1 Stable</span>
            </div>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

        {/* Error Message */}
        {error && (
          <div className="max-w-4xl mx-auto bg-red-50/90 backdrop-blur border-l-4 border-red-500 p-4 mb-8 rounded-r-xl shadow-lg flex items-center justify-between animate-fade-in-up ring-1 ring-red-100">
            <div className="flex items-center gap-4">
              <div className="bg-white p-2 rounded-full text-red-500 shadow-sm">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" /></svg>
              </div>
              <div>
                <h3 className="text-red-800 font-bold">Algo salió mal</h3>
                <p className="text-red-700 text-sm font-medium mt-0.5">{error}</p>
              </div>
            </div>
            <button onClick={() => setError(null)} className="text-red-400 hover:text-red-600 bg-white/50 hover:bg-white p-2 rounded-full transition-all">✕</button>
          </div>
        )}

        {/* Loading Overlay with Glassmorphism */}
        {isLoading && (
          <div className="fixed inset-0 bg-white/60 backdrop-blur-md z-[100] flex flex-col items-center justify-center p-4 transition-all duration-500">
            <div className="w-full max-w-lg bg-white/80 p-10 rounded-3xl shadow-2xl border border-white/50 text-center relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-purple-50/50 -z-10"></div>

              <div className="relative mb-8 inline-block">
                <div className="absolute inset-0 bg-blue-400 rounded-full animate-ping opacity-20"></div>
                <div className="relative bg-gradient-to-tr from-blue-600 to-indigo-600 p-5 rounded-full text-white shadow-xl shadow-blue-500/40">
                  <Loader2 size={48} className="animate-spin" />
                </div>
              </div>

              <h3 className="text-2xl font-black text-slate-800 mb-3 tracking-tight">Generando Secuencia</h3>
              <div className="h-8 mb-6 flex justify-center items-center">
                <p className="text-indigo-600 font-semibold animate-pulse text-lg">{loadingMessages[loadingStep]}</p>
              </div>

              <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden shadow-inner border border-gray-200">
                <div
                  className="bg-gradient-to-r from-blue-500 to-indigo-600 h-3 rounded-full transition-all duration-700 ease-out relative"
                  style={{ width: `${((loadingStep + 1) / loadingMessages.length) * 100}%` }}
                >
                  <div className="absolute inset-0 bg-white/30 animate-[shimmer_2s_infinite]"></div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Input Form Section */}
        <div className={sequence ? 'hidden' : 'block animate-fade-in-up max-w-5xl mx-auto'}>
          <div className="mb-10 text-center">
            <h2 className="text-4xl md:text-5xl font-black text-slate-800 mb-4 tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-700">
              Diseño Curricular <br className="md:hidden" /><span className="text-blue-600">Inteligente</span>
            </h2>
            <p className="text-slate-500 text-lg md:text-xl max-w-2xl mx-auto leading-relaxed">
              Transforma los estándares del MEN en secuencias didácticas listas para el aula en segundos.
            </p>
          </div>
          <InputForm
            input={input}
            setInput={setInput}
            onGenerate={() => handleGenerate()}
            isLoading={isLoading}
          />
        </div>

        {/* Sequence Preview Section */}
        {sequence && (
          <div className="animate-fade-in-up max-w-6xl mx-auto">
            <div className="mb-8 no-print flex flex-col md:flex-row justify-between items-center gap-4">
              <button
                onClick={handleEdit}
                className="group flex items-center gap-3 px-5 py-2.5 bg-white border border-gray-200 rounded-xl text-slate-600 hover:text-blue-700 hover:border-blue-200 hover:shadow-md transition-all font-semibold"
              >
                <span className="group-hover:-translate-x-1 transition-transform">←</span>
                Editar Parámetros
              </button>
            </div>

            {/* ALERTAS DE INCOHERENCIA - Redesigned */}
            {sequence.alertas_generadas && sequence.alertas_generadas.length > 0 && (
              <div className="mb-8 bg-amber-50 border border-amber-200 rounded-2xl p-6 shadow-sm animate-soft-bounce relative overflow-hidden no-print">
                <div className="absolute top-0 right-0 p-4 opacity-10">
                  <AlertTriangle size={100} className="text-amber-500" />
                </div>
                <div className="flex gap-4 relative z-10">
                  <div className="bg-amber-100 p-3 rounded-xl text-amber-600 h-fit">
                    <AlertTriangle size={24} />
                  </div>
                  <div>
                    <h3 className="text-amber-900 font-bold text-lg mb-2">Ajuste Curricular Automático</h3>
                    <div className="space-y-2">
                      {sequence.alertas_generadas.map((alerta, i) => (
                        <div key={i} className="flex gap-2 text-amber-800 bg-amber-100/50 px-3 py-2 rounded-lg text-sm font-medium border border-amber-200">
                          <span>•</span>
                          <p>{alerta}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            <SequencePreview
              data={sequence}
              input={input}
              onRefine={(instruction) => handleGenerate({ instruction })}
              onReset={handleReset}
            />
          </div>
        )}

      </main>

    </div>
  );
}

export default App;