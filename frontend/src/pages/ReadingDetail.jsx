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



    const [currentSentence,setCurrentSentence] = useState(0);









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


            console.error(error);


            return null;

        }


    }









    useEffect(()=>{


        loadReading();



        const timer = setInterval(async()=>{


            const status =
                await loadReading();



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

                "Added to vocabulary"

            );



        }catch(error){


            console.error(error);



        }


    }









    if(!data){


        return (

            <div className="loading-page">

                Loading...

            </div>

        );

    }









    if(data.status==="processing"){


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









    const sentences =

        data.sentences || [];




    const sentence =

        sentences[currentSentence];









    if(!sentence){


        return (

            <div className="loading-page">

                No sentence available.

            </div>

        );


    }









    const progress =

        Math.round(

            (

                (currentSentence + 1)

                /

                sentences.length

            )

            *

            100

        );









    return (



        <div className="learning-reading-page">







            <h1>

                {data.title}

            </h1>





            <p className="subtitle">


                {data.difficulty}

                {" · "}

                Sentence

                {" "}

                {currentSentence + 1}

                /

                {sentences.length}


            </p>









            {/* Progress */}



            <div className="progress-container">


                <div

                className="progress-bar"


                style={{

                    width:`${progress}%`

                }}

                >

                </div>


            </div>









            {/* Sentence Card */}



            <div className="sentence-card">







                <div className="sentence-original">


                {


                sentence.words &&

                sentence.words.length > 0



                ?



                sentence.words.map(

                    word=>(


                    <span


                    key={word.id}


                    onClick={()=>handleWordClick(

                        word.word

                    )}



                    className={

                        selectedWord ===

                        word.word.toLowerCase()

                        ?

                        "word selected"

                        :

                        "word"

                    }



                    >

                        {word.word}


                    </span>


                    )


                )



                :


                sentence.original



                }



                </div>









                <div className="sentence-translation">


                    {


                    sentence.translation

                    ||

                    "Generating translation..."


                    }


                </div>






            </div>









            {/* Navigation */}



            <div className="sentence-navigation">



                <button


                disabled={currentSentence===0}



                onClick={()=>


                    setCurrentSentence(

                        currentSentence-1

                    )


                }


                >

                    ← Previous

                </button>






                <button


                disabled={

                    currentSentence ===

                    sentences.length-1

                }



                onClick={()=>


                    setCurrentSentence(

                        currentSentence+1

                    )


                }


                >

                    Next →

                </button>





            </div>









            {/* Word popup */}



            {


            wordInfo &&



            <div className="word-popup">



                <button

                className="close-popup"

                onClick={()=>setWordInfo(null)}

                >

                    ×

                </button>






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

                    {wordInfo.data.definition}

                </p>





                <p>

                    {

                    wordInfo.data.translations?.en

                    ||

                    "-"

                    }

                </p>






                <button

                onClick={addVocabulary}

                >

                    + Add Vocabulary

                </button>



                </>





                :



                <p>

                    Word not found.

                </p>



                }




            </div>


            }



        </div>


    );


}



export default ReadingDetail;