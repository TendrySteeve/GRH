<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Input from '../components/UI/Input.vue';
import { login } from '../api/auth';

const router = useRouter();
const loading = ref(false);
const errors = ref({});
const generalError = ref('');

const formData = ref({
  username: '',
  password: ''
});

const validateForm = () => {
  errors.value = {};

  if (!formData.value.username) {
    errors.value.username = 'Le nom d\'utilisateur est requis';
  }

  if (!formData.value.password) {
    errors.value.password = 'Le mot de passe est requis';
  }

  return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  loading.value = true;
  generalError.value = '';

  try {
    const response = await login(formData.value);
    console.log('Login successful:', response);

    localStorage.setItem('access_token', response.access);
    localStorage.setItem('refresh_token', response.refresh);

    router.push('/planning');
  } catch (error) {
    if (error.status == 401) generalError.value = "Ce compte n'a pas encore l'autorisation. Contacter l'administrateur"
    else generalError.value = 'Erreur de connexion. Vérifiez vos identifiants.'
  } finally {
    loading.value = false;
  }
};

const clearForm = () => {
  formData.value = { username: '', password: '' };
  errors.value = {};
  generalError.value = '';
};
</script>

<template>
  <div class="min-h-screen w-full flex justify-center items-center bg-gray-50">
    <div class="shadow-2xl p-10 rounded-2xl bg-white w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 bg-sky-100 rounded-full mb-4">
          <svg class="w-8 h-8 text-sky-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z">
            </path>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Connexion</h1>
        <p class="text-gray-500">Accédez à votre plateforme RH</p>
      </div>

      <transition name="fade">
        <div v-if="generalError"
          class="bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded mb-6 flex items-start gap-3">
          <svg class="w-5 h-5 mt-0.5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"></path>
          </svg>
          <span>{{ generalError }}</span>
        </div>
      </transition>

      <form @submit.prevent="handleSubmit" class="space-y-5">
        <Input inputId="username" inputType="text" v-model="formData.username" label="Nom d'utilisateur"
          placeholder="Entrez votre nom d'utilisateur" :error="errors.username" :disabled="loading" required
          inputClass="focus:border-sky-600" />

        <Input inputId="password" inputType="password" v-model="formData.password" label="Mot de passe"
          placeholder="••••••••" :error="errors.password" :disabled="loading" required
          inputClass="focus:border-sky-600" />

        <div class="flex items-center justify-between text-sm">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" class="w-4 h-4 rounded border-gray-300 text-sky-600 focus:ring-sky-600">
              <span class="text-gray-600">Se souvenir de moi</span>
          </label>
          <router-link to="/forgot-password"
            class="text-sky-600 font-medium hover:text-sky-700 hover:underline transition">
            Mot de passe oublié?
          </router-link>
        </div>

        <button type="submit" :disabled="loading"
          class="w-full bg-sky-600 text-white py-3 rounded-lg font-semibold cursor-pointer hover:bg-blue-600 transition duration-300 disabled:opacity-60 disabled:cursor-not-allowed shadow-lg hover:shadow-xl mt-6">
          <span v-if="loading" class="inline-flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            Connexion en cours...
          </span>
          <span v-else>Se connecter</span>
        </button>
      </form>

      <div class="relative my-6">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-gray-300"></div>
        </div>
        <div class="relative flex justify-center text-sm">
          <span class="px-2 bg-white text-gray-500">Ou</span>
        </div>
      </div>

      <div class="text-center">
        <p class="text-gray-600">
          Pas encore de compte?
          <router-link to="/register" class="text-sky-600 font-semibold hover:text-sky-700 hover:underline transition">
            S'inscrire
          </router-link>
        </p>
      </div>

      <div class="mt-8 pt-6 border-t border-gray-200 text-center text-xs text-gray-500">
        <p>RH-Gestion © 2026 - Tous droits réservés</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>