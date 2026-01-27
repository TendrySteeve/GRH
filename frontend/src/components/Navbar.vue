<script setup>
import { onMounted, ref } from "vue";
import logoImg from "../assets/Logo.png"
import { CalendarIcon, ChevronDownIcon, ChevronUpIcon, Squares2X2Icon, CalendarDaysIcon, CheckBadgeIcon, ChevronRightIcon } from '@heroicons/vue/24/solid'
import { useRouter, useRoute } from 'vue-router';
import { logout, profil } from "../api/auth";
import { getInitials } from '../utils/Methods'


const route = useRoute()
const router = useRouter()

const user = ref({})

const links = ref([
  {
    path: "/schedule",
    label: "Suivi planning",
    icon: CalendarIcon
  },
  {
    path: "/manage-schedule",
    label: "Gestion des planning",
    icon: Squares2X2Icon
  },
  {
    path: "/manage-leave",
    label: "Gestion des congé",
    icon: CalendarDaysIcon
  },
  {
    path: "/validate-leave",
    label: "Validation des Congés",
    icon: CheckBadgeIcon
  }
])

const isActive = (menuRoute) => {
  return route.path === menuRoute;
};


const showDropdown = ref(false)

const handleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const handleLogout = () => {
  logout();
  router.push('/login');
};

const goTo = (path) => {
  router.push(path)
}

onMounted(async () => {
  const res = await profil()
  if (res) {
    let userInitial = getInitials(res.first_name, res.last_name)
    user.value = {
      ...res,
      userInitial
    }
  }
})

const dropdownLinks = ref([
  {
    path: "/setting",
    label: "Paramettre"
  }
])

</script>
<template>
  <nav class="bg-white shadow sticky top-0 z-50">
    <div class="flex items-center justify-between px-8 py-4">
      <div class="flex items-center gap-3">
        <img :src="logoImg" alt="logo_aika" class="w-20 ">
        <div class="">
          <h1 class="text-xl font-bold text-gray-600">Alliance Aika</h1>
          <p class="text-xs text-gray-500">Gestion RH</p>
        </div>
      </div>
      <div class="">
        <ul class="flex gap-2 justify-center items-center">
          <li v-for="link in links" class="">
            <RouterLink :to="link.path"
              :class="['flex flex-col items-center justify-center  py-1 px-3 rounded-lg transition duration-200 ',
                isActive(link.path) ? 'text-blue-500 bg-blue-50' : 'hover:bg-blue-50 hover:text-blue-500 text-gray-400']">
              <component :is="link.icon" class="w-8" />
              <span class="text-sm">{{ link.label }}</span>
            </RouterLink>
          </li>
        </ul>
      </div>
      <div class="relative">
        <button class="cursor-pointer flex items-center gap-1 hover:bg-gray-50 px-4 py-2 rounded-lg transition"
          @click="handleDropdown">
          <span
            class="w-10 h-10 flex items-center justify-center rounded-full bg-linear-30 from-sky-500 to-indigo-500 text-white text-sm font-bold">
            {{ user.userInitial }}
          </span>
          <ChevronDownIcon class="w-4 h-4 text-gray-700" v-if="!showDropdown" />
          <ChevronUpIcon class="w-4 h-4 text-gray-700" v-if="showDropdown" />
        </button>
        <div v-if="showDropdown"
          class="absolute z-50 w-72 right-5 mt-3 bg-white/95 backdrop-blur-xl shadow-[0_20px_50px_rgba(0,0,0,0.1)] rounded-3xl border border-gray-100 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200">

          <div class="px-6 py-6 border-b border-gray-100 bg-linear-to-br from-gray-50/50 to-white">
            <div class="flex items-center gap-4 mb-4">
              <div
                class="w-12 h-12 rounded-2xl bg-blue-600 flex items-center justify-center text-white font-black text-lg shadow-lg shadow-blue-100">
                {{ user.first_name.charAt(0) }}{{ user.last_name.charAt(0) }}
              </div>
              <div>
                <p class="text-sm font-black text-gray-900 tracking-tight leading-none mb-1">{{ user.name }}</p>
                <p class="text-[11px] font-medium text-gray-400 truncate w-40">{{ user.email }}</p>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <div
                class="flex items-center gap-1.5 bg-emerald-50 text-emerald-600 px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest ring-1 ring-inset ring-emerald-600/10">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                En ligne
              </div>
              <div
                class="bg-blue-50 text-blue-600 px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest ring-1 ring-inset ring-blue-600/10">
                {{ user.role_label }}
              </div>
            </div>
          </div>

          <div v-if="user.phone" class="px-6 py-3 bg-gray-50/50 border-b border-gray-50">
            <p class="text-[10px] text-gray-400 font-bold uppercase tracking-tighter mb-0.5">Téléphone</p>
            <p class="text-xs text-gray-700 font-bold">{{ user.phone }}</p>
          </div>

          <div class="p-2">
            <button @click="goTo(link.path)" v-for="link in dropdownLinks" :key="link.path"
              class="w-full text-left px-4 py-3 hover:bg-blue-50/50 rounded-xl transition-all duration-200 text-sm text-gray-600 hover:text-blue-600 flex items-center justify-between group">
              <span class="font-bold tracking-tight">{{ link.label }}</span>
              <ChevronRightIcon
                class="w-4 h-4 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all text-blue-400" />
            </button>
          </div>

          <div class="p-2 bg-gray-50/30">
            <button @click="handleLogout"
              class="w-full text-left px-4 py-3 hover:bg-red-50 rounded-xl transition-all duration-200 text-sm text-red-500 hover:text-red-600 flex items-center gap-3 font-black uppercase tracking-widest text-[10px]">
              Déconnexion
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>