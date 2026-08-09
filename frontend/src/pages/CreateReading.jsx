import {
    useState,
    useEffect
} from "react";


import {
    useNavigate
} from "react-router-dom";


import api from "../api/axios";





function CreateReading(){


    const [content,setContent] = useState("");


    const [loading,setLoading] = useState(false);



    const [language,setLanguage] = useState(

        localStorage.getItem(
            "learningLanguage"
        )
        ||
        "de"

    );



    const navigate = useNavigate();







    const translationLanguage =

        language === "de"

        ?

        "en"

        :

        "de";









    // =========================
    // Sync Navbar language change
    // =========================


    useEffect(()=>{


        function updateLanguage(){


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

            updateLanguage

        );






        return ()=>{


            window.removeEventListener(

                "languageChange",

                updateLanguage

            );


        };



    },[]);









    async function handleSubmit(){



        if(!content.trim()){


            alert(

                "Please enter text"

            );


            return;


        }







        try{


            setLoading(true);





            const res = await api.post(

                "/readings",

                {


                    title:null,


                    content:content,


                    source_language:language,


                    translation_language:

                        translationLanguage,


                    difficulty:"B2"


                }

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



        }finally{


            setLoading(false);


        }


    }









    return (


        <div

        className="create-reading-page"

        >





            <h1>

                Import Reading

            </h1>






            <p

            className="subtitle"

            >


                {


                language === "de"

                ?

                "Paste a German article and start learning."

                :

                "Paste an English article and start learning."



                }


            </p>









            <textarea


            className="reading-input"



            rows="15"



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








            <button


            className="start-button"



            onClick={handleSubmit}



            disabled={loading}



            >



                {


                loading

                ?

                "Creating..."

                :

                "Start Learning"



                }



            </button>






        </div>


    );


}



export default CreateReading;