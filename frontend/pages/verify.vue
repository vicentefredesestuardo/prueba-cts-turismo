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
            :class="[
              'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2',
              errors.password && (touched.password || triedSubmit)
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-green-500',
            ]"
            :aria-invalid="errors.password && (touched.password || triedSubmit)"
            required
            minlength="8"
          />
          <p
            v-if="errors.password && (touched.password || triedSubmit)"
            class="mt-1 text-sm text-red-600"
            role="alert"
          >
            {{ errors.password }}
          </p>
        </div>

        <div>
          <label
            for="password_confirm"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Confirmar Contraseña <span class="text-red-600">*</span></label
          >
          <input
            id="password_confirm"
            type="password"
            v-model="form.password_confirm"
            @blur="
              markTouched('password_confirm');
              validateField('password_confirm');
            "
            @input="
              touched.password_confirm && validateField('password_confirm')
            "
            :class="[
              'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2',
              errors.password_confirm &&
              (touched.password_confirm || triedSubmit)
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-green-500',
            ]"
            :aria-invalid="
              errors.password_confirm &&
              (touched.password_confirm || triedSubmit)
            "
            required
            minlength="8"
          />
          <p
            v-if="
              errors.password_confirm &&
              (touched.password_confirm || triedSubmit)
            "
            class="mt-1 text-sm text-red-600"
            role="alert"
          >
            {{ errors.password_confirm }}
          </p>
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
    case "password":
      if (!value || value.length === 0) {
        errors.value[field] = "Ingresa tu contraseña.";
      } else if (value.length < 8) {
        errors.value[field] = "La contraseña debe tener al menos 8 caracteres.";
      }
      break;

    case "password_confirm":
      if (!value || value.length === 0) {
        errors.value[field] = "Confirma tu contraseña.";
      } else if (value !== form.value.password) {
        errors.value[field] = "Las contraseñas no coinciden.";
      }
      break;
  }
};

const validateAll = () => {
  const fields = ["password", "password_confirm"];
  fields.forEach((field) => {
    touched.value[field] = true;
    validateField(field);
  });
  return Object.keys(errors.value).length === 0;
};

onMounted(() => {
  if (!token.value) {
    message.value = "Token de verificación no encontrado en la URL.";
    messageClass.value =
      "bg-yellow-100 text-yellow-800 border border-yellow-300";
  }
});

const handleVerify = async () => {
  if (!token.value) return;

  triedSubmit.value = true;
  message.value = "";
  messageClass.value = "";

  // Validar antes de enviar
  if (!validateAll()) {
    return;
  }

  loading.value = true;

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
    if (e?.status === 400) {
      message.value =
        "Token inválido o expirado. Solicita un nuevo enlace de verificación.";
    } else if (e?.status >= 500) {
      message.value = "Error del servidor. Inténtalo en unos minutos.";
    } else if (e?.isNetworkError) {
      message.value =
        "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
    } else {
      message.value = "Error al verificar tu cuenta. Intenta nuevamente.";
    }
    messageClass.value = "bg-red-100 text-red-700 border border-red-300";
  } finally {
    loading.value = false;
  }
};
</script>
