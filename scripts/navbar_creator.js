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
            else if (window.location.href.includes("upload")) {
                return {
                    // href links at creator (upload.html)
                    homeLink: "",
                    viewLink: "./content.html"
                }
            }
            else if (window.location.href.includes("content")) {
                return {
                    // href links at creator (content.html)
                    homeLink: "",
                    uploadLink: "./upload.html"
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
          <li class="nav-item">
          <a class="nav-link" :href=links.uploadLink>Upload</a>
          </li>
          <li class="nav-item ">
            <a class="nav-link" :href=links.viewLink>Content</a>
          </li>
        </ul>
      </div>
    </nav>`
})
navbar.mount("#compApp")