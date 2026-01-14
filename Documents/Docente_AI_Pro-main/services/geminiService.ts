import { GoogleGenerativeAI, SchemaType } from "@google/generative-ai";
import { SequenceInput, DidacticSequence } from "../types";

const responseSchema: any = {
  type: SchemaType.OBJECT,
  properties: {
    tema_principal: { type: SchemaType.STRING },
    titulo_secuencia: { type: SchemaType.STRING, description: "Un título creativo y formal para la secuencia." },
    descripcion_secuencia: { type: SchemaType.STRING, description: "Resumen curricular de qué se aprenderá." },
    objetivo_aprendizaje: { type: SchemaType.STRING },
    contenidos: {
      type: SchemaType.ARRAY,
      items: { type: SchemaType.STRING }
    },
    competencias_men: { type: SchemaType.STRING },
    estandar: { type: SchemaType.STRING },
    metodologia: { type: SchemaType.STRING },
    corporiedad_adi: { type: SchemaType.STRING, description: "Estrategias para el desarrollo corporal y emocional" },
    actividades: {
      type: SchemaType.ARRAY,
      items: {
        type: SchemaType.OBJECT,
        properties: {
          sesion: { type: SchemaType.NUMBER },
          descripcion: { type: SchemaType.STRING },
          materiales: { type: SchemaType.ARRAY, items: { type: SchemaType.STRING } },
          tiempo: { type: SchemaType.STRING },
          imprimibles: { type: SchemaType.STRING, description: "Descripción DETALLADA del contenido de las fichas, guías o material gráfico que el docente debe imprimir para esta sesión." }
        },
        required: ["sesion", "descripcion", "materiales", "tiempo", "imprimibles"]
      }
    },
    rubrica: {
      type: SchemaType.ARRAY,
      items: {
        type: SchemaType.OBJECT,
        properties: {
          criterio: { type: SchemaType.STRING },
          basico: { type: SchemaType.STRING },
          satisfactorio: { type: SchemaType.STRING },
          avanzado: { type: SchemaType.STRING },
          retroalimentacion: { type: SchemaType.STRING }
        },
        required: ["criterio", "basico", "satisfactorio", "avanzado", "retroalimentacion"]
      }
    },
    evaluacion: {
      type: SchemaType.ARRAY,
      items: {
        type: SchemaType.OBJECT,
        properties: {
          pregunta: { type: SchemaType.STRING },
          tipo: { type: SchemaType.STRING }
        },
        required: ["pregunta", "tipo"]
      }
    },
    recursos: {
      type: SchemaType.ARRAY,
      items: {
        type: SchemaType.OBJECT,
        properties: {
          nombre: { type: SchemaType.STRING },
          descripcion: { type: SchemaType.STRING }
        },
        required: ["nombre", "descripcion"]
      }
    },
    productos_asociados: { type: SchemaType.STRING, description: "Productos entregables de la secuencia." },
    instrumentos_evaluacion: { type: SchemaType.STRING, description: "Herramientas usadas para evaluar." },
    bibliografia: { type: SchemaType.STRING, description: "Fuentes bibliográficas citadas." },
    observaciones: { type: SchemaType.STRING, description: "Observaciones finales o recomendaciones." },
    adecuaciones_piar: { type: SchemaType.STRING, description: "Ajustes razonables (PIAR) para estudiantes con dificultades o discapacidad." },
    alertas_generadas: {
      type: SchemaType.ARRAY,
      items: { type: SchemaType.STRING },
      description: "Lista de mensajes de alerta si hubo incoherencias corregidas automáticamente (Ej: DBA no coincidía con Área)."
    },
    dba_utilizado: {
      type: SchemaType.STRING,
      description: "El texto del DBA que finalmente se usó para la planeación (puede ser el original o uno corregido)."
    }
  },
  required: [
    "tema_principal",
    "titulo_secuencia",
    "descripcion_secuencia",
    "objetivo_aprendizaje",
    "contenidos",
    "competencias_men",
    "estandar",
    "metodologia",
    "corporiedad_adi",
    "actividades",
    "rubrica",
    "evaluacion",
    "recursos",
    "productos_asociados",
    "instrumentos_evaluacion",
    "bibliografia",
    "observaciones",
    "adecuaciones_piar",
    "alertas_generadas",
    "dba_utilizado"
  ]
};

// Función auxiliar simple para esperar
const wait = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const generateDidacticSequence = async (input: SequenceInput, refinementInstruction?: string): Promise<DidacticSequence> => {
  const apiKey = import.meta.env.VITE_API_KEY; // Usar VITE_ prefix es mejor práctica en Vite, pero mantendremos compatibilidad si usan process.env shim
  // Nota: Si el usuario usa 'process.env.API_KEY' en Vite sin define, puede fallar.
  // Intentaremos leer de import.meta.env primero si es posible, o fallback.
  // Asumimos que el usuario ya tiene configurado esto, pero el error original mostraba process.env.

  // Vamos a usar la key que venga
  const keyToUse = typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_KEY
    ? import.meta.env.VITE_API_KEY
    : (typeof process !== 'undefined' && process.env ? process.env.API_KEY || "" : "");

  if (!keyToUse) {
    throw new Error("No se encontró la API Key. Revisa tu archivo .env");
  }

  if (keyToUse.includes("AQUI_TU_API_KEY")) {
    throw new Error("¡Alto! No has puesto tu API Key real todavía. Abre el archivo .env y pega tu llave de Google.");
  }

  // Debug (Safe)
  console.log(`Usando API Key: ${keyToUse.substring(0, 4)}...${keyToUse.substring(keyToUse.length - 4)} (Longitud: ${keyToUse.length})`);

  const genAI = new GoogleGenerativeAI(keyToUse);

  // Seguridad: Sanitización básica de entradas
  const sanitizeInput = (text: string | undefined): string => {
    if (!text) return "";
    return text
      .replace(/ignore previous instructions/gi, "")
      .replace(/system prompt/gi, "")
      .replace(/<script>/gi, "")
      .replace(/<\/script>/gi, "")
      .trim();
  };

  const safeTema = sanitizeInput(input.tema);
  const safeDba = sanitizeInput(input.dba);

  const prompt = `
    Actúa como un Experto en Diseño Curricular para Educación Básica y Media en Colombia (Ministerio de Educación Nacional - MEN).
    Tu tarea es diseñar una SECUENCIA DIDÁCTICA detallada y coherente para la Institución Educativa Guaimaral.

    INFORMACIÓN DE ENTRADA:
    - Grado: ${input.grado}
    - Área: ${input.area}
    - Tema Central: ${safeTema}
    - DBA OPCIONAL SUGERIDO POR DOCENTE: "${safeDba}" 
    - Número de Sesiones de clase: ${input.sesiones} (Duración sesión: 50 min)
    - Eje Transversal (CRESE): ${input.ejeCrese}
    ${refinementInstruction ? `- INSTRUCCIÓN DE REFINAMIENTO (PRIORIDAD ALTA): "${sanitizeInput(refinementInstruction)}"` : ''}

    REGLAS DE VALIDACIÓN Y COHERENCIA (CRÍTICO):
    0. **FILTRO DE COMPATIBILIDAD (ELIMINAR DISTORSIÓN)**: 
       - Antes de generar, verifica si el **Tema** (${input.tema}) es compatible pedagógicamente con el **Área** (${input.area}).
       - Si el tema pertenece CLARAMENTE a otra materia (ej: Geometría en Religión, Álgebra en Inglés, Gramática en Educación Física): **NO GENERES LA SECUENCIA**.
       - En este caso, el JSON retornado debe tener:
         - 'titulo_secuencia': "ERROR: INCOMPATIBILIDAD DE ÁREA Y TEMA"
         - 'alertas_generadas': "El tema '${input.tema}' no corresponde al área de '${input.area}'. Por favor, elige un área coherente."
         - Deja los demás campos con textos breves de error.
    
    1. **Validación del DBA**:
       - SI EL "DBA SUGERIDO" ESTÁ VACÍO O ES CORTO (<10 caracteres): Selecciona automáticamente el DBA oficial vigente más pertinente para el Grado ${input.grado}, Área ${input.area} y Tema ${input.tema}.
       - SI EL "DBA SUGERIDO" NO CORRESPONDE AL ÁREA (Incoherencia): Ignóralo y selecciona el correcto.
       - Registra cualquier cambio o selección automática en "alertas_generadas" (Ej: "Se seleccionó automáticamente el DBA: [Texto]...").
       - **OBLIGATORIO**: Pon el DBA que decidiste usar en el campo "dba_utilizado".
       - Si el sugerido era correcto, cópialo íntegramente en "dba_utilizado". No dejes este campo vacío.
    
    2. **Refinamiento**: Si existe una "INSTRUCCIÓN DE REFINAMIENTO", modifica la secuencia generada previamente (o genera una nueva) obedeciendo esa instrucción por encima de las configuraciones estándar, pero manteniendo la estructura curricular legal.

    REQUISITOS PEDAGÓGICOS ESTRICTOS:
    1. **Formato Institucional**: Llena TODOS los campos incluyendo Adecuaciones PIAR.
    2. **Coherencia**: Las actividades deben desarrollar progresivamente el "dba_utilizado".
    3. **Actividades**: Genera exactamente ${input.sesiones} sesiones. Sé EXTREMADAMENTE MINUCIOSO y descriptivo.
       - **Debes incluir el CONTENIDO REAL**: Si es una clase de Inglés o Lenguaje, **INCLUYE EL TEXTO CORTO** de lectura, el vocabulario específico o el diálogo. No digas "leer un texto", ¡ESCRIBE el texto ahí mismo!
       - Si es Matemáticas, **INCLUYE LOS EJERCICIOS NUMÉRICOS** y sus respuestas.
       - Estructura: "Inicio (Exploración), Desarrollo (Práctica/Ejecución), Cierre (Transferencia/Valoración)".
    4. **Evaluación Formativa**: La rúbrica debe ser clara, usando verbos de desempeño.
    5. **Banco de Preguntas (IMPORTANTE)**: Debes generar OBLIGATORIAMENTE **5 preguntas** tipo Saber/ICFES **POR CADA SESIÓN**. Si son ${input.sesiones} sesiones, debes generar un total de ${input.sesiones * 5} preguntas. Ejemplo: Si son 2 sesiones, genera 10 preguntas.
    6. **Corporiedad/ADI**: Incluye pausas activas o momentos de reflexión emocional vinculados al eje ${input.ejeCrese}.
    7. **INTEGRIDAD DE ÁREA (REGLA DE ORO - SIN DISTORSIÓN)**: El Área manda DE FORMA ABSOLUTA sobre el Tema. 
       - Si el docente elige un Área (ej. Religión) pero escribe un Tema inapropiado o de otra materia (ej. Geometría), la IA DEBE ignorar la lógica de la otra materia. No intentes "mezclarlas".
       - **PROHIBIDA LA DISTORSIÓN**: No crees "híbridos" pedagógicos (ej. Religión-Geométrica). Si el área es Religión, genera una clase de Religión sobre el sentido de la vida, valores o moral, e ignora los términos técnicos de geometría.
       - La planeación debe alinearse 100% con los estándares curriculares del MIN de la materia **${input.area}**.
       - Sé fiel a la epistemología de cada materia. Las matemáticas son exactas, la religión es confesional/ética, el inglés es lingüístico. NO LAS CRUCES.
    7. **Inclusión (PIAR)**: En el campo "adecuaciones_piar", describe estrategias concretas y ajustes razonables para estudiantes con dificultades de aprendizaje o discapacidad, relacionadas con el tema.
    8. **Material Imprimible**: En el campo "imprimibles" de cada actividad, sugiere fichas, talleres o guías concretas que el docente puede imprimir y entregar.
    9. **Bibliografía**: Cita al menos 2 fuentes reales.
    
    FORMATO DE SALIDA:
    Retorna EXCLUSIVAMENTE un objeto JSON válido que cumpla con el esquema solicitado.
  `;

  // Lista de modelos priorizada
  // Usuario indica tener acceso a "gemini-2.5-flash" (posible beta/typo) y "gemini-2.0-flash".
  // Los agregamos primero. Si fallan (404), el sistema caerá automáticamente a 1.5-flash.
  const MODELS = [
    "gemini-2.5-flash", // User specific request
    "gemini-2.0-flash", // Standard Next Gen
    "gemini-2.0-flash-exp", // Experimental
    "gemini-1.5-flash", // Backup stable
    "gemini-1.5-pro",
  ];

  let lastError;

  for (const modelName of MODELS) {
    try {
      console.log(`Intentando conectar con modelo: ${modelName}...`);
      const model = genAI.getGenerativeModel({
        model: modelName,
        generationConfig: {
          responseMimeType: "application/json",
          responseSchema: responseSchema,
          temperature: 0.7,
        }
      });

      // Implementamos retry simple para 429 solo en el primer intento si es muy rápido
      let result;
      try {
        result = await model.generateContent(prompt);
      } catch (firstErr: any) {
        if (firstErr.message && firstErr.message.includes('429')) {
          console.warn(`Modelo ${modelName} ocupado (429). Esperando 4 segundos para reintentar...`);
          await wait(4000); // Esperar 4s
          result = await model.generateContent(prompt);
        } else {
          throw firstErr; // Relanzar si no es 429
        }
      }

      if (result && result.response) {
        let text = result.response.text();
        // Clenaing markdown artifacts just in case
        text = text.replace(/```json/g, "").replace(/```/g, "").trim();
        console.log(`¡Éxito con modelo ${modelName}!`);
        return JSON.parse(text) as DidacticSequence;
      }

    } catch (err: any) {
      console.warn(`Fallo con modelo ${modelName}:`, err.message || err);
      lastError = err;

      // Si el error es 404 (modelo no encontrado), no tiene sentido reintentar ese modelo, pasamos al siguiente.
      // Si el error es 429 y ya reintentamos arriba, pasamos al siguiente modelo de la lista.
    }
  }

  // Si llegamos aquí, todos fallaron
  console.error("Todos los modelos fallaron. Último error:", lastError);
  throw new Error("No se pudo conectar con ningun modelo de IA disponible. Por favor intenta más tarde.");
};