// vue.js for universal navbar
const navbar = Vue.createApp({

})

//navbar vue component
navbar.component('navbar', {
  data() {
    return {
      appName: 'OnlyFence'
    }
  },
  computed: {
    links() {
      // href links at consumer
      if (window.location.href.includes("creator_gallery")) {
        return {
          homeLink: ""
        }
      }
      else{
        return {
            homeLink: "creator_gallery.html",
        }
    }
    }
  },
  template: `<nav class="px-5 navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="#">OnlyFence</a>
      <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <a class="nav-link" :href=links.homeLink>Home</a>
          </li>
        </ul>
      </div>
    </nav>`
})
navbar.mount("#compApp")