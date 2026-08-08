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
                "Vocabulary error:",
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

            <h2>
                Loading vocabulary...
            </h2>

        );


    }









    return (

        <div

        style={{

            maxWidth:"900px",

            margin:"0 auto",

            padding:"20px"

        }}

        >



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

                word => (



                <div

                key={word.id}


                style={{

                    border:"1px solid #ddd",

                    borderRadius:"10px",

                    padding:"20px",

                    marginBottom:"20px",

                    background:"#fff"

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


                        <br/>


                        {

                            word.definition ||

                            "-"

                        }


                    </p>







                    <p>

                        <b>
                            Translation:
                        </b>


                        <br/>


                        {

                            word.translation ||

                            "-"

                        }


                    </p>








                    <p>

                        <b>
                            CEFR:
                        </b>


                        {" "}


                        {

                            word.cefr ||

                            "-"

                        }


                    </p>







                    <p>

                        <b>
                            POS:
                        </b>


                        {" "}


                        {

                            word.pos ||

                            "-"

                        }


                    </p>







                </div>


                )


            )

            }





        </div>


    );


}



export default Vocabulary;