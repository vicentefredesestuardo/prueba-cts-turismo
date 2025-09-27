<template>
  <div
    class="min-h-screen bg-gradient-to-br from-green-100 to-blue-100 flex items-center justify-center p-4"
  >
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-green-600 mb-2">
          ✅ Verificar Cuenta
        </h1>
        <h2 class="text-lg font-semibold text-gray-800 mb-2">
          Hotel Mirador del Lago
        </h2>
        <p class="text-gray-600">
          Completa tu registro para el concurso de San Valentín
        </p>
      </div>

      <form @submit.prevent="handleVerify" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Contraseña</label
          >
          <input
            type="password"
            v-model="form.password"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            required
            minlength="8"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Confirmar Contraseña</label
          >
          <input
            type="password"
            v-model="form.password_confirm"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
            required
            minlength="8"
          />
        </div>

        <button
          type="submit"
          :disabled="loading || !token"
          class="w-full bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
        >
          {{ loading ? "Verificando..." : "Activar Cuenta" }}
        </button>
      </form>

      <div
        v-if="!token"
        class="mt-4 p-3 rounded-md bg-yellow-100 text-yellow-800 border border-yellow-300"
      >
        Falta el <strong>token</strong>. Abre este enlace desde tu correo o
        añade <code>?token=...</code> a la URL.
      </div>

      <div v-if="message" class="mt-4 p-3 rounded-md" :class="messageClass">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ layout: false });

useHead({
  title: "Verificar Cuenta - Hotel Mirador del Lago",
});

const route = useRoute();
const router = useRouter();
const { verifyEmail } = useApi();

const token = computed(() => route.query.token || "");

const form = ref({ password: "", password_confirm: "" });
const loading = ref(false);
const message = ref("");
const messageClass = ref("");

onMounted(() => {
  if (!token.value) {
    message.value = "Token de verificación no encontrado en la URL.";
    messageClass.value =
      "bg-yellow-100 text-yellow-800 border border-yellow-300";
  }
});

const handleVerify = async () => {
  if (!token.value) return;
  if (form.value.password !== form.value.password_confirm) {
    message.value = "Las contraseñas no coinciden.";
    messageClass.value = "bg-red-100 text-red-700 border border-red-300";
    return;
  }

  loading.value = true;
  message.value = "";

  try {
    await verifyEmail({
      token: token.value,
      password: form.value.password,
      password_confirm: form.value.password_confirm,
    });

    message.value =
      "Tu cuenta ha sido activada. Ya estás participando en el sorteo.";
    messageClass.value = "bg-green-100 text-green-700 border border-green-300";
    setTimeout(() => router.push("/"), 2000);
  } catch (e) {
    // DRF: puede venir detail, token, password, non_field_errors, etc.
    const data = e?.data || {};
    const first =
      data.detail ||
      data.token ||
      data.password ||
      data.non_field_errors?.[0] ||
      "Error al verificar tu cuenta. Intenta nuevamente.";
    message.value = Array.isArray(first) ? first[0] : first;
    messageClass.value = "bg-red-100 text-red-700 border border-red-300";
  } finally {
    loading.value = false;
  }
};
</script>
