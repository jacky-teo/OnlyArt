const app = Vue.createApp({
    created() {
        //checks if user has logged in; redirect to login.html if not logged in
        if (!sessionStorage.getItem('CreatorID')) {
            window.location.href = this.loginURL;
        }
    },
    data() {
        return {
            loginURL: "./login.html",

            description: "",

            showDesciptionErr: false,
            showFileErr: false,
            descErrMsg: 'Description is empty.',
            fileErrMsg: 'No file uploaded :(',
        }
    },
    methods: {
        checkForm: function (e) {
            var uploadFile = document.getElementById(file).value;
            console.log(uploadFile);

            if (this.description && uploadFile) {
                this.showDesciptionErr = false;
                this.showFileErr = false;
                return true;
            }

            if (!this.description) {
                this.showDesciptionErr = true;
            } else {
                this.showDesciptionErr = false;
            }

            if (!uploadFile) {
                this.showFileErr = true;
            } else {
                this.showFileErr = false;
            }

            e.preventDefault();
        }
    },

})

app.mount("#app")