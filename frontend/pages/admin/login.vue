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
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Usuario</label
          >
          <input
            type="text"
            v-model.trim="form.username"
            autocomplete="username"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Contraseña</label
          >
          <input
            type="password"
            v-model="form.password"
            autocomplete="current-password"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
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
  loading.value = true;
  message.value = "";

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
    // DRF / SimpleJWT suelen devolver .data.detail o .data.non_field_errors
    const detail = e?.data?.detail || e?.data?.non_field_errors?.[0];
    message.value =
      detail || "Credenciales inválidas o no tienes permisos de administrador.";
    messageClass.value = "bg-red-100 text-red-700 border border-red-300";
  } finally {
    loading.value = false;
  }
};
</script>
