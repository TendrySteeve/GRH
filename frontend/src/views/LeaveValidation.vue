<script setup>
import { onMounted, ref } from 'vue';
import MainLayout from '../layouts/MainLayout.vue'
import { approveLeave, getAllLeavesPending, rejectLeave } from '../api/leave';
import { profil } from '../api/auth';
import { CheckIcon, ClockIcon, XMarkIcon } from '@heroicons/vue/24/solid';
import { getInitials } from '../utils/Methods';

const allLeaves = ref([])
const userAuthenticated = ref({})


const loadAllLeaves = async () => {
  try {
    const res = await getAllLeavesPending()
    if (res) {
      allLeaves.value = res
    }
  } catch (error) {
  }
}

const handleRejectLeave = async (leaveId) => {
  try {
    const res = await rejectLeave(leaveId)
    await loadAllLeaves()
  } catch (error) {
  }
}


const handleApproveLeave = async (leaveId) => {
  try {
    const res = await approveLeave(leaveId)
    await loadAllLeaves()
  } catch (error) {
  }
}

const calculateDuration = (startDate, endDate) => {
  if (!startDate || !endDate) return 0;

  const start = new Date(startDate);
  const end = new Date(endDate);

  const diffInMs = end - start;

  const days = Math.floor(diffInMs / (1000 * 60 * 60 * 24)) + 1;

  return days > 0 ? days : 0;
};

const formatDate = (dateString) => {
  if (!dateString) return 'Date inconnue';

  const date = new Date(dateString);

  return date.toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  }).replace('.', '');
};

onMounted(async () => {
  loadAllLeaves()
  try {
    const u = await profil()
    if (u) userAuthenticated.value = u
  } catch (e) {

  }
})

</script>
<template>
  <MainLayout>
    <div class="max-w-5xl mx-auto p-6">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-2xl font-black text-gray-900 tracking-tight">Demandes en attente</h2>
          <p class="text-sm text-gray-500 font-medium italic">Veuillez valider ou refuser les demandes de vos
            collaborateurs</p>
        </div>
        <div
          class="bg-amber-50 text-amber-600 px-4 py-2 rounded-2xl border border-amber-100 flex items-center gap-2 whitespace-nowrap">
          <ClockIcon class="w-4 h-4" />
          <span class="text-xs font-black uppercase tracking-widest">{{ allLeaves.length }} à traiter</span>
        </div>
      </div>

      <div class="space-y-4">
        <div v-for="leave in allLeaves" :key="leave.id"
          class="group bg-white rounded-4xl border border-gray-100 p-6 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">

          <div class="flex flex-col gap-6">

            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">

              <div class="flex items-center gap-4 w-110 shrink-0">
                <div
                  class="w-12 h-12 shrink-0 rounded-2xl bg-indigo-600 text-white flex items-center justify-center font-black text-lg shadow-lg shadow-indigo-100">
                  {{ getInitials(leave.user_firstname, leave.user_lastname) }}
                </div>

                <div class="flex-1 min-w-0 flex flex-col justify-center">
                  <h3 class="font-black text-gray-900 tracking-tight truncate text-sm leading-tight">
                    {{ leave.user_firstname }} {{ leave.user_lastname }}
                  </h3>

                  <p class="text-[10px] text-gray-400 font-bold uppercase tracking-widest whitespace-nowrap mt-0.5">
                    Soumis le {{ formatDate(leave.created_at) }}
                  </p>
                </div>
              </div>

              <div
                class="flex items-center gap-4 bg-gray-50 px-5 py-3 rounded-2xl border border-gray-100 flex-1 justify-between md:justify-start">
                <div class="flex flex-col items-center">
                  <span class="text-[9px] uppercase font-black text-gray-400 whitespace-nowrap">Départ</span>
                  <span class="text-sm font-bold text-gray-800 whitespace-nowrap">{{ formatDate(leave.start_date)
                  }}</span>
                </div>

                <div class="h-8 w-px bg-gray-200 mx-2"></div>

                <div class="flex flex-col items-center">
                  <span class="text-[9px] uppercase font-black text-gray-400 whitespace-nowrap">Retour</span>
                  <span class="text-sm font-bold text-gray-800 whitespace-nowrap">{{ formatDate(leave.end_date)
                  }}</span>
                </div>

                <div class="ml-auto hidden md:block">
                  <span
                    class="bg-blue-100 text-blue-700 px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-tighter whitespace-nowrap">
                    {{ calculateDuration(leave.start_date, leave.end_date) }} Jours
                  </span>
                </div>
              </div>
            </div>

            <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 pt-4 border-t border-gray-50">

              <div v-if="leave.reason" class="flex-1 relative pl-4 border-l-2 border-indigo-200 py-1">
                <p class="text-xs text-gray-500 leading-relaxed">
                  <span class="text-indigo-400 font-serif text-lg leading-none mr-1"></span>
                  {{ leave.reason }}
                </p>
              </div>
              <div v-else class="flex-1 text-xs text-gray-300">
                Aucun motif précisé
              </div>

              <div class="flex items-center gap-2 shrink-0">
                <button @click="handleRejectLeave(leave.id)"
                  class="flex-1 md:flex-none flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-red-50 text-red-600 font-black text-[11px] uppercase tracking-widest whitespace-nowrap hover:bg-red-600 hover:text-white transition-all active:scale-90">
                  <XMarkIcon class="w-4 h-4 shadow-sm" />
                  Rejeter
                </button>

                <button @click="handleApproveLeave(leave.id)"
                  class="flex-1 md:flex-none flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-emerald-500 text-white font-black text-[11px] uppercase tracking-widest whitespace-nowrap shadow-lg shadow-emerald-100 hover:bg-emerald-600 transition-all active:scale-95">
                  <CheckIcon class="w-4 h-4 shadow-sm" />
                  Approuver
                </button>
              </div>
            </div>

          </div>
        </div>

        <div v-if="allLeaves.length === 0"
          class="text-center py-20 bg-gray-50 rounded-[3rem] border-2 border-dashed border-gray-200">
          <p class="text-gray-400 font-medium italic">Aucune demande en attente pour le moment.</p>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<style scoped></style>