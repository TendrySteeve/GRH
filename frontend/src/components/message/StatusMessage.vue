<script setup>
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  type: { type: String, default: 'success' }, // 'success', 'error', 'warning'
  title: String,
  message: String,
  show: Boolean
})

const emit = defineEmits(['close'])

const configs = {
  success: {
    bg: 'bg-emerald-50/90',
    border: 'border-emerald-100',
    icon: CheckCircleIcon,
    iconColor: 'text-emerald-500',
    titleColor: 'text-emerald-900',
    msgColor: 'text-emerald-700'
  },
  error: {
    bg: 'bg-red-50/90',
    border: 'border-red-100',
    icon: XCircleIcon,
    iconColor: 'text-red-500',
    titleColor: 'text-red-900',
    msgColor: 'text-red-700'
  },
  warning: {
    bg: 'bg-amber-50/90',
    border: 'border-amber-100',
    icon: ExclamationTriangleIcon,
    iconColor: 'text-amber-500',
    titleColor: 'text-amber-900',
    msgColor: 'text-amber-700'
  }
}
</script>

<template>
  <Transition enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100" leave-to-class="opacity-0">
    <div v-if="show" :class="[configs[type].bg, configs[type].border]"
      class="fixed bottom-5 right-5 z-[100] w-full max-w-sm overflow-hidden rounded-[1.5rem] border backdrop-blur-md shadow-2xl shadow-black/5">
      <div class="p-4">
        <div class="flex items-start gap-4">
          <div :class="[configs[type].bg, 'p-2 rounded-xl shadow-inner']">
            <component :is="configs[type].icon" :class="['w-6 h-6', configs[type].iconColor]" />
          </div>

          <div class="flex-1 pt-0.5">
            <p :class="['text-sm font-black uppercase tracking-widest', configs[type].titleColor]">
              {{ title }}
            </p>
            <p :class="['mt-1 text-xs font-medium leading-relaxed', configs[type].msgColor]">
              {{ message }}
            </p>
          </div>

          <button @click="emit('close')" class="text-gray-400 hover:text-gray-600 transition-colors p-1">
            <XMarkIcon class="w-5 h-5" />
          </button>
        </div>
      </div>

      <div class="h-1 w-full bg-black/5">
        <div :class="[configs[type].iconColor, 'h-full bg-current transition-all duration-300']" style="width: 100%">
        </div>
      </div>
    </div>
  </Transition>
</template>