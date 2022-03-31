const app = Vue.createApp({
    data() {
        return {
            isConsumer: false,
            isCreator: false,
            userType: '',
            username: '',
            password: '',
            creatorAuthURL: 'http://127.0.0.1:5002/creator/authenticate',
            consumerAuthURL: 'http://127.0.0.1:5001/consumer/authenticate',

            invalidInputs: false,
            inputsMsg: 'Login fields incomplete.',
            isLoginFail: false,
            loginFailMsg: 'Incorrect credentials.',

            consumerRedirect: './creator_gallery.html',
            creatorRedirect: './upload.html',
        }
    },
    computed: {
        validInputs() {
            return this.username && this.password;
            
        }
    },
    created() {
        //checks if user has already logged in; redirect to respective url if logged in before
        if (sessionStorage.getItem('CreatorID')) {
            window.location.href = this.creatorRedirect;
            
        } else if (sessionStorage.getItem('ConsumerID')) {
            window.location.href = this.consumerRedirect;
        }
    },
    methods: {
        //update user type when user declares account type
        declareUser(userType) {
            let prevType = this.userType;
            this.userType = userType;

            if (userType == 'Creator') {
                this.isCreator = true;
                this.isConsumer = false;

                //keeps username and password if userType is the same - in case user accidentally clicks modal away 
                this.username = prevType == userType ? this.username : '';
                this.password = prevType == userType ? this.password : '';

            } else {    
                this.isConsumer = true;
                this.isCreator = false;

                this.username = prevType == userType ? this.username : '';
                this.password = prevType == userType ? this.password : '';
            }
        },
        //authentication 
        login() {
            if (!this.validInputs) {
                //login fields not complete
                this.invalidInputs = true;

            } else {
                this.invalidInputs = false;

                //declare api url depending on user type
                var url = '';
                var redirectURL = '';

                if (this.userType == "Creator") {
                    url = this.creatorAuthURL;
                    redirectURL = this.creatorRedirect;

                } else {
                    url = this.consumerAuthURL;
                    redirectURL = this.consumerRedirect;
                }

                //make call with to authenticate
                axios({
                    method: 'post',
                    url: url,
                    params: {
                        username: this.username,
                        password: this.password
                    }
                })
                .then((resp) => {
                    var data = resp.data;
                    var code = data.code;
                    
                    if (code != 200) {                  //incorrect password
                        this.isLoginFail = true

                    } else {                            //authenticated
                        this.isLoginFail = false;
                        let userInfo = data.data;
                        let userId = this.userType == 'Creator' ? userInfo.creatorID : userInfo.consumerID;
                        console.log(userId);
                        sessionStorage.setItem(this.userType + 'ID', userId);
                        window.location.href = redirectURL;
                        
                    }
                })
                .catch((err) => {
                    console.log(err);

                })
            }
        }
    }
})

app.mount('#loginPage')