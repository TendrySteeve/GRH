<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goHome = () => {
  router.push('/');
};

const goBack = () => {
  router.back();
};
</script>

<template>
  <div class="h-screen w-full flex justify-center items-center bg-gray-50">
    <div class="text-center">
      <h1 class="text-9xl font-bold text-sky-600 mb-4">404</h1>
      
      <h2 class="text-4xl font-bold text-gray-800 mb-2">Page non trouvée</h2>
      <p class="text-gray-600 text-lg mb-8">
        Désolé, la page que vous recherchez n'existe pas ou a été supprimée.
      </p>
      
      <div class="flex gap-4 justify-center">
        <button 
          @click="goHome"
          class="bg-sky-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-sky-700 transition"
        >
          Accueil
        </button>
        
        <button 
          @click="goBack"
          class="bg-gray-300 text-gray-800 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition"
        >
          Retour
        </button>
      </div>
      
      <div class="mt-12">
        <svg class="w-48 h-48 mx-auto text-gray-300" fill="currentColor" viewBox="0 0 24 24">
          <path d="M0 0h24v24H0z" fill="none"/>
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
        </svg>
      </div>
    </div>
  </div>
</template>