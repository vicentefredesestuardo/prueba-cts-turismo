<template>
  <div class="min-h-screen bg-gray-50 p-4">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg">
        <!-- Header -->
        <div
          class="bg-gradient-to-r from-purple-600 to-indigo-700 text-white p-6 rounded-t-lg"
        >
          <div
            class="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-4"
          >
            <div class="flex-1">
              <h1 class="text-2xl font-bold">🏆 Sorteo de Ganador</h1>
              <h2 class="text-lg font-semibold text-purple-100">
                Hotel Mirador del Lago
              </h2>
            </div>
            <div class="flex gap-3 flex-wrap">
              <NuxtLink
                to="/admin/contestants"
                class="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white font-semibold px-5 py-2.5 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 flex-1 sm:flex-none min-w-fit text-center"
              >
                👥 Concursantes
              </NuxtLink>
              <button
                @click="logout"
                class="bg-red-500 hover:bg-red-600 font-semibold px-5 py-2.5 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl flex-1 sm:flex-none min-w-fit"
              >
                🚪 Salir
              </button>
            </div>
          </div>
        </div>

        <!-- Contenido -->
        <div class="p-8">
          <!-- Ganador actual -->
          <div
            v-if="winner"
            class="mb-8 p-6 bg-green-50 border border-green-200 rounded-lg"
          >
            <h2 class="text-xl font-bold text-green-800 mb-4">
              🎉 ¡Ganador Seleccionado!
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="font-semibold text-gray-700">Nombre:</p>
                <p class="text-lg text-green-800">
                  {{ winner.contestant_name || winner.contestant?.full_name }}
                </p>
              </div>
              <div>
                <p class="font-semibold text-gray-700">Email:</p>
                <p class="text-lg text-green-800">
                  {{ winner.contestant_email || winner.contestant?.email }}
                </p>
              </div>
              <div>
                <p class="font-semibold text-gray-700">Teléfono:</p>
                <p class="text-lg text-green-800">
                  {{ winner.contestant_phone || winner.contestant?.phone }}
                </p>
              </div>
              <div>
                <p class="font-semibold text-gray-700">Fecha del sorteo:</p>
                <p class="text-lg text-green-800">
                  {{ formatDate(winner.drawn_at) }}
                </p>
              </div>
            </div>
          </div>

          <!-- Botón de sorteo -->
          <div v-else class="text-center">
            <div class="mb-8">
              <h2 class="text-2xl font-bold text-gray-800 mb-4">
                ¿Listo para el sorteo?
              </h2>
              <p class="text-gray-600 mb-6">
                Se seleccionará un ganador aleatorio entre todos los
                concursantes verificados.
              </p>
              <div
                class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg"
              >
                <p class="text-blue-800">
                  <strong>Nota:</strong> Solo se puede realizar el sorteo una
                  vez. El ganador recibirá automáticamente un email.
                </p>
              </div>
            </div>

            <button
              @click="draw"
              :disabled="loading"
              class="bg-purple-600 text-white px-8 py-4 rounded-lg text-xl font-bold hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50 transition-all duration-300 transform hover:scale-105"
            >
              {{ loading ? "🎲 Sorteando..." : "🎲 Realizar Sorteo" }}
            </button>
          </div>

          <!-- Mensaje -->
          <div v-if="message" class="mt-6 p-4 rounded-md" :class="messageClass">
            {{ message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: "admin", layout: false });

useHead({
  title: "Sorteo de Ganador - Hotel Mirador del Lago",
});

const router = useRouter();
const { getWinner, drawWinner } = useApi();

const winner = ref(null);
const loading = ref(false);
const message = ref("");
const messageClass = ref("");

const loadWinner = async () => {
  try {
    const res = await getWinner();
    winner.value = res.winner;
    message.value = "";
  } catch (e) {
    if (e?.status === 404) {
      winner.value = null;
      message.value = "";
    } else if (e?.status === 401) {
      message.value =
        "Tu sesión ha expirado. Por favor inicia sesión nuevamente.";
      messageClass.value =
        "bg-yellow-100 text-yellow-800 border border-yellow-300";
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      setTimeout(() => router.push("/admin/login"), 2000);
    } else if (e?.status >= 500) {
      message.value = "Error del servidor. Inténtalo en unos minutos.";
      messageClass.value = "bg-red-100 text-red-700 border border-red-300";
    } else if (e?.isNetworkError) {
      message.value =
        "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
      messageClass.value = "bg-red-100 text-red-700 border border-red-300";
    } else {
      message.value = "Error al consultar el ganador.";
      messageClass.value = "bg-red-100 text-red-700 border border-red-300";
    }
  }
};

const draw = async () => {
  if (winner.value) {
    message.value = "Ya se ha realizado el sorteo.";
    messageClass.value =
      "bg-yellow-100 text-yellow-700 border border-yellow-300";
    return;
  }
  loading.value = true;
  message.value = "";
  try {
    const res = await drawWinner();
    winner.value = res.winner;
    message.value = res.message || "¡Ganador seleccionado!";
    messageClass.value = "bg-green-100 text-green-700 border border-green-300";
  } catch (e) {
    if (e?.status === 400 && e?.data?.error) {
      message.value = e.data.error;
      messageClass.value =
        "bg-yellow-100 text-yellow-700 border border-yellow-300";
    } else if (e?.status === 401) {
      message.value =
        "Tu sesión ha expirado. Por favor inicia sesión nuevamente.";
      messageClass.value =
        "bg-yellow-100 text-yellow-800 border border-yellow-300";
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      setTimeout(() => router.push("/admin/login"), 2000);
      return;
    } else if (e?.status >= 500) {
      message.value = "Error del servidor. Inténtalo en unos minutos.";
      messageClass.value = "bg-red-100 text-red-700 border border-red-300";
    } else if (e?.isNetworkError) {
      message.value =
        "No se pudo conectar con el servidor. Verifica tu conexión a internet.";
      messageClass.value = "bg-red-100 text-red-700 border border-red-300";
    } else {
      message.value = "Error al realizar el sorteo. Intenta nuevamente.";
      messageClass.value = "bg-red-100 text-red-700 border border-red-300";
    }
  } finally {
    loading.value = false;
  }
};

const formatDate = (iso) =>
  new Date(iso).toLocaleDateString("es-CL", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  router.push("/admin/login");
};

onMounted(loadWinner);
</script>
