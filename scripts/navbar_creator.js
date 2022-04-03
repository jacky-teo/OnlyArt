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
    methods: {
        logout() {
            sessionStorage.setItem('CreatorID', '')
            location.reload();
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
                    <a class="nav-link ms-2" :href=links.homeLink>Upload</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link ms-2" :href=links.viewLink>View</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link ms-2" :href=links.updateLink>Edit</a>
                </li>
                <li class="nav-item">
                <a class="btn btn-outline-light btn-sm mt-1 ms-2" @click="logout()">Logout</a>
                </li>
            </ul>
        </div>
    </nav>`
})
navbar.mount("#compApp")