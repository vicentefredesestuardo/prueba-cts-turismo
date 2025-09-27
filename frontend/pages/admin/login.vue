<template>
  <div
    class="min-h-screen bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center p-4"
  >
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-blue-600 mb-2">🔐 Admin Login</h1>
        <h2 class="text-lg font-semibold text-gray-800 mb-2">
          Hotel Mirador del Lago
        </h2>
        <p class="text-gray-600">
          Acceso exclusivo para administradores del hotel
        </p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4" novalidate>
        <div>
          <label
            for="username"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Usuario <span class="text-red-600">*</span></label
          >
          <input
            id="username"
            type="text"
            v-model.trim="form.username"
            @blur="
              markTouched('username');
              validateField('username');
            "
            @input="touched.username && validateField('username')"
            autocomplete="username"
            :class="[
              'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2',
              errors.username && (touched.username || triedSubmit)
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500',
            ]"
            :aria-invalid="errors.username && (touched.username || triedSubmit)"
            required
          />
          <p
            v-if="errors.username && (touched.username || triedSubmit)"
            class="mt-1 text-sm text-red-600"
            role="alert"
          >
            {{ errors.username }}
          </p>
        </div>

        <div>
          <label
            for="password"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Contraseña <span class="text-red-600">*</span></label
          >
          <input
            id="password"
            type="password"
            v-model="form.password"
            @blur="
              markTouched('password');
              validateField('password');
            "
            @input="touched.password && validateField('password')"
            autocomplete="current-password"
            :class="[
              'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2',
              errors.password && (touched.password || triedSubmit)
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-blue-500',
            ]"
            :aria-invalid="errors.password && (touched.password || triedSubmit)"
            required
          />
          <p
            v-if="errors.password && (touched.password || triedSubmit)"
            class="mt-1 text-sm text-red-600"
            role="alert"
          >
            {{ errors.password }}
          </p>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        >
          {{ loading ? "Iniciando sesión..." : "Iniciar Sesión" }}
        </button>
      </form>

      <div v-if="message" class="mt-4 p-3 rounded-md" :class="messageClass">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: false });

useHead({
  title: "Login Administrador - Hotel Mirador del Lago",
});

const router = useRouter();
const { adminLogin } = useApi();

const form = ref({ username: "", password: "" });
const loading = ref(false);
const message = ref("");
const messageClass = ref("");

// Estado de validación
const errors = ref({});
const touched = ref({});
const triedSubmit = ref(false);

const markTouched = (field) => {
  touched.value[field] = true;
};

const validateField = (field) => {
  const value = form.value[field];

  // Limpiar error anterior
  delete errors.value[field];

  switch (field) {
    case "username":
      if (!value || value.trim().length === 0) {
        errors.value[field] = "Ingresa tu usuario.";
      }
      break;

    case "password":
      if (!value || value.length === 0) {
        errors.value[field] = "Ingresa tu contraseña.";
      }
      break;
  }
};

const validateAll = () => {
  const fields = ["username", "password"];
  fields.forEach((field) => {
    touched.value[field] = true;
    validateField(field);
  });
  return Object.keys(errors.value).length === 0;
};

// Si ya hay token válido, manda directo al panel
onMounted(() => {
  if (process.client) {
    const token = localStorage.getItem("access_token");
    if (token && !isExpired(token)) router.push("/admin/contestants");
  }
});

function isExpired(jwt) {
  try {
    const payload = JSON.parse(atob(jwt.split(".")[1]));
    const now = Math.floor(Date.now() / 1000);
    return payload.exp && payload.exp <= now;
  } catch {
    return true;
  }
}

const handleLogin = async () => {
  if (loading.value) return;

  triedSubmit.value = true;
  message.value = "";
  messageClass.value = "";

  // Validar antes de enviar
  if (!validateAll()) {
    return;
  }

  loading.value = true;

  try {
    // Llama al backend: POST /api/admin/login/
    const res = await adminLogin({ ...form.value });
    // SimpleJWT responde { access, refresh }
    localStorage.setItem("access_token", res.access);
    localStorage.setItem("refresh_token", res.refresh);

    message.value = "Login exitoso. Redirigiendo...";
    messageClass.value = "bg-green-100 text-green-700 border border-green-300";

    router.push("/admin/contestants");
  } catch (e) {
    if (e?.status === 401 || e?.status === 400) {
      message.value = "Credenciales inválidas. Revisa tu usuario y contraseña.";
    } else if (e?.status >= 500) {
      message.value = "Error del servidor. Inténtalo en unos minutos.";
    } else if (e?.isNetworkError) {
      message.value =
        "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
    } else {
      message.value = "Credenciales inválidas. Revisa tu usuario y contraseña.";
    }
    messageClass.value = "bg-red-100 text-red-700 border border-red-300";
  } finally {
    loading.value = false;
  }
};
</script>
