<template>
  <div class="adminMainBody">
    <!-- Sidebar -->
    <div class="adminSideBar">
      <ul>
        <li @click="changeContent('admin')">Admin Operations</li>
        <li @click="changeContent('content')">Content Operations</li>
        <li @click="changeContent('tests')">Test Operations</li>
      </ul>
    </div>

    <!-- Main Content -->
    <div class="adminContent">
      <div class="adminContentHeader">
        <h1>Admin Dashboard</h1>
      </div>
      <div class="adminContentBody">
        <div class="adminContentBodyHeader">
          <h2>{{ selectedContent.title }}</h2>
        </div>
        <div class="adminContentBodyMain">
          <component :is="selectedContent.component"></component>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AdminOperations from '@/components/adminComponents/AdminOperations.vue'; // Import your components
import ContentOperations from '@/components/adminComponents/ContentOperations.vue';
import Tests from '@/components/adminComponents/TestOperations.vue';
import ProjectOptions from '@/components/adminComponents/ProjectOperations.vue';

export default {
  data() {
    return {
      selectedContent: {
        title: 'Admin Operations',
        component: AdminOperations,
      },
    };
  },
  methods: {
    changeContent(type) {
      switch (type) {
        case 'admin':
          this.selectedContent = {
            title: 'Admin Content Body',
            component: AdminOperations,
          };
          break;
        case 'content':
          this.selectedContent = {
            title: 'Content Operations',
            component: ContentOperations,
          };
          break;
        case 'tests':
          this.selectedContent = {
            title: 'Tests',
            component: Tests,
          };
          break;
        case 'project':
          this.selectedContent = {
            title: 'Project Options',
            component: ProjectOptions,
          };
          break;
        default:
          break;
      }
    },
  },
};
</script>