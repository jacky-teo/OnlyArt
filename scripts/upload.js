//insert value of CreatorID into hidden form input
document.getElementById('creatorID').value = sessionStorage.getItem('CreatorID');

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
            uploadFile: null,

            showDesciptionErr: false,
            showFileErr: false,
            descErrMsg: 'Description is empty.',
            fileErrMsg: 'No file uploaded :(',
        }
    },
    methods: {
        checkForm: function (e) {
            if (this.description && this.uploadFile) {
                return true;
            }

            if (!this.description) {
                this.showDesciptionErr = true;
            }

            if (!this.uploadFile) {
                this.showFileErr = true;
            }

            e.preventDefault();
        },
        updateFile(event) {
            console.log(event);
        }
    },

})

app.mount("#app")