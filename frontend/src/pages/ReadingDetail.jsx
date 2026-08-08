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



            if(status !== "completed"){


                timer=setInterval(
                    async ()=>{


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


        start();



        return ()=>{


            if(timer){

                clearInterval(timer);

            }


        };


    },[id]);













    async function handleWordClick(word){


        const cleanWord =
            word
            .replace(/[.,!?;:"'()]/g,"")
            .toLowerCase();



        try{


            setLoadingWord(true);


            const res =
                await api.get(
                    `/dictionary/${cleanWord}?language=${data.source_language}`
                );



            console.log(
                "DICTIONARY:",
                res.data
            );



            if(res.data.found){


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


            setWordInfo(null);



        }finally{


            setLoadingWord(false);


        }



    }









    async function addVocabulary(){



        if(!wordInfo){

            return;

        }





        try{


            const translation =
                wordInfo.translations?.en || "";



            await api.post(

                "/vocabulary",

                {


                    word:
                        wordInfo.word,


                    lemma:
                        wordInfo.lemma,


                    definition:
                        wordInfo.definition,


                    translation,


                    cefr:
                        wordInfo.cefr,


                    pos:
                        wordInfo.pos,


                    language:
                        wordInfo.language || "de"


                }

            );



            alert(
                "Added to vocabulary!"
            );



        }catch(error){


            console.error(
                error
            );


            alert(
                "Failed to add"
            );


        }


    }









    if(!data){


        return <h2>Loading...</h2>;

    }






    return (

        <div>


            <h1>
                {data.title}
            </h1>



            <p>
                Difficulty: {data.difficulty}
            </p>



            <hr/>




            {
                data.sentences?.map(
                    sentence=>(


                    <div

                    key={sentence.id}

                    style={{
                        marginBottom:"30px"
                    }}

                    >



                        <h3>


                        {
                            sentence.words?.map(
                                w=>(


                                <span

                                key={w.id}

                                onClick={()=>{

                                    handleWordClick(
                                        w.word
                                    );

                                }}


                                style={{

                                    cursor:"pointer",

                                    marginRight:"8px"

                                }}

                                >


                                    {w.word}


                                </span>


                                )

                            )

                        }



                        </h3>




                        <p>

                            {sentence.translation}

                        </p>




                    </div>


                    )

                )

            }









            {
                loadingWord && (

                    <div>

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

                        top:"100px",

                        width:"320px",

                        background:"#fff",

                        border:"1px solid #ccc",

                        padding:"20px",

                        boxShadow:"0 0 10px #aaa"

                    }}

                    >



                        <h2>

                            {wordInfo.word}

                        </h2>



                        <p>

                            Lemma:

                            {" "}

                            {wordInfo.lemma || "-"}

                        </p>




                        <p>

                            POS:

                            {" "}

                            {wordInfo.pos || "-"}

                        </p>




                        <p>

                            CEFR:

                            {" "}

                            {wordInfo.cefr || "-"}

                        </p>




                        <p>

                            Definition:

                            {" "}

                            {wordInfo.definition || "-"}

                        </p>




                        <p>

                            Translation:

                            {" "}

                            {wordInfo.translations?.en || "-"}

                        </p>




                        <p>

                            IPA:

                            {" "}

                            {wordInfo.ipa || "-"}

                        </p>




                        {
                            wordInfo.examples?.length > 0 && (

                            <div>

                                <p>
                                    Examples:
                                </p>


                                {
                                    wordInfo.examples.map(
                                        (e,index)=>(

                                        <p key={index}>
                                            {e}
                                        </p>

                                        )
                                    )
                                }


                            </div>

                            )
                        }





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

    );


}


export default ReadingDetail;