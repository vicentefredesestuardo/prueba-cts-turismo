<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-gray-100 p-4">
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-xl shadow-xl overflow-hidden">
        <!-- Header -->
        <div
          class="bg-gradient-to-r from-purple-600 to-indigo-700 text-white p-6"
        >
          <div
            class="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-4"
          >
            <div class="flex-1">
              <h1 class="text-3xl font-bold">👥 Concursantes</h1>
              <h2 class="text-xl font-semibold text-purple-100">
                Hotel Mirador del Lago
              </h2>
              <p class="text-purple-100 mt-1">
                Gestiona los participantes del concurso de San Valentín
              </p>
            </div>
            <div class="flex gap-3 flex-wrap">
              <NuxtLink
                to="/admin/winner"
                class="bg-yellow-500 hover:bg-yellow-600 text-yellow-900 font-semibold px-5 py-2.5 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 flex-1 sm:flex-none min-w-fit text-center"
              >
                🏆 Sorteo
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

        <!-- Filtros -->
        <div class="p-6 border-b border-gray-200 bg-gray-50">
          <div class="flex flex-col lg:flex-row gap-4">
            <!-- Search bar -->
            <div class="flex-1 lg:min-w-0">
              <input
                type="text"
                v-model.trim="search"
                placeholder="🔍 Buscar por nombre o email..."
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
              />
            </div>

            <!-- Selector y botón -->
            <div class="flex gap-4 lg:gap-3 lg:flex-shrink-0">
              <select
                v-model="verifiedFilter"
                class="flex-1 lg:flex-none lg:min-w-48 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 bg-white"
              >
                <option value="">📋 Todos</option>
                <option value="true">✅ Verificados</option>
                <option value="false">⏳ No verificados</option>
              </select>
              <button
                @click="applyFilters"
                class="flex-1 lg:flex-none bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-semibold px-6 py-3 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 whitespace-nowrap"
              >
                🔍 Buscar
              </button>
            </div>
          </div>
        </div>

        <!-- Lista -->
        <div class="p-6">
          <div v-if="loading" class="text-center py-12">
            <div
              class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"
            ></div>
            <p class="text-gray-600 mt-3">Cargando concursantes...</p>
          </div>

          <div v-else-if="contestants.length === 0" class="text-center py-12">
            <div class="text-6xl mb-4">😔</div>
            <p class="text-gray-600 text-lg">
              No hay concursantes que coincidan con los filtros.
            </p>
            <button
              @click="clearFilters"
              class="mt-4 text-purple-600 hover:text-purple-800 font-medium"
            >
              🔄 Limpiar filtros
            </button>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full table-auto">
              <thead>
                <tr class="bg-gradient-to-r from-gray-100 to-gray-200">
                  <th class="px-6 py-4 text-left font-semibold text-gray-700">
                    Nombre Completo
                  </th>
                  <th class="px-6 py-4 text-left font-semibold text-gray-700">
                    Email
                  </th>
                  <th class="px-6 py-4 text-left font-semibold text-gray-700">
                    Teléfono
                  </th>
                  <th class="px-6 py-4 text-left font-semibold text-gray-700">
                    Estado
                  </th>
                  <th class="px-6 py-4 text-left font-semibold text-gray-700">
                    Fecha Registro
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="c in contestants"
                  :key="c.id"
                  class="border-b border-gray-200 hover:bg-gray-50 transition-colors duration-150"
                >
                  <td class="px-6 py-4 font-medium text-gray-900">
                    {{ c.full_name }}
                  </td>
                  <td class="px-6 py-4 text-gray-600">{{ c.email }}</td>
                  <td class="px-6 py-4 text-gray-600">{{ c.phone }}</td>
                  <td class="px-6 py-4">
                    <span
                      v-if="c.is_verified"
                      class="inline-flex items-center gap-1.5 bg-green-100 text-green-800 px-3 py-1.5 rounded-full text-sm font-medium border border-green-200 whitespace-nowrap"
                    >
                      <span class="text-green-500">●</span>
                      <span>Verificado</span>
                    </span>
                    <span
                      v-else
                      class="inline-flex items-center gap-1.5 bg-amber-100 text-amber-800 px-3 py-1.5 rounded-full text-sm font-medium border border-amber-200 whitespace-nowrap"
                    >
                      <span class="text-amber-500">●</span>
                      <span>Pendiente</span>
                    </span>
                  </td>
                  <td class="px-6 py-4 text-gray-500 text-sm">
                    {{ formatDate(c.created_at) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Paginación -->
          <div
            v-if="totalPages > 1"
            class="mt-8 flex justify-center gap-2 flex-wrap"
          >
            <button
              v-for="p in totalPages"
              :key="p"
              @click="goToPage(p)"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-all duration-200',
                p === currentPage
                  ? 'bg-purple-600 text-white shadow-lg transform scale-105'
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300 hover:border-purple-300',
              ]"
            >
              {{ p }}
            </button>
          </div>

          <!-- Mensaje de error/estado -->
          <div v-if="message" class="mt-6 p-4 rounded-md" :class="messageClass">
            {{ message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: ["admin"], layout: false });

useHead({
  title: "Concursantes - Hotel Mirador del Lago",
});

const router = useRouter();
const { getContestants } = useApi();

const contestants = ref([]);
const loading = ref(false);
const message = ref("");
const messageClass = ref("");
const search = ref("");
const verifiedFilter = ref("");
const currentPage = ref(1);
const pageSize = 50;
const totalPages = ref(1);
const totalCount = ref(0);

const fetchContestants = async () => {
  loading.value = true;
  message.value = "";
  messageClass.value = "";
  try {
    const params = {
      search: search.value || "",
      page: currentPage.value,
      page_size: pageSize,
    };

    if (verifiedFilter.value !== "") {
      params.verified = verifiedFilter.value;
    }

    const res = await getContestants(params);

    contestants.value = res.contestants || [];
    totalCount.value = res.count || 0;
    totalPages.value = Math.max(1, Math.ceil(totalCount.value / pageSize));
  } catch (e) {
    if (e?.status === 401) {
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
    }
  } finally {
    loading.value = false;
  }
};

const applyFilters = () => {
  currentPage.value = 1;
  fetchContestants();
};

const clearFilters = () => {
  search.value = "";
  verifiedFilter.value = "";
  currentPage.value = 1;
  fetchContestants();
};

const goToPage = (p) => {
  if (p === currentPage.value) return;
  currentPage.value = p;
  fetchContestants();
};

const formatDate = (iso) => {
  return new Date(iso).toLocaleDateString("es-CL", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const logout = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  router.push("/admin/login");
};

onMounted(fetchContestants);
</script>
