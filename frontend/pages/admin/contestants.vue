<template>
  <div class="min-h-screen bg-gray-50 p-4">
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg">
        <!-- Header -->
        <div class="bg-blue-600 text-white p-6 rounded-t-lg">
          <div class="flex justify-between items-center">
            <h1 class="text-2xl font-bold">👥 Lista de Concursantes</h1>
            <div class="flex gap-4">
              <NuxtLink
                to="/admin/winner"
                class="bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-md"
              >
                🏆 Sorteo
              </NuxtLink>
              <button
                @click="logout"
                class="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-md"
              >
                Salir
              </button>
            </div>
          </div>
        </div>

        <!-- Filtros -->
        <div class="p-6 border-b">
          <div class="flex gap-4 items-center flex-wrap">
            <input
              type="text"
              v-model.trim="search"
              placeholder="Buscar por nombre o email..."
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <select
              v-model="verifiedFilter"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos</option>
              <option value="true">Verificados</option>
              <option value="false">No verificados</option>
            </select>
            <button
              @click="applyFilters"
              class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
              Buscar
            </button>
          </div>
        </div>

        <!-- Lista -->
        <div class="p-6">
          <div v-if="loading" class="text-center py-8">
            <p class="text-gray-600">Cargando concursantes...</p>
          </div>

          <div v-else-if="contestants.length === 0" class="text-center py-8">
            <p class="text-gray-600">No hay concursantes registrados.</p>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full table-auto">
              <thead>
                <tr class="bg-gray-100">
                  <th class="px-4 py-2 text-left">Nombre Completo</th>
                  <th class="px-4 py-2 text-left">Email</th>
                  <th class="px-4 py-2 text-left">Teléfono</th>
                  <th class="px-4 py-2 text-left">Estado</th>
                  <th class="px-4 py-2 text-left">Fecha Registro</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="c in contestants" :key="c.id" class="border-b">
                  <td class="px-4 py-2">{{ c.full_name }}</td>
                  <td class="px-4 py-2">{{ c.email }}</td>
                  <td class="px-4 py-2">{{ c.phone }}</td>
                  <td class="px-4 py-2">
                    <span
                      v-if="c.is_verified"
                      class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-sm"
                    >
                      ✅ Verificado
                    </span>
                    <span
                      v-else
                      class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-sm"
                    >
                      ⏳ Pendiente
                    </span>
                  </td>
                  <td class="px-4 py-2">{{ formatDate(c.created_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Paginación -->
          <div
            v-if="totalPages > 1"
            class="mt-6 flex justify-center gap-2 flex-wrap"
          >
            <button
              v-for="p in totalPages"
              :key="p"
              @click="goToPage(p)"
              :class="[
                'px-3 py-2 rounded-md',
                p === currentPage
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
              ]"
            >
              {{ p }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: "admin", layout: false });

const router = useRouter();
const { getContestants } = useApi();

// Estado
const contestants = ref([]);
const loading = ref(false);
const search = ref("");
const verifiedFilter = ref("");
const currentPage = ref(1);
const pageSize = 50;
const totalPages = ref(1);
const totalCount = ref(0);

const fetchContestants = async () => {
  loading.value = true;
  try {
    const res = await getContestants({
      search: search.value || "",
      verified: verifiedFilter.value || "",
      page: currentPage.value,
      page_size: pageSize,
    });
    contestants.value = res.contestants || [];
    totalCount.value = res.count || 0;
    totalPages.value = Math.max(1, Math.ceil(totalCount.value / pageSize));
  } catch (e) {
    // Si el token expiró o no es válido, DRF devolverá 401
    if (e?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      return router.push("/admin/login");
    }
    console.error("Error fetching contestants:", e);
  } finally {
    loading.value = false;
  }
};

const applyFilters = () => {
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
