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


    const [data, setData] = useState(null);


    const [selectedWord, setSelectedWord] = useState(null);


    const [wordInfo, setWordInfo] = useState(null);





    async function loadReading(){


        try{


            const res = await api.get(
                `/readings/${id}`
            );


            console.log(
                "READING:",
                res.data
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


                timer = setInterval(
                    async ()=>{


                        const newStatus =
                            await loadReading();



                        if(
                            newStatus === "completed"
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


        console.log(
            "CLICK WORD:",
            word
        );



        try{


            const cleanWord =
                word
                .replace(/[.,!?;:"']/g,"")
                .toLowerCase();



            setSelectedWord(
                cleanWord
            );



            const res =
                await api.get(
                    `/dictionary/${cleanWord}`
                );



            console.log(
                "DICTIONARY:",
                res.data
            );



            setWordInfo(
                res.data
            );



        }catch(error){


            console.error(
                "Dictionary error:",
                error
            );


            setWordInfo(null);


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


                    definition:
                        wordInfo.data.definition,


                    cefr:
                        wordInfo.data.cefr

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

            <div>


                <h1>
                    Generating...
                </h1>


                <p>
                    AI is preparing your reading material...
                </p>


            </div>

        );


    }







    return (


        <div>



            <h1>
                {data.title}
            </h1>



            <p>

                Difficulty:

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



                        <h3>



                        {
                            sentence.words ?

                            sentence.words.map(
                                w=>(


                                <span

                                key={
                                    w.id
                                }


                                onClick={()=>{

                                    handleWordClick(
                                        w.word
                                    );

                                }}



                                style={{

                                    cursor:"pointer",

                                    marginRight:"6px"

                                }}


                                >


                                    {w.word}


                                </span>


                                )

                            )

                            :

                            sentence.original


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
                wordInfo?.data && (


                <div


                style={{

                    position:"fixed",

                    right:"20px",

                    top:"100px",

                    width:"300px",

                    padding:"20px",

                    background:"white",

                    border:"1px solid #ccc",

                    boxShadow:"0 0 10px #aaa"

                }}



                >



                    <h2>

                        {
                            wordInfo.data.word
                        }

                    </h2>




                    <p>

                        Lemma:

                        {" "}

                        {
                            wordInfo.data.lemma || "-"
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