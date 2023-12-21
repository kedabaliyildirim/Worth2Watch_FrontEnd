<template>
  <div class="mainAdmin">
    <form v-if="!loginState" class="loginForm" @submit.prevent="login">
      <!-- <input type="hidden" name="_token" :value="csrf"> -->
      <label for="email">Email:</label>
      <input type="email" id="email" v-model="email" required />
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required />
      <button type="submit" login>Login</button>
    </form>
    <adminComponent v-if="loginState">
    </adminComponent> 
  </div>
</template>

<script>
import adminComponent from "@/components/AdminComponent.vue";
export default {
  components: {
    adminComponent
  },
  name: 'AdminView',
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    async login() {
      const payload = {
        email: this.email,
        password: this.password
      }
      this.$store.dispatch('login', payload)
    }
  },
  computed: {
    loginState() {
      return this.$store.getters.getLoginState
    },
    csrfState() {
      this.$store.getters.getCsrftoken
      return this.$store.getters.getCsrftoken
    }
  }
}
</script>

<style>
.loginForm {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
button {
  margin: 15px;
  border-radius: 5%;
}
</style>
