import {
    useEffect,
    useState
} from "react";


import {
    useParams
} from "react-router-dom";


import api from "../api/axios";





function ReadingDetail(){


    const { id } = useParams();


    const [data,setData] = useState(null);


    const [wordInfo,setWordInfo] = useState(null);


    const [loadingWord,setLoadingWord] = useState(false);









    async function loadReading(){


        try{


            const res = await api.get(
                `/readings/${id}`
            );


            setData(
                res.data
            );


            return res.data.status;


        }catch(error){


            console.error(
                error
            );


        }


    }








    useEffect(()=>{


        let timer;



        async function start(){


            const status =
                await loadReading();



            if(
                status !== "completed"
            ){


                timer=setInterval(

                    async ()=>{


                        const newStatus =
                            await loadReading();



                        if(
                            newStatus === "completed"
                        ){

                            clearInterval(
                                timer
                            );

                        }


                    },

                    3000

                );


            }


        }




        start();




        return ()=>{


            if(timer){

                clearInterval(
                    timer
                );

            }


        };


    },[id]);









    async function handleWordClick(
        word
    ){


        try{


            setLoadingWord(
                true
            );



            const cleanWord =
                word
                .replace(
                    /[.,!?;:"'()]/g,
                    ""
                )
                .trim();



            const res =
                await api.get(

                    `/dictionary/${cleanWord}?language=${data.source_language}`

                );




            if(
                res.data.found
            ){


                setWordInfo(

                    res.data.data

                );


            }else{


                setWordInfo({

                    word:cleanWord,

                    definition:
                    "Word not found"

                });


            }




        }catch(error){


            console.error(
                error
            );


        }finally{


            setLoadingWord(
                false
            );


        }


    }









    async function addVocabulary(){


        if(!wordInfo){

            return;

        }



        try{


            await api.post(

                "/vocabulary",

                {

                    word:
                        wordInfo.word,


                    language:
                        wordInfo.language ||
                        data.source_language

                }

            );



            alert(
                "Added to vocabulary"
            );



        }catch(error){


            console.error(
                error
            );


            alert(
                "Failed"
            );


        }


    }









    if(!data){


        return (

            <h2>
                Loading...
            </h2>

        );

    }









    return (


        <div


        onClick={()=>{


            if(wordInfo){

                setWordInfo(null);

            }


        }}



        style={{

            display:"flex",

            gap:"30px",

            padding:"20px",

            alignItems:"flex-start"

        }}



        >







            {/* ====================
                Article
            ==================== */}



            <div


            onClick={
                e=>e.stopPropagation()
            }



            style={{

                flex:1,

                minWidth:0

            }}


            >



                <h1>

                    {
                        data.title ||
                        "Imported Reading"
                    }

                </h1>




                <p>

                    Difficulty:

                    {" "}

                    {
                        data.difficulty
                    }

                </p>




                <hr/>







                {

                data.sentences?.map(

                    sentence=>(


                    <div


                    key={
                        sentence.id
                    }



                    style={{

                        marginBottom:"25px"

                    }}



                    >



                        <div


                        style={{

                            display:"flex",

                            flexWrap:"wrap",

                            gap:"4px",

                            lineHeight:"1.8",

                            fontSize:"18px"

                        }}



                        >



                        {

                        sentence.words?.map(

                            w=>(


                            <span


                            key={
                                w.id
                            }



                            onClick={

                                e=>{

                                    e.stopPropagation();

                                    handleWordClick(
                                        w.word
                                    );

                                }

                            }



                            style={{

                                cursor:"pointer",

                                padding:"2px 4px",

                                borderRadius:"4px"

                            }}



                            >


                                {w.word}


                            </span>


                            )


                        )

                        }



                        </div>





                        <p

                        style={{

                            color:"#666",

                            marginTop:"8px"

                        }}

                        >

                            {
                                sentence.translation
                            }

                        </p>





                    </div>


                    )


                )

                }





            </div>









            {/* ====================
                Dictionary Panel
            ==================== */}



            <div


            onClick={
                e=>e.stopPropagation()
            }



            style={{

                width:"320px",

                flexShrink:0,

                position:"sticky",

                top:"20px",

                borderLeft:"1px solid #ddd",

                paddingLeft:"20px",

                minHeight:"200px"

            }}



            >




            {

                loadingWord && (

                    <p>
                        Loading dictionary...
                    </p>

                )

            }





            {

            wordInfo && !loadingWord && (


                <div>



                    <h2>

                        {
                            wordInfo.word
                        }

                    </h2>





                    <p>

                        <b>
                        Lemma:
                        </b>


                        {" "}

                        {
                            wordInfo.lemma || "-"
                        }


                    </p>





                    <p>

                        <b>
                        Definition:
                        </b>


                        <br/>


                        {
                            wordInfo.definition ||
                            "-"
                        }


                    </p>





                    <p>

                        <b>
                        Translation:
                        </b>


                        <br/>


                        {

                        wordInfo.translations?.en ||

                        "-"

                        }


                    </p>





                    <p>

                        <b>
                        CEFR:
                        </b>


                        {" "}


                        {
                            wordInfo.cefr || "-"
                        }


                    </p>





                    <p>

                        <b>
                        POS:
                        </b>


                        {" "}


                        {
                            wordInfo.pos || "-"
                        }


                    </p>





                    <button

                    onClick={
                        addVocabulary
                    }

                    >

                        Add to Vocabulary

                    </button>




                </div>


            )


            }



            </div>








        </div>


    );


}



export default ReadingDetail;