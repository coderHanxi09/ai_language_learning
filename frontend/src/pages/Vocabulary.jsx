import {
    useEffect,
    useState
} from "react";


import api from "../api/axios";



function Vocabulary(){


    const [words,setWords] = useState([]);




    async function loadVocabulary(){


        try{


            const res = await api.get(
                "/vocabulary"
            );


            console.log(
                "VOCABULARY:",
                res.data
            );


            setWords(
                res.data
            );



        }catch(error){


            console.error(
                error
            );


        }


    }







    useEffect(()=>{


        loadVocabulary();



    },[]);








    return (

        <div>


            <h1>
                My Vocabulary
            </h1>




            {
                words.length === 0 && (

                    <p>
                        No vocabulary yet.
                    </p>

                )
            }






            {
                words.map(
                    word=>(


                    <div

                    key={word.id}

                    style={{

                        border:"1px solid #ccc",

                        padding:"15px",

                        marginBottom:"15px",

                        borderRadius:"8px"

                    }}

                    >



                        <h2>

                            {word.word}

                        </h2>





                        <p>

                            <b>
                                Lemma:
                            </b>

                            {" "}

                            {word.lemma || "-"}

                        </p>





                        <p>

                            <b>
                                Definition:
                            </b>

                            {" "}

                            {word.definition || "-"}

                        </p>






                        <p>

                            <b>
                                Translation:
                            </b>

                            {" "}

                            {word.translation || "-"}

                        </p>






                        <p>

                            <b>
                                CEFR:
                            </b>

                            {" "}

                            {word.cefr || "-"}

                        </p>






                        <p>

                            <b>
                                POS:
                            </b>

                            {" "}

                            {word.pos || "-"}

                        </p>






                        <p>

                            <b>
                                Language:
                            </b>

                            {" "}

                            {word.language || "-"}

                        </p>






                        <p>

                            <b>
                                Status:
                            </b>

                            {" "}

                            {word.status || "-"}

                        </p>




                    </div>


                    )

                )
            }



        </div>

    );


}


export default Vocabulary;