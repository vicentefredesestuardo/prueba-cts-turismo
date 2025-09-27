<template>
  <div
    class="min-h-screen bg-gradient-to-br from-pink-100 to-red-100 flex items-center justify-center p-4"
  >
    <div class="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-pink-600 mb-2">
          💕 Concurso San Valentín
        </h1>
        <h2 class="text-xl font-semibold text-gray-800 mb-2">
          Hotel Mirador del Lago
        </h2>
        <p class="text-gray-600">
          ¡Inscríbete y gana 2 noches románticas en nuestro hotel!
        </p>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4" novalidate>
        <div>
          <label
            for="first_name"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Nombre(s) <span class="text-red-600">*</span></label
          >
          <input
            id="first_name"
            type="text"
            v-model.trim="form.first_name"
            @blur="
              markTouched('first_name');
              validateField('first_name');
            "
            @input="touched.first_name && validateField('first_name')"
            :class="[
              'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2',
              errors.first_name && (touched.first_name || triedSubmit)
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-pink-500',
            ]"
            :aria-invalid="
              errors.first_name && (touched.first_name || triedSubmit)
            "
            required
          />
          <p
            v-if="errors.first_name && (touched.first_name || triedSubmit)"
            class="mt-1 text-sm text-red-600"
            role="alert"
          >
            {{ errors.first_name }}
          </p>
        </div>

        <div>
          <label
            for="last_name"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Apellido Paterno <span class="text-red-600">*</span></label
          >
          <input
            id="last_name"
            type="text"
            v-model.trim="form.last_name"
            @blur="
              markTouched('last_name');
              validateField('last_name');
            "
            @input="touched.last_name && validateField('last_name')"
            :class="[
              'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2',
              errors.last_name && (touched.last_name || triedSubmit)
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-pink-500',
            ]"
            :aria-invalid="
              errors.last_name && (touched.last_name || triedSubmit)
            "
            required
          />
          <p
            v-if="errors.last_name && (touched.last_name || triedSubmit)"
            class="mt-1 text-sm text-red-600"
            role="alert"
          >
            {{ errors.last_name }}
          </p>
        </div>

        <div>
          <label
            for="second_last_name"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Apellido Materno</label
          >
          <input
            id="second_last_name"
            type="text"
            v-model.trim="form.second_last_name"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-pink-500"
          />
        </div>

        <div>
          <label
            for="email"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Correo Electrónico <span class="text-red-600">*</span></label
          >
          <input
            id="email"
            type="email"
            v-model="form.email"
            @blur="
              markTouched('email');
              validateField('email');
            "
            @input="touched.email && validateField('email')"
            :class="[
              'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2',
              errors.email && (touched.email || triedSubmit)
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-pink-500',
            ]"
            :aria-invalid="errors.email && (touched.email || triedSubmit)"
            required
          />
          <p
            v-if="errors.email && (touched.email || triedSubmit)"
            class="mt-1 text-sm text-red-600"
            role="alert"
          >
            {{ errors.email }}
          </p>
        </div>

        <div>
          <label
            for="phone"
            class="block text-sm font-medium text-gray-700 mb-1"
            >Teléfono <span class="text-red-600">*</span></label
          >
          <input
            id="phone"
            type="tel"
            v-model="form.phone"
            @blur="
              markTouched('phone');
              validateField('phone');
            "
            @input="touched.phone && validateField('phone')"
            placeholder="+56912345678"
            :class="[
              'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2',
              errors.phone && (touched.phone || triedSubmit)
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300 focus:ring-pink-500',
            ]"
            :aria-invalid="errors.phone && (touched.phone || triedSubmit)"
            required
          />
          <p
            v-if="errors.phone && (touched.phone || triedSubmit)"
            class="mt-1 text-sm text-red-600"
            role="alert"
          >
            {{ errors.phone }}
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

useHead({
  title: "Concurso San Valentín - Hotel Mirador del Lago",
});

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

// Estado de validación
const errors = ref({});
const touched = ref({});
const triedSubmit = ref(false);

// Helpers de validación
const isEmail = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
const isE164 = (s) => /^\+?[1-9]\d{7,14}$/.test(s);

const markTouched = (field) => {
  touched.value[field] = true;
};

const validateField = (field) => {
  const value = form.value[field];

  // Limpiar error anterior
  delete errors.value[field];

  switch (field) {
    case "first_name":
      if (!value || value.trim().length === 0) {
        errors.value[field] = "Ingresa tu nombre.";
      } else if (value.trim().length < 2) {
        errors.value[field] = "El nombre debe tener al menos 2 caracteres.";
      }
      break;

    case "last_name":
      if (!value || value.trim().length === 0) {
        errors.value[field] = "Ingresa tu apellido paterno.";
      } else if (value.trim().length < 2) {
        errors.value[field] = "El apellido debe tener al menos 2 caracteres.";
      }
      break;

    case "email":
      if (!value || value.trim().length === 0) {
        errors.value[field] = "Ingresa tu correo.";
      } else if (!isEmail(value.trim())) {
        errors.value[field] = "Ingresa un correo válido.";
      }
      break;

    case "phone":
      if (!value || value.trim().length === 0) {
        errors.value[field] = "Ingresa tu teléfono.";
      } else if (!isE164(value.trim())) {
        errors.value[field] =
          "Ingresa un teléfono válido en formato internacional, ej: +56912345678.";
      }
      break;
  }
};

const validateAll = () => {
  const fields = ["first_name", "last_name", "email", "phone"];
  fields.forEach((field) => {
    touched.value[field] = true;
    validateField(field);
  });
  return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
  message.value = "";
  messageClass.value = "";
  triedSubmit.value = true;

  // Validar antes de enviar
  if (!validateAll()) {
    return;
  }

  // Normaliza email y phone para coincidir con backend
  const payload = {
    first_name: (form.value.first_name || "").trim(),
    last_name: (form.value.last_name || "").trim(),
    second_last_name: (form.value.second_last_name || "").trim(),
    email: (form.value.email || "").trim().toLowerCase(),
    phone: (form.value.phone || "").trim(),
  };

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
    errors.value = {};
    touched.value = {};
    triedSubmit.value = false;
  } catch (e) {
    if (e?.status === 400) {
      message.value =
        "Revisa los datos ingresados. Puede que el correo ya esté registrado.";
    } else if (e?.status >= 500) {
      message.value = "Error del servidor. Inténtalo en unos minutos.";
    } else if (e?.isNetworkError) {
      message.value =
        "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
    } else {
      message.value = "Error al procesar tu inscripción. Intenta nuevamente.";
    }
    messageClass.value = "bg-red-100 text-red-700 border border-red-300";
  } finally {
    loading.value = false;
  }
};
</script>
