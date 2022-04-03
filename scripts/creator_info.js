const app = Vue.createApp({
    data(){
        return {
            postlist:[],
            creatorid:"",
            loginURL: './login.html',
            subType: ''
        }
    },
    methods:{
        getContent(){
            console.log("getContent running...")
            var url_string = window.location.href; //window.location.href
            var thisurl = new URL(url_string);

            //checks if cid found in url query
            if (thisurl.searchParams.get("cid") != null) {
                var CID = thisurl.searchParams.get("cid");
                this.creatorid = CID;
                console.log("CID: ",CID)            
            } else {
                console.log("CID not found.");
            }

            let output = null;
            var counter = 0;
            //retrieve consumerID from session storage
            var ConsumerID = sessionStorage.getItem('ConsumerID') ? sessionStorage.getItem('ConsumerID') : null;
            console.log("ConID: ", ConsumerID);
            const url = "http://localhost:5100/view_content";
            axios.post(
                url,
                {
                    "CREATORID":CID,
                    "CONSUMERID": ConsumerID
                }
            )
                .then((response) => {
                    console.log("response: ", response)
                    let output = response.data.data;
                    this.subType = response.data.SubType;
                    let urls = response.data.urls; // Get all image URLs

                    for (result of output){
                        listobject = {};
                        listobject['creator'] = result.CREATORID;
                        listobject['desc']= result.DESCRIPTION;
                        listobject['imgurl']=urls[counter] // using this line instead cause ive already stored the imageURLs inside the response
                        listobject['postid']= result.POSTID
                        listobject['postdate']= result.POST_DATE;
                        this.postlist.push(listobject);
                        counter ++
                    }
                    console.log("done");
                    document.getElementById("app").style.display = "block";
                    document.getElementById("loader").style.display = "none";
                },
                (error) => {
                    console.log(error)
                    output = error
                }
                )
        }
    },
    created(){
        this.getContent()

        //checks if user has logged in; redirect to login.html if not logged in
        if (!sessionStorage.getItem('ConsumerID')) {
            window.location.href = this.loginURL;
        }
    },
    computed: {
        unsubcribed() {
            if (this.subType === 1) {   
                return false
                
            } else if (this.subType === 2) {
                return true

            }
        }
    }
})
const vm = app.mount("#app")

// Function for Subscribe Button
async function redirectPayment() {
    console.log("--- JS FUNCTION redirectPayment() ---")
    
    var subscribeURL = "http://localhost:5101/subscribe"
    var data = {
        CREATORID: sessionStorage.getItem('CreatorID')
    }
    var otherParams = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }

    try {
        console.log('LOADING...')
        // Call Subscribe.py to request for payment information
        const response = 
            await fetch(
                subscribeURL, otherParams
            );
        
        const result = await response.json();
            if (response.status === 200) {
                // Success Case
                console.log('SUCCESS CASE')
                console.log(result)

                // Redirect to payment html with payment information
                code = result.code
                creatorUsername = result.creatorUsername
                creatorEmail = result.creatorEmail
                creatorID = result.creatorID
                price = result.price
                
                sessionStorage.setItem('creatorUsername',creatorUsername)
                sessionStorage.setItem('creatorEmail',creatorEmail)
                sessionStorage.setItem('price',price)

                window.location.href = "./payment.html"; 
            } else if (response.status === 404) {
                // Error
                console.log('Error: Response 404')
            } else {
                // Error
                console.log('Error: Response ???')
                throw response.status
            }
    } catch (error) {
        console.log('Error: Error in the service')
    }

}