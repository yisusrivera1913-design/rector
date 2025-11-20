/**
 * Supabase Authentication Integration
 * Uses Supabase JS client to handle login and registration
 */

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm';
import { config } from './config.js';

const supabase = createClient(config.SUPABASE_URL, config.SUPABASE_ANON_KEY);

/**
 * Login user with Supabase using cedula and password
 * @param {string} cedula
 * @param {string} password
 * @returns {Promise<object>} user session or error
 */
export async function supabaseLogin(cedula, password) {
  // Supabase uses email for login, so we assume cedula is stored as email or use a custom auth flow
  // For this example, we assume cedula is stored in a custom column and we use a RPC or filter to login
  // But Supabase auth only supports email/password by default
  // So we need to query user by cedula and then sign in with email/password

  // Query user by cedula
  const { data: users, error: userError } = await supabase
    .from('usuarios')
    .select('email')
    .eq('cedula', cedula)
    .limit(1)
    .single();

  if (userError || !users) {
    return { error: 'Usuario no encontrado' };
  }

  const email = users.email;

  // Sign in with email and password
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    return { error: error.message };
  }

  return { session: data.session, user: data.user };
}

/**
 * Register user with Supabase
 * @param {object} userData - { nombre, email, cedula, password, rol }
 * @returns {Promise<object>} user or error
 */
export async function supabaseRegister(userData) {
  // Register user with email and password
  const { data, error } = await supabase.auth.signUp({
    email: userData.email,
    password: userData.password,
  });

  if (error) {
    return { error: error.message };
  }

  // Insert additional user data in 'usuarios' table
  const { error: insertError } = await supabase
    .from('usuarios')
    .insert([
      {
        id: data.user.id,
        nombre: userData.nombre,
        email: userData.email,
        cedula: userData.cedula,
        rol: userData.rol || 'estudiante',
      },
    ]);

  if (insertError) {
    return { error: insertError.message };
  }

  return { user: data.user };
}
