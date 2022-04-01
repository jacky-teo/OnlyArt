// vue.js for universal navbar
const app = Vue.createApp({

})

//navbar vue component
app.component('navbar', {
    data() {
        return {
            appName: 'OnlyFence'
        }
    },
    computed: {
        links() {
            // href links at upload directory
            if (window.location.href.includes("creator_gallery")) {
                return {
                    homeLink: "./"
                }
            }
            else {
                return {
                    homeLink: ""
                }
            }
        }
    },
    template: `<nav class="px-5 navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="#">OnlyFences</a>
      <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" :href=links.homeLink>Home</a>
          </li>
        </ul>
      </div>
    </nav>`
})
app.mount("#compApp")