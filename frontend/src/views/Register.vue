<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Input from '../components/UI/Input.vue';
import { register } from '../api/auth';

const router = useRouter();
const loading = ref(false);
const errors = ref({});
const generalError = ref('');
const successMessage = ref('');

const formData = ref({
  username: '',
  email: '',
  phone: '',
  first_name: '',
  last_name: '',
  password: '',
  password_confirm: ''
});

const validateForm = () => {
  errors.value = {};

  if (!formData.value.username || formData.value.username.length < 3) {
    errors.value.username = 'Le nom d\'utilisateur doit contenir au moins 3 caractères';
  }

  if (!formData.value.email || !formData.value.email.includes('@')) {
    errors.value.email = 'Veuillez entrer une adresse email valide';
  }

  if (!formData.value.first_name) {
    errors.value.first_name = 'Le prénom est requis';
  }

  if (!formData.value.last_name) {
    errors.value.last_name = 'Le nom est requis';
  }

  if (formData.value.phone && !/^\d{10,13}$/.test(formData.value.phone.replace(/\s/g, ''))) {
    errors.value.phone = 'Numéro de téléphone invalide';
  }

  if (!formData.value.password || formData.value.password.length < 8) {
    errors.value.password = 'Le mot de passe doit contenir au moins 8 caractères';
  }

  if (formData.value.password !== formData.value.password_confirm) {
    errors.value.password_confirm = 'Les mots de passe ne correspondent pas';
  }

  return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
  if (!validateForm()) return;

  loading.value = true;
  generalError.value = '';
  successMessage.value = '';

  try {
    const data = {
      username: formData.value.username,
      email: formData.value.email,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      phone: formData.value.phone,
      password: formData.value.password,
      password_confirm: formData.value.password_confirm
    };

    await register(data);

    successMessage.value = 'Inscription réussie! Redirection vers la connexion...';

    setTimeout(() => {
      router.push('/login');
    }, 2000);

  } catch (error) {
    generalError.value = error.response?.data?.username?.[0] ||
      error.response?.data?.email?.[0] ||
      'Erreur lors de l\'inscription. Veuillez réessayer.';
  } finally {
    loading.value = false;
  }
};

const clearForm = () => {
  formData.value = {
    username: '',
    email: '',
    phone: '',
    first_name: '',
    last_name: '',
    password: '',
    password_confirm: ''
  };
  errors.value = {};
  generalError.value = '';
  successMessage.value = '';
};
</script>

<template>
  <div class="min-h-screen w-full flex justify-center items-center bg-linear-to-br from-sky-50 to-blue-100 p-4">
    <div class="shadow-2xl p-10 rounded-2xl bg-white w-full max-w-2xl">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 bg-sky-100 rounded-full mb-4">
          <svg class="w-8 h-8 text-sky-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Créer un compte</h1>
        <p class="text-gray-500">Rejoignez notre plateforme RH</p>
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

      <transition name="fade">
        <div v-if="successMessage"
          class="bg-green-50 border-l-4 border-green-500 text-green-700 px-4 py-3 rounded mb-6 flex items-start gap-3">
          <svg class="w-5 h-5 mt-0.5 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"></path>
          </svg>
          <span>{{ successMessage }}</span>
        </div>
      </transition>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <Input inputId="first_name" inputType="text" v-model="formData.first_name" label="Prénom" placeholder="Jean"
            :error="errors.first_name" :disabled="loading" required inputClass="focus:border-sky-600" />
          <Input inputId="last_name" inputType="text" v-model="formData.last_name" label="Nom" placeholder="Dupont"
            :error="errors.last_name" :disabled="loading" required inputClass="focus:border-sky-600" />
        </div>

        <Input inputId="username" inputType="text" v-model="formData.username" label="Nom d'utilisateur"
          placeholder="jdupont" :error="errors.username" :disabled="loading" required
          inputClass="focus:border-sky-600" />

        <div class="grid grid-cols-3 gap-4">
          <Input inputId="email" inputType="email" v-model="formData.email" label="E-mail" placeholder="votre@email.com"
            :error="errors.email" :disabled="loading" required inputClass="focus:border-sky-600" divClass="col-span-2" />

          <Input inputId="phone" inputType="phone" v-model="formData.phone" label="Téléphone"
            placeholder="03X XX XXX XX" :error="errors.phone" :disabled="loading"
            inputClass="focus:border-sky-600" />
        </div>

        <div class="grid grid-cols-2 gap-4">
          <Input inputId="password" inputType="password" v-model="formData.password" label="Mot de passe"
            placeholder="••••••••" :error="errors.password" :disabled="loading" required
            inputClass="focus:border-sky-600" />

          <Input inputId="password_confirm" inputType="password" v-model="formData.password_confirm"
            label="Confirmer le mot de passe" placeholder="••••••••" :error="errors.password_confirm"
            :disabled="loading" required inputClass="focus:border-sky-600" />
        </div>

        <button type="submit" :disabled="loading"
          class="w-full bg-linear-to-r from-sky-600 to-blue-600 text-white py-3 rounded-lg font-semibold cursor-pointer hover:from-sky-700 hover:to-blue-700 transition duration-300 disabled:opacity-60 disabled:cursor-not-allowed shadow-lg hover:shadow-xl mt-6">
          <span v-if="loading" class="inline-flex items-center gap-2">
            <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            Inscription en cours...
          </span>
          <span v-else>S'inscrire</span>
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
          Vous avez déjà un compte?
          <router-link to="/login" class="text-sky-600 font-semibold hover:text-sky-700 hover:underline transition">
            Se connecter
          </router-link>
        </p>
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