<template>
  <div class="adminContentHeader">
    <button @click="logout" class="logoutButton">Logout</button>
    <p>Admin Operations</p>
  </div>

  <div class="adminContentBody">
    <!-- Register Admin Form -->
    <form class="adminRegisterForm" @submit.prevent>
      <label for="registerEmail">Email:</label>
      <input type="email" v-model="registerEmail" required />
      <label for="registerPassword">Password:</label>
      <input type="password" v-model="registerPassword" required />
      <button @click="registerAdmin" type="submit">Register Admin</button>
    </form>

    <!-- Change Password Form -->
    <form class="passRegisterForm" @submit.prevent>
      <label for="changePasswordId">Admin ID:</label>
      <input type="text" v-model="changePasswordId" required />
      <label for="changePassword">New Password:</label>
      <input type="password" v-model="changePw" required />
      <button @click="changePassword" type="submit">Change Password</button>
    </form>
    <div>
      <button @click="createCSV" class="logoutButton">Create CSV</button>
    </div>

    <!-- Admin Deletion Form -->
    <div class="dangerZone">
      <h3>Danger Zone</h3>
      <form @submit.prevent>
        <label for="adminToDelete">Select Admin to Delete:</label>
        <select  v-model="adminToDelete" required>
          <option v-for="admin in adminList" :key="admin">
            {{ admin }} 
          </option>
        </select>
        <button @click="deleteAdmin" type="submit">Delete Admin</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      registerEmail: '',
      registerPassword: '',
      changePasswordId: '',
      changePw: '',
      username: '',
      adminToDelete: '',
      // Add more admins as needed
    }
  },
  mounted() {
    this.$store.dispatch('getAdminList')
  },
  methods: {
    registerAdmin() {
      this.$store.dispatch('createAdmin', {
        email: this.registerEmail,
        password: this.registerPassword
      })
    },
    changePassword() {
      this.$store.dispatch('changePassword', {
        email: this.changePasswordId,
        password: this.changePw
      })
    },
    logout() {
      this.$store.dispatch('logout')
    },
    deleteAdmin() {
      console.log("deleteAdmin" + this.adminToDelete);
      this.$store.dispatch('deleteAdmin', this.adminToDelete)
    },
    createCSV() {
      this.$store.dispatch('createCSV')
    },
  },
  computed: {
    adminList() {

      return this.$store.getters.getAdminList
    }
  }
}
</script>
