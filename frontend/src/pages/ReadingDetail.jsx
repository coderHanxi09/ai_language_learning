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




            if(
                status === "processing"
            ){


                timer = setInterval(
                    async ()=>{


                        const newStatus =
                            await loadReading();



                        if(
                            newStatus !== "processing"
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

                clearInterval(timer);

            }


        };


    },[id]);









    async function handleWordClick(
        word
    ){


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


            console.error(
                error
            );


            setWordInfo(null);


        }


    }









    async function addVocabulary(){


        if(
            !wordInfo?.data
        ){

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


            console.error(
                error
            );


            alert(
                "Failed to add vocabulary"
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







    if(
        data.status === "processing"
    ){


        return (

            <div

            style={{

                padding:"40px"

            }}

            >

                <h1
                style={{
                    lineHeight:"1.5"
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

            padding:"30px"

        }}

        >




            {/* =====================
                Article Area
            ====================== */}


            <div

            style={{

                flex:1,

                minWidth:0

            }}

            >



                <h1

                style={{

                    fontSize:"32px",

                    lineHeight:"1.4",

                    marginBottom:"10px",

                    overflowWrap:
                        "break-word",

                    wordBreak:
                        "break-word"

                }}

                >

                    {data.title}

                </h1>





                <div

                style={{

                    marginBottom:"30px"

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


                        <div

                        key={
                            sentence.id
                        }


                        style={{

                            marginBottom:"35px"

                        }}


                        >



                            <div

                            style={{

                                display:"flex",

                                flexWrap:"wrap",

                                gap:"8px",

                                fontSize:"18px",

                                lineHeight:"1.8"

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

                                        cursor:
                                            "pointer",

                                        padding:
                                            "2px 3px",

                                        borderRadius:
                                            "4px"

                                    }}


                                    >

                                        {
                                            word.word
                                        }


                                    </span>


                                    )

                                )
                            }


                            </div>





                            <p

                            style={{

                                marginTop:"10px",

                                color:"#555",

                                fontSize:"16px",

                                lineHeight:"1.6"

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









            {/* =====================
                Dictionary Sidebar
            ====================== */}


            {
                wordInfo && (

                <div

                style={{

                    width:"320px",

                    flexShrink:0,

                    position:"sticky",

                    top:"20px",

                    height:"fit-content",

                    padding:"20px",

                    border:
                        "1px solid #ddd",

                    borderRadius:"10px",

                    background:"#fff"

                }}

                >



                    <h2>

                        {
                            selectedWord
                        }

                    </h2>



                    {
                        wordInfo.found ?

                        <>


                        <p>
                            Lemma:
                            {" "}
                            {
                                wordInfo.data.lemma
                            }
                        </p>



                        <p>
                            POS:
                            {" "}
                            {
                                wordInfo.data.pos || "-"
                            }
                        </p>



                        <p>
                            CEFR:
                            {" "}
                            {
                                wordInfo.data.cefr || "-"
                            }
                        </p>



                        <p>
                            Definition:
                            {" "}
                            {
                                wordInfo.data.definition || "-"
                            }
                        </p>



                        <p>
                            Translation:
                            {" "}
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



                </div>

                )

            }





        </div>


    );


}


export default ReadingDetail;