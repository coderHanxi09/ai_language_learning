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


    const [selectedWord,setSelectedWord] = useState("");





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



            if(status==="processing"){


                timer=setInterval(
                    async()=>{


                        const newStatus =
                            await loadReading();



                        if(
                            newStatus !== "processing"
                        ){

                            clearInterval(timer);

                        }


                    },
                    3000
                );

            }


        }


        start();



        return ()=>{


            if(timer){

                clearInterval(timer);

            }

        };


    },[id]);









    async function handleWordClick(word){


        try{


            const cleanWord =
                word
                .replace(
                    /[.,!?;:"'()]/g,
                    ""
                )
                .toLowerCase();



            setSelectedWord(
                cleanWord
            );



            const res =
                await api.get(
                    `/dictionary/${cleanWord}?language=${data.source_language}`
                );



            setWordInfo(
                res.data
            );



        }catch(error){


            console.error(error);


            setWordInfo(null);


        }


    }









    async function addVocabulary(){


        if(!wordInfo?.data){

            return;

        }



        try{


            await api.post(

                "/vocabulary",

                {


                    word:
                        wordInfo.data.word,


                    lemma:
                        wordInfo.data.lemma,


                    definition:
                        wordInfo.data.definition,


                    translation:
                        wordInfo.data.translations?.en || "",


                    cefr:
                        wordInfo.data.cefr,


                    pos:
                        wordInfo.data.pos,


                    source_language:
                        wordInfo.data.language


                }

            );



            alert(
                "Added!"
            );


        }catch(error){


            console.error(error);


            alert(
                "Failed to add vocabulary"
            );


        }


    }









    if(!data){


        return (

            <div style={{
                padding:"40px"
            }}>

                Loading...

            </div>

        );

    }






    if(data.status==="processing"){


        return (

            <div

            style={{

                padding:"40px"

            }}

            >

                <h1

                style={{

                    lineHeight:"1.6",

                    fontSize:"28px"

                }}

                >

                    Generating translation...

                </h1>



                <p>

                    AI is preparing your reading material.

                </p>


            </div>

        );


    }








    return (

        <div

        style={{

            display:"flex",

            gap:"30px",

            maxWidth:"1400px",

            margin:"0 auto",

            padding:"30px",

            alignItems:"flex-start"

        }}

        >




            {/* Article */}


            <main

            style={{

                flex:1,

                minWidth:0,

                overflowWrap:"break-word"

            }}

            >



                <h1

                style={{

                    fontSize:"32px",

                    lineHeight:"1.6",

                    marginBottom:"20px",

                    fontWeight:"700"

                }}

                >

                    {data.title}

                </h1>





                <div

                style={{

                    marginBottom:"30px",

                    color:"#555"

                }}

                >

                    Difficulty:

                    {" "}

                    <b>
                        {data.difficulty}
                    </b>


                </div>







                {
                    data.sentences?.map(

                        sentence=>(


                        <section

                        key={
                            sentence.id
                        }


                        style={{

                            marginBottom:"35px"

                        }}

                        >





                            {/* original sentence */}


                            <div

                            style={{

                                display:"flex",

                                flexWrap:"wrap",

                                gap:"6px",

                                fontSize:"18px",

                                lineHeight:"2",

                                textAlign:"left"

                            }}

                            >



                            {
                                sentence.words?.map(

                                    word=>(


                                    <span


                                    key={
                                        word.id
                                    }



                                    onClick={()=>{

                                        handleWordClick(
                                            word.word
                                        );

                                    }}



                                    style={{

                                        cursor:"pointer",

                                        padding:"3px 5px",

                                        borderRadius:"5px",

                                        background:

                                            selectedWord ===
                                            word.word.toLowerCase()

                                            ?

                                            "#fff3cd"

                                            :

                                            "transparent"

                                    }}


                                    >


                                        {word.word}


                                    </span>


                                    )

                                )

                            }


                            </div>








                            {/* translation */}


                            <p

                            style={{

                                marginTop:"12px",

                                marginBottom:"0",

                                color:"#64748b",

                                fontSize:"16px",

                                lineHeight:"1.8",

                                textAlign:"left"

                            }}

                            >

                                {sentence.translation}


                            </p>





                        </section>


                        )

                    )

                }




            </main>










            {/* Dictionary */}


            {
                wordInfo && (


                <aside

                style={{

                    width:"320px",

                    flexShrink:0,

                    position:"sticky",

                    top:"20px",

                    padding:"20px",

                    border:"1px solid #ddd",

                    borderRadius:"12px",

                    background:"#fff",

                    boxShadow:
                    "0 4px 12px rgba(0,0,0,0.08)"

                }}

                >



                    <h2

                    style={{

                        marginTop:0

                    }}

                    >

                        {selectedWord}

                    </h2>





                    {
                        wordInfo.found ?


                        <>


                        <p>
                            <b>Lemma:</b>{" "}
                            {wordInfo.data.lemma}
                        </p>



                        <p>
                            <b>POS:</b>{" "}
                            {wordInfo.data.pos || "-"}
                        </p>



                        <p>
                            <b>CEFR:</b>{" "}
                            {wordInfo.data.cefr || "-"}
                        </p>



                        <p>
                            <b>Definition:</b>{" "}
                            {wordInfo.data.definition || "-"}
                        </p>



                        <p>
                            <b>Translation:</b>{" "}
                            {
                            wordInfo.data.translations?.en || "-"
                            }
                        </p>



                        <button

                        onClick={
                            addVocabulary
                        }

                        >

                            Add Vocabulary

                        </button>


                        </>


                        :

                        <p>
                            Word not found.
                        </p>

                    }



                </aside>


                )

            }




        </div>

    );


}



export default ReadingDetail;