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
    }
})

app.mount("#app")