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


    const [loading,setLoading] = useState(false);






    async function loadReading(){


        try{


            const res = await api.get(
                `/readings/${id}`
            );


            console.log(
                "READING DATA:",
                res.data
            );


            setData(
                res.data
            );


            return res.data.status;



        }catch(error){


            console.error(
                "Load reading error:",
                error
            );


            return null;

        }


    }








    useEffect(()=>{


        let timer;



        async function init(){


            const status =
                await loadReading();



            if(
                status !== "completed"
            ){


                timer=setInterval(
                    async()=>{


                        const newStatus =
                            await loadReading();



                        if(
                            newStatus==="completed"
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



        init();



        return ()=>{


            if(timer){

                clearInterval(
                    timer
                );

            }

        };


    },[id]);









    async function handleWordClick(word){


        console.log(
            "CLICK WORD:",
            word
        );



        setLoading(true);



        try{


            const cleanWord =
                word
                .replace(
                    /[.,!?;:"']/g,
                    ""
                )
                .toLowerCase();



            console.log(
                "LOOKUP WORD:",
                cleanWord
            );



            const res =
                await api.get(
                    `/dictionary/${cleanWord}?language=de`
                );



            console.log(
                "DICTIONARY RESPONSE:",
                res.data
            );



            if(
                res.data.found
            ){

                setWordInfo(
                    res.data
                );

            }
            else{


                setWordInfo({

                    found:false,

                    data:{
                        word:cleanWord
                    }

                });


            }




        }catch(error){


            console.error(
                "Dictionary lookup failed:",
                error
            );


            setWordInfo(null);


        }
        finally{


            setLoading(false);


        }


    }









    async function addVocabulary(){



        if(
            !wordInfo ||
            !wordInfo.data
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


                    cefr:
                        wordInfo.data.cefr,


                    definition:
                        wordInfo.data.definition,


                    source_language:
                        "de"

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









    return (

        <div
        style={{
            padding:"20px"
        }}
        >



            <h1>
                {data.title}
            </h1>




            <p>

                Level:

                {" "}

                {data.difficulty}

            </p>



            <hr/>







            {
                data.sentences &&
                data.sentences.map(
                    sentence=>(


                    <div

                    key={
                        sentence.id
                    }


                    style={{

                        marginBottom:"30px"

                    }}

                    >





                        <div>


                        {


                        sentence.words.map(

                            word=>(


                            <span

                            key={
                                word.id
                            }


                            onClick={()=>{

                                /*
                                  Important:
                                  use lemma for dictionary
                                */

                                handleWordClick(
                                    word.lemma
                                );


                            }}


                            style={{

                                cursor:"pointer",

                                marginRight:"8px",

                                color:"#0066cc"

                            }}


                            >


                                {word.word}


                            </span>


                            )

                        )


                        }


                        </div>






                        <p>

                            <b>
                            Translation:
                            </b>

                            {" "}

                            {sentence.translation}

                        </p>





                    </div>


                    )

                )

            }









            {
                loading && (

                    <div

                    style={{

                        position:"fixed",

                        right:"20px",

                        top:"80px",

                        background:"#eee",

                        padding:"15px"

                    }}

                    >

                        Loading dictionary...

                    </div>

                )
            }









            {
                wordInfo && (


                <div

                style={{

                    position:"fixed",

                    right:"20px",

                    top:"120px",

                    width:"320px",

                    background:"white",

                    border:"1px solid #ccc",

                    padding:"20px",

                    boxShadow:
                    "0 0 10px rgba(0,0,0,0.2)"

                }}

                >



                    {


                    wordInfo.found ?


                    <>


                    <h2>

                        {
                            wordInfo.data.word
                        }

                    </h2>



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
                        wordInfo.data.pos
                    }

                    </p>





                    <p>

                    CEFR:

                    {" "}

                    {
                        wordInfo.data.cefr
                    }

                    </p>





                    <p>

                    IPA:

                    {" "}

                    {
                        wordInfo.data.ipa
                    }

                    </p>





                    <p>

                    Translation:

                    {" "}

                    {
                        wordInfo.data.translations?.en
                    }

                    </p>




                    <p>

                    Examples:

                    </p>



                    {

                    wordInfo.data.examples?.map(

                        (e,index)=>(

                            <p key={index}>
                                {e}
                            </p>

                        )

                    )

                    }





                    <button

                    onClick={
                        addVocabulary
                    }

                    >

                        Add Vocabulary

                    </button>


                    </>


                    :


                    <>

                    <h3>

                    {wordInfo.data.word}

                    </h3>


                    <p>
                    Word not found.
                    </p>

                    </>


                    }



                </div>


                )

            }





        </div>


    );

}



export default ReadingDetail;