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



    const [isMobile,setIsMobile] = useState(
        window.innerWidth <= 768
    );









    useEffect(()=>{


        function resize(){


            setIsMobile(

                window.innerWidth <= 768

            );


        }



        window.addEventListener(

            "resize",

            resize

        );



        return ()=>{


            window.removeEventListener(

                "resize",

                resize

            );


        };


    },[]);









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


            return null;


        }


    }









    useEffect(()=>{


        loadReading();



        const timer = setInterval(async()=>{


            const status = await loadReading();



            if(

                status === "completed"

                ||

                status === "failed"

            ){

                clearInterval(timer);

            }


        },3000);





        return ()=>{


            clearInterval(timer);


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




            const res = await api.get(

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

                        wordInfo.data.translations?.en

                        ||

                        "",


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

            <div className="loading-page">

                Loading...

            </div>

        );


    }









    if(data.status === "processing"){


        return (

            <div className="loading-page">


                <h1>

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

        className="reading-layout"

        >








            {/* Article */}



            <main

            style={{

                flex:1,

                minWidth:0,

                overflowWrap:"break-word"

            }}

            >




                <h1>

                    {data.title || "Reading"}

                </h1>





                <p>


                    Difficulty:

                    {" "}


                    <b>

                        {data.difficulty}

                    </b>


                </p>









                {


                data.sentences &&

                data.sentences.length > 0



                ?



                data.sentences.map(

                    sentence=>(


                    <section

                    key={sentence.id}


                    style={{

                        marginBottom:"35px"

                    }}

                    >





                        {/* Original */}



                        <div

                        style={{

                            fontSize:

                            isMobile

                            ?

                            "16px"

                            :

                            "18px",


                            lineHeight:"2",


                            display:"flex",


                            flexWrap:"wrap",


                            gap:"6px"


                        }}

                        >





                        {


                        sentence.words &&

                        sentence.words.length > 0



                        ?



                        sentence.words.map(

                            word=>{


                            const normalizedWord =


                                word.word

                                .replace(

                                    /[.,!?;:"'()]/g,

                                    ""

                                )

                                .toLowerCase();




                            return (



                            <span


                            key={word.id}



                            onClick={()=>


                                handleWordClick(

                                    word.word

                                )

                            }



                            style={{


                                cursor:"pointer",


                                padding:"3px 5px",


                                borderRadius:"5px",


                                background:


                                selectedWord === normalizedWord


                                ?


                                "#fff3cd"


                                :


                                "transparent"



                            }}


                            >



                                {word.word}



                            </span>


                            );


                            }


                        )



                        :



                        <span>

                            {sentence.original}

                        </span>



                        }





                        </div>









                        {/* Translation */}



                        <p

                        style={{


                            marginTop:"12px",


                            color:"#64748b",


                            lineHeight:"1.8",


                            fontSize:

                            isMobile

                            ?

                            "14px"

                            :

                            "16px"


                        }}

                        >


                            {


                            sentence.translation


                            ||


                            "Generating translation..."


                            }



                        </p>





                    </section>


                    )


                )



                :



                <p>

                    No sentences available.

                </p>



                }





            </main>









            {/* Dictionary */}



            {


            wordInfo &&



            <aside

            className="dictionary-panel"

            >





                <h2>

                    {selectedWord}

                </h2>






                {


                wordInfo.found



                ?



                <>



                <p>

                    <b>

                        Lemma:

                    </b>


                    {" "}


                    {wordInfo.data.lemma}


                </p>





                <p>

                    <b>

                        POS:

                    </b>


                    {" "}


                    {wordInfo.data.pos}


                </p>





                <p>

                    <b>

                        CEFR:

                    </b>


                    {" "}


                    {wordInfo.data.cefr}


                </p>





                <p>

                    <b>

                        Definition:

                    </b>


                    {" "}


                    {wordInfo.data.definition}


                </p>





                <p>

                    <b>

                        Translation:

                    </b>


                    {" "}


                    {


                    wordInfo.data.translations?.en

                    ||

                    "-"


                    }


                </p>






                <button

                onClick={addVocabulary}

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



            }




        </div>


    );


}



export default ReadingDetail;