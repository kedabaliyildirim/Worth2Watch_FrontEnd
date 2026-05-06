import { ref } from 'vue'

// Single shared search term so the header input and the catalog list
// stay in sync without prop-drilling through the router.
const term = ref('')

export function useGlobalSearch() {
  function setTerm(v) {
    term.value = v
  }
  return { term, setTerm }
}
