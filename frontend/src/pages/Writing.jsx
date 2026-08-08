import {
    useEffect,
    useState
} from "react";


import {
    useNavigate
} from "react-router-dom";


import api from "../api/axios";





function Writing(){


    const navigate = useNavigate();



    const [language,setLanguage] = useState("de");


    const [level,setLevel] = useState("B2");


    const [vocabularyCount,setVocabularyCount] = useState(0);


    const [loading,setLoading] = useState(false);







    async function loadVocabularyCount(){


        try{


            const res = await api.get(
                "/vocabulary"
            );


            setVocabularyCount(
                res.data.length
            );



        }catch(error){


            console.error(
                error
            );


        }


    }







    useEffect(()=>{


        loadVocabularyCount();


    },[]);









    async function generate(){


        try{


            setLoading(true);




            const res = await api.post(

                "/writing/generate",

                {


                    language,


                    level


                }

            );






            if(
                res.data.id
            ){


                navigate(

                    `/readings/${res.data.id}`

                );


            }



        }catch(error){


            console.error(
                error
            );


            alert(
                "Failed to generate article"
            );


            setLoading(false);


        }


    }









    return (


        <div

        style={{

            maxWidth:"800px",

            margin:"40px auto",

            padding:"30px"

        }}

        >



            <h1>

                AI Writing

            </h1>





            <p

            style={{

                color:"#666",

                lineHeight:"1.6"

            }}

            >

                Generate a personalized reading article
                based on your vocabulary.

            </p>








            <div

            style={{

                marginBottom:"30px",

                padding:"15px",

                background:"#f5f5f5",

                borderRadius:"8px"

            }}

            >


                Vocabulary available:

                {" "}

                <b>

                    {vocabularyCount}

                </b>


                <br />


                Words used:

                {" "}

                <b>

                    {Math.min(
                        50,
                        vocabularyCount
                    )}

                </b>


            </div>









            <label>

                Language

            </label>



            <select

            value={language}

            onChange={
                e=>setLanguage(
                    e.target.value
                )
            }


            style={{

                width:"100%",

                padding:"10px",

                margin:"10px 0 20px"

            }}

            >


                <option value="de">

                    German

                </option>


                <option value="en">

                    English

                </option>


            </select>









            <label>

                Level

            </label>



            <select

            value={level}

            onChange={
                e=>setLevel(
                    e.target.value
                )
            }


            style={{

                width:"100%",

                padding:"10px",

                margin:"10px 0 30px"

            }}

            >


                <option value="A2">

                    A2

                </option>


                <option value="B1">

                    B1

                </option>


                <option value="B2">

                    B2

                </option>


                <option value="C1">

                    C1

                </option>


            </select>









            <button


            onClick={generate}


            disabled={loading}


            style={{

                width:"100%",

                padding:"14px",

                fontSize:"16px",

                cursor:

                    loading

                    ?

                    "not-allowed"

                    :

                    "pointer"

            }}

            >


                {

                    loading

                    ?

                    "Generating..."

                    :

                    "Generate Article"

                }


            </button>





        </div>


    );


}



export default Writing;