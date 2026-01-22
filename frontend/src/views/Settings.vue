<script setup>
import { onMounted, ref } from 'vue';
import MainLayout from '../layouts/MainLayout.vue';
import { profil } from '../api/auth';
import { getInitials } from '../utils/Methods'

const user = ref({})
let optionSelected = ref('profil')
const options = ref([
  {
    id: 'profil',
    label: "Profile"
  },
  {
    id: 'edit',
    label: "Modifier profile"
  },
  {
    id: 'changepwd',
    label: "Changer mot de passe"
  }
])

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


</script>
<template>
  <MainLayout>
    <div class="grid grid-cols-3 p-5 justify-center gap-5 items-start">
      <div class="bg-white p-5 shadow-xl/5 rounded-md">
        <ul class="flex flex-col gap-2">
          <li v-for="option in options" class="w-full">
            <button @click="optionSelected = option.id" :class="['p-3 cursor-pointer rounded-lg w-full text-start font-medium transition duration-200',
              option.id === optionSelected ? 'text-indigo-500 bg-indigo-50' : 'hover:bg-indigo-50 hover:text-indigo-500 text-gray-400'
            ]">{{ option.label }}</button>
          </li>
        </ul>
      </div>
      <div v-if="optionSelected === 'profil'" class="col-span-2 bg-white p-5 shadow-xl/5 rounded-md">
        <div class="">
          <div class="flex gap-3 items-center mb-5">
            <span
              class="w-15 h-15 flex items-center justify-center rounded-full bg-linear-30 from-sky-500 to-indigo-500 text-white font-bold text-xl">
              {{ user.userInitial }}
            </span>
            <div class="flex flex-col">
              <span class="text-gray-600 font-semibold">{{ user.first_name }} {{ user.last_name }}</span>
              <div><span class="text-xs py-1 px-2 rounded-full bg-purple-50 text-purple-500 font-medium">{{
                user.role_label }}</span></div>
            </div>
          </div>
          <div>
            <div class="grid grid-cols-2 gap-5">
              <div class="my-2 flex flex-col gap-1">
                <strong class="text-gray-700">Nom</strong>
                <p class="bg-gray-100 p-3 rounded-sm shadow-xs text-sm text-gray-600">{{ user.last_name }}</p>
              </div>

              <div class="my-2 flex flex-col gap-1">
                <strong class="text-gray-700">Prénom</strong>
                <p class="bg-gray-100 p-3 rounded-sm shadow-xs text-sm text-gray-600">{{ user.first_name }}</p>
              </div>
            </div>
            <div class="my-2 flex flex-col gap-1">
              <strong class="text-gray-700">Nom d'utilisateur</strong>
              <p class="bg-gray-100 p-3 rounded-sm shadow-xs text-sm text-gray-600">{{ user.username }}</p>
            </div>
            <div class="grid grid-cols-3 gap-5">
              <div class="my-2 flex flex-col gap-1 col-span-2">
                <strong class="text-gray-700">E-mail</strong>
                <p class="bg-gray-100 p-3 rounded-sm shadow-xs text-sm text-gray-600">{{ user.email }}</p>
              </div>
              <div class="my-2 flex flex-col gap-1">
                <strong class="text-gray-700">Téléphone</strong>
                <p class="bg-gray-100 p-3 rounded-sm shadow-xs text-sm text-gray-600">{{ user.phone }}</p>
              </div>
            </div>

          </div>
        </div>
      </div>
      <div v-if="optionSelected === 'edit'" class="col-span-2 bg-white p-5 shadow-xl/5 rounded-md">
        edit
      </div>
      <div v-if="optionSelected === 'changepwd'" class="col-span-2 bg-white p-5 shadow-xl/5 rounded-md">
        change mdp
      </div>
    </div>
  </MainLayout>
</template>