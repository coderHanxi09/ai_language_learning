import { useState } from "react";
import { useNavigate } from "react-router-dom";


function CreateReading() {


    const [content, setContent] = useState("");

    const navigate = useNavigate();



    async function handleSubmit(){


        if(!content.trim()){

            alert(
                "Please enter text"
            );

            return;

        }



        try{


            const response = await fetch(

                "http://127.0.0.1:8000/readings",

                {

                    method:"POST",

                    headers:{

                        "Content-Type":
                            "application/json"

                    },


                    body:JSON.stringify({

                        title:
                            "Imported Reading",


                        content:
                            content,


                        source_language:
                            "de",


                        translation_language:
                            "en",


                        difficulty:
                            "B2"

                    })

                }

            );



            const data =
                await response.json();



            console.log(
                "Create reading response:",
                data
            );



            const readingId =
                data.id;



            if(!readingId){


                alert(
                    "No reading id returned"
                );


                return;

            }



            navigate(
                `/readings/${readingId}`
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

                rows="10"

                cols="80"

                placeholder="Paste German text here..."

                value={content}

                onChange={
                    e =>
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