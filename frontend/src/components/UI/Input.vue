<script setup>
defineProps({
  inputType: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'email', 'password', 'number', 'phone', 'date'].includes(value)
  },
  inputId: {
    type: String,
    required: true
  },
  label: String,
  placeholder: String,
  inputClass: String,
  modelValue: {
    type: [String, Number],
    default: ''
  },
  error: String,
  required: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  },
  divClass: String
})

const emit = defineEmits(['update:modelValue'])

const handleInput = (e) => {
  emit('update:modelValue', e.target.value)
}
</script>

<template>
  <div :class="['flex flex-col gap-2', divClass]">
    <label :for="inputId" class="text-gray-500 font-medium text-lg">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <input 
      :id="inputId" 
      :type="inputType" 
      :placeholder="placeholder"
      :value="modelValue"
      :disabled="disabled"
      :class="[
        'px-4 py-3 border-2 rounded focus:outline-0 transition',
        error ? 'border-red-500' : 'border-black/25',
        disabled ? 'bg-gray-100 cursor-not-allowed' : '',
        inputClass
      ]"
      @input="handleInput"
    >
    
    <span v-if="error" class="text-red-500 text-sm">{{ error }}</span>
  </div>
</template>
