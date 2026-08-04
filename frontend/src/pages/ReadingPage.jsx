import {
    useState
} from "react";


import {
    createReading,
    getReading
} from "../api/readingApi";



function ReadingPage() {


    const [topic, setTopic] = useState("");

    const [reading, setReading] = useState(null);

    const [loading, setLoading] = useState(false);



    async function handleGenerate() {


        setLoading(true);


        try {


            const result = await createReading({

                topic: topic,

                difficulty: "B2",

                known_vocabulary: []

            });



            console.log(
                "Created:",
                result
            );



            const data = await waitForReading(
                result.id
            );


            setReading(data);



        } catch(error) {


            console.error(error);


        } finally {

            setLoading(false);

        }

    }



    async function waitForReading(id) {


        while(true) {


            const data = await getReading(id);



            console.log(
                data.status
            );



            if(
                data.status === "completed"
                ||
                data.status === "failed"
            ) {

                return data;

            }



            await new Promise(
                resolve =>
                    setTimeout(resolve, 2000)
            );

        }

    }




    return (

        <div>


            <h1>
                AI Reading Generator
            </h1>



            <input

                value={topic}

                onChange={
                    e =>
                    setTopic(e.target.value)
                }

                placeholder="Topic"

            />



            <button

                onClick={handleGenerate}

                disabled={loading}

            >

                {
                    loading
                    ?
                    "Generating..."
                    :
                    "Generate"
                }

            </button>



            {
                reading && (

                    <div>

                        <h2>
                            {reading.title}
                        </h2>


                        <p>
                            {reading.content}
                        </p>

                    </div>

                )
            }


        </div>

    );

}


export default ReadingPage;