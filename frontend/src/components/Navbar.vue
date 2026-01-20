<script setup>
import { onMounted, ref } from "vue";
import logoImg from "../assets/Logo.png"
import { CalendarIcon, ChevronDownIcon, ChevronUpIcon, Squares2X2Icon } from '@heroicons/vue/24/solid'
import { useRouter, useRoute } from 'vue-router';
import { logout, profil } from "../api/auth";

const route = useRoute()
const router = useRouter()

const user = ref({})

const getInitials = (firstName, lastName) => {
  const first = firstName ? firstName.charAt(0).toUpperCase() : '';
  const last = lastName ? lastName.charAt(0).toUpperCase() : '';
  return first + last || 'U';
};


const links = ref([
  {
    path: "/planning",
    label: "Suivi planning",
    icon: CalendarIcon
  },
  {
    path: "/manage",
    label: "Gestion RH",
    icon: Squares2X2Icon
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

onMounted(async () => {
  const res = await profil()
  if (res.data) {
    let userInitial = getInitials(res.data.first_name, res.data.last_name)
    user.value = {
      ...res.data,
      userInitial
    }
  }
})

const dropdownLinks = ref([
  {
    path: "profile/",
    label: "Profile",
  },
  {
    path: "setting",
    label: "Paramettre"
  }
])

</script>
<template>
  <nav class="shadow-xl/2">
    <div class="flex items-center justify-between px-8 py-4">
      <div class="flex items-center gap-3">
        <img :src="logoImg" alt="logo_aika" class="w-20 ">
        <div class="">
          <h1 class="text-xl font-bold text-gray-800">GRH</h1>
          <p class="text-xs text-gray-500">Gestion des Ressources Humaines</p>
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
            class="w-10 h-10 flex items-center justify-center rounded-full bg-linear-30 from-sky-500 to-indigo-500 text-white font-bold">
            {{ user.userInitial }}
          </span>
          <ChevronDownIcon class="w-4 h-4 text-gray-700" v-if="!showDropdown" />
          <ChevronUpIcon class="w-4 h-4 text-gray-700" v-if="showDropdown" />
        </button>
        <div v-if="showDropdown" class="absolute z-50 w-54 right-5 mt-1 bg-white shadow-2xl/8 rounded ">
          <div class="px-4 py-4 border-b border-gray-200 bg-linear-to-r from-sky-50 to-blue-50">
            <div class="flex items-center gap-3 mb-3">

              <div>
                <p class="text-sm font-bold text-gray-800">{{ user.name }}</p>
                <p class="text-xs text-gray-600">{{ user.email }}</p>
              </div>
            </div>

            <div class="flex items-center gap-2 mb-2">
              <div class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-semibold">
                ✓ En ligne
              </div>
              <div class="text-xs bg-sky-100 text-sky-700 px-2 py-1 rounded-full font-semibold">
                {{ user.role_label }}
              </div>
            </div>

            <div class="text-xs text-gray-600 space-y-1">
              <p v-if="user.phone">
                <span class="font-semibold">Téléphone:</span> {{ user.phone }}
              </p>
            </div>
          </div>
          <div class="p-2">
            <RouterLink :to="link.path" v-for="link in dropdownLinks"
              class="w-full text-left px-4 py-3 hover:bg-gray-50 transition text-sm text-gray-700 flex items-center gap-3 ">
              <span class="font-medium">{{ link.label }}</span>
            </RouterLink>
          </div>
          <div class="border-t border-gray-200 p-2">
            <button @click="handleLogout"
              class="w-full text-left px-4 py-3 hover:bg-red-50 transition text-sm text-red-600 hover:text-red-700 flex items-center gap-3 font-semibold rounded-lg">
              Déconnexion
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>