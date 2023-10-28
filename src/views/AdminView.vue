<template>
  <div class="mainAdmin">
    <form class="loginForm" @submit.prevent="login">
      {% csrf_token %}
      <label for="email">Email:</label>
      <input type="email" id="email" v-model="email" required />
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required />
      <button type="submit" login>Login</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'AdminView',
  data() {
    return {
      email: '',
      password: ''
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
      return this.$store.getters.getLoginStete
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
