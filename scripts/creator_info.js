const app = Vue.createApp({
    data(){
        return {
            postlist:[],
            creatorid:""
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
                    console.log("response: ",response)
                    output = response.data.data;
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
    }
})
const vm = app.mount("#app")