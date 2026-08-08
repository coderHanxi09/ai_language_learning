import {
    useEffect,
    useState
} from "react";


import api from "../api/axios";



function Vocabulary(){


    const [words,setWords] = useState([]);


    const [loading,setLoading] = useState(true);




    async function loadVocabulary(){


        try{


            const response =
                await api.get(
                    "/vocabulary"
                );


            setWords(
                response.data
            );


        }catch(error){


            console.error(
                error
            );


        }finally{


            setLoading(false);


        }


    }






    useEffect(()=>{


        loadVocabulary();


    },[]);






    if(loading){


        return (

            <div style={{
                padding:"40px"
            }}>

                Loading vocabulary...

            </div>

        );

    }







    return (

        <div

        style={{

            padding:"40px",

            maxWidth:"1000px",

            margin:"auto"

        }}

        >


            <h1>
                📚 Vocabulary
            </h1>





            {
                words.length === 0

                ?

                <p>
                    No vocabulary yet.
                </p>

                :

                <div>


                {
                    words.map(
                        word=>(

                        <div

                        key={
                            word.id
                        }


                        style={{

                            border:
                            "1px solid #ddd",

                            borderRadius:
                            "12px",

                            padding:
                            "20px",

                            marginBottom:
                            "15px"

                        }}

                        >


                            <h2>
                                {
                                    word.word
                                }
                            </h2>



                            <p>
                                Lemma:
                                {" "}
                                {
                                    word.lemma
                                }
                            </p>



                            {
                                word.translation &&

                                <p>

                                    Translation:
                                    {" "}
                                    {
                                        word.translation
                                    }

                                </p>

                            }



                            {
                                word.definition &&

                                <p>

                                    Definition:
                                    {" "}
                                    {
                                        word.definition
                                    }

                                </p>

                            }



                            {
                                word.cefr &&

                                <p>

                                    CEFR:
                                    {" "}
                                    {
                                        word.cefr
                                    }

                                </p>

                            }


                        </div>


                        )

                    )

                }


                </div>

            }



        </div>

    );


}



export default Vocabulary;