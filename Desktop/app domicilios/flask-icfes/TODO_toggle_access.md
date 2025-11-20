# TODO: Implementar Toggle de Acceso con AJAX

## Pasos para completar:

1. **Modificar admin_routes.py**:
   - En la función `toggle_access`, detectar si la petición es AJAX (usando `request.headers.get('Content-Type')` o similar).
   - Si es AJAX, retornar JSON con `{"success": True, "message": "Guardado", "new_state": new_access}`.
   - Si no, mantener el comportamiento actual (redirect).

2. **Modificar templates/admin.html**:
   - Agregar JavaScript para interceptar el submit del form.
   - Enviar AJAX POST a la ruta toggle_access.
   - Al recibir respuesta exitosa:
     - Cambiar el texto del botón ("Dar acceso" / "Retirar").
     - Actualizar el display de acceso (True/False).
     - Mostrar "Guardado" temporalmente (e.g., en un div que desaparece en 2 segundos).
   - Manejar errores mostrando mensaje de error.

3. **Probar funcionalidad**:
   - Verificar que el toggle funcione sin recargar la página.
   - Confirmar que "Guardado" aparezca y desaparezca.
   - Asegurar que el estado se actualice correctamente en la DB y UI.
   - Probar fallback (si JS falla, debería recargar).

## Estado actual:
- [x] Paso 1 completado
- [x] Paso 2 completado
- [x] Paso 3 completado
