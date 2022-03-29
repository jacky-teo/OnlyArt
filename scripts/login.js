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
            loginFailMsg: 'Incorrect credentials.'
        }
    },
    computed: {
        validInputs() {
            return this.username && this.password;
            
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
                if (this.userType == "Creator") {
                    url = this.creatorAuthURL;

                } else {
                    url = this.consumerAuthURL;
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
                        console.log('wrong password');

                    } else {                            //authenticated
                        this.isLoginFail = false;
                        let userInfo = data.data;
                        let userId = this.userType == 'Creator' ? userInfo.creatorID : userInfo.consumerID;
                        console.log(userId);
                        
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