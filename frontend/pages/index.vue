<template>
  <div
    class="min-h-screen bg-gradient-to-br from-pink-100 to-red-100 flex items-center justify-center p-4"
  >
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-pink-600 mb-2">
          💕 Concurso San Valentín
        </h1>
        <p class="text-gray-600">¡Inscríbete y gana 2 noches románticas!</p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4" novalidate>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Nombre(s)</label
          >
          <input
            type="text"
            v-model.trim="form.first_name"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Apellido Paterno</label
          >
          <input
            type="text"
            v-model.trim="form.last_name"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Apellido Materno</label
          >
          <input
            type="text"
            v-model.trim="form.second_last_name"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Correo Electrónico</label
          >
          <input
            type="email"
            v-model="form.email"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Teléfono</label
          >
          <input
            type="tel"
            v-model="form.phone"
            placeholder="+56912345678"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
            required
          />
          <p v-if="phoneError" class="text-sm text-red-600 mt-1">
            {{ phoneError }}
          </p>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-pink-600 text-white py-2 px-4 rounded-md hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-pink-500 disabled:opacity-50"
        >
          {{ loading ? "Inscribiendo..." : "¡Inscribirme!" }}
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

const { registerContestant } = useApi();

const form = ref({
  first_name: "",
  last_name: "",
  second_last_name: "",
  email: "",
  phone: "",
});

const loading = ref(false);
const message = ref("");
const messageClass = ref("");
const phoneError = ref("");

const e164 = /^\+?[1-9]\d{7,14}$/; // mismo criterio que tu validador del backend

const handleSubmit = async () => {
  message.value = "";
  messageClass.value = "";
  phoneError.value = "";

  // Normaliza email y phone para coincidir con backend
  const payload = {
    first_name: (form.value.first_name || "").trim(),
    last_name: (form.value.last_name || "").trim(),
    second_last_name: (form.value.second_last_name || "").trim(),
    email: (form.value.email || "").trim().toLowerCase(),
    phone: (form.value.phone || "").trim(),
  };

  // Validación rápida de teléfono (evita ida y vuelta inútil)
  if (!e164.test(payload.phone)) {
    phoneError.value =
      "Ingrese un teléfono válido en formato internacional (E.164), ej: +56912345678.";
    return;
  }

  loading.value = true;
  try {
    await registerContestant(payload);

    message.value =
      "¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta (puede llegar a Spam).";
    messageClass.value = "bg-green-100 text-green-700 border border-green-300";

    // Limpia formulario
    form.value = {
      first_name: "",
      last_name: "",
      second_last_name: "",
      email: "",
      phone: "",
    };
  } catch (e) {
    // Muestra el primer error que venga del serializer
    const data = e?.data || {};
    const first =
      data.email ||
      data.phone ||
      data.first_name ||
      data.last_name ||
      data.non_field_errors?.[0] ||
      "Error al procesar tu inscripción. Intenta nuevamente.";
    const msg = Array.isArray(first) ? first[0] : first;
    message.value = msg;
    messageClass.value = "bg-red-100 text-red-700 border border-red-300";
  } finally {
    loading.value = false;
  }
};
</script>
