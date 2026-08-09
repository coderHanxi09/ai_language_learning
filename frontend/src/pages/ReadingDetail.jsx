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



    const [language,setLanguage] = useState(

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de"

    );








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



            if(status === "completed"){

                clearInterval(timer);

            }


            if(status === "failed"){

                clearInterval(timer);

            }


        },3000);





        return ()=>{


            clearInterval(timer);


        };


    },[id]);









    useEffect(()=>{


        function handleLanguageChange(){


            setLanguage(

                localStorage.getItem(
                    "learningLanguage"
                )
                ||
                "de"

            );


        }




        window.addEventListener(

            "languageChange",

            handleLanguageChange

        );



        return ()=>{


            window.removeEventListener(

                "languageChange",

                handleLanguageChange

            );


        };


    },[]);









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
                "Added!"
            );


        }catch(error){


            console.error(error);


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









    if(data.status === "processing"){


        return (

            <div

            style={{

                padding:"40px"

            }}

            >


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

        style={{

            display:"flex",

            gap:"30px",

            maxWidth:"1400px",

            margin:"0 auto",

            padding:"30px"

        }}

        >




            <main

            style={{

                flex:1

            }}

            >




                <h1>

                    {data.title}

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

                            fontSize:"18px",

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

                            word=>(


                            <span

                            key={word.id}


                            onClick={()=>handleWordClick(

                                word.word

                            )}


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

                            lineHeight:"1.8"

                        }}

                        >


                            {sentence.translation ||

                            "Generating translation..."}


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









            {
                wordInfo &&


                <aside

                style={{

                    width:"320px",

                    padding:"20px",

                    border:"1px solid #ddd",

                    borderRadius:"12px"

                }}

                >



                    <h2>

                        {selectedWord}

                    </h2>





                    {

                    wordInfo.found


                    ?

                    <>

                    <p>

                    <b>Lemma:</b>

                    {" "}

                    {wordInfo.data.lemma}

                    </p>



                    <p>

                    <b>POS:</b>

                    {" "}

                    {wordInfo.data.pos}

                    </p>



                    <p>

                    <b>CEFR:</b>

                    {" "}

                    {wordInfo.data.cefr}

                    </p>



                    <p>

                    <b>Definition:</b>

                    {" "}

                    {wordInfo.data.definition}

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