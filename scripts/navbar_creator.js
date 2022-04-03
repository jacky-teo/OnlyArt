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
            if (window.location.href.includes("upload")) {
                return {
                    homeLink: "",
                    viewLink: "./content.html",
                    updateLink:"./update.html"
                }
            }
            else if (window.location.href.includes("content")) {
                return {
                    homeLink: "./upload.html",
                    viewLink: "",
                    updateLink:"./update.html"
                }
            }
            else if (window.location.href.includes("update")) {
                return {
                    homeLink: "./upload.html",
                    viewLink: "./content.html",
                    updateLink:""
                }
            }
            else {
                return {
                    homeLink: "./upload.html",
                    viewLink: "./content.html",
                    updateLink:"./update.html"
                }
            }
        }
    },
    template: `<nav class="px-5 navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="#">OnlyFence</a>
      <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <a class="nav-link" :href=links.homeLink>Upload</a>
          </li>
          <li class="nav-item">
          <a class="nav-link" :href=links.viewLink>View</a>
          </li>
          <li class="nav-item">
          <a class="nav-link" :href=links.updateLink>Edit</a>
          </li>
        </ul>
      </div>
    </nav>`
})
navbar.mount("#compApp")