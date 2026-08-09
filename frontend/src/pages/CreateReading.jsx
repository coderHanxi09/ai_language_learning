import {
    useState
} from "react";


import {
    useNavigate
} from "react-router-dom";


import api from "../api/axios";



function CreateReading(){


    const [content,setContent]
        = useState("");



    const navigate = useNavigate();



    const language =

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de";



    const translationLanguage =

        language === "de"

        ?

        "en"

        :

        "de";








    async function handleSubmit(){


        if(!content.trim()){


            alert(
                "Please enter text"
            );


            return;

        }




        try{


            const res = await api.post(

                "/readings",

                {

                    title:null,


                    content:content,


                    source_language:language,


                    translation_language:translationLanguage,


                    difficulty:"B2"

                }

            );





            console.log(

                "CREATE READING:",

                res.data

            );






            navigate(

                `/readings/${res.data.id}`

            );





        }catch(error){


            console.error(
                error
            );


            alert(
                "Failed to create reading"
            );


        }


    }






    return (

        <div>


            <h1>
                Import Reading
            </h1>



            <textarea

                rows="15"

                style={{

                    width:"100%",

                    maxWidth:"900px"

                }}


                placeholder={

                    language === "de"

                    ?

                    "Paste your German article here..."

                    :

                    "Paste your English article here..."

                }


                value={content}


                onChange={

                    e=>

                    setContent(

                        e.target.value

                    )

                }


            />



            <br/>

            <button

                onClick={handleSubmit}

            >

                Start Learning

            </button>



        </div>

    );

}



export default CreateReading;