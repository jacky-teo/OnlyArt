const app = Vue.createApp({
    data() {
        return {
            isConsumer: false,
            isCreator: false,
            userType: ''
        }
    },
    computed: {

    },
    methods: {
        //update user type when user declares account type
        declareUser(userType) {
            this.userType = userType;
            if (userType == 'creator') {
                this.isCreator = true;
                this.isConsumer = false;

            } else {    
                this.isConsumer = true;
                this.isCreator = false;
            }
        }
    }
})

app.mount('#loginPage')