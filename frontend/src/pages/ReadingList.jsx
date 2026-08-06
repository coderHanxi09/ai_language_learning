import {
    useEffect,
    useState
} from "react";


import {
    Link
} from "react-router-dom";


import api from "../api/axios";



function ReadingList(){


    const [readings,setReadings]
        = useState([]);



    useEffect(()=>{


        api.get("/readings")
            .then(res=>{

                setReadings(
                    res.data
                );

            })


    },[]);



    return (

        <div>


            <h1>
                My Readings
            </h1>


            <Link to="/create">

                Create Reading

            </Link>



            {
                readings.map(
                    r=>(

                    <div key={r.id}>


                        <h3>

                            <Link
                            to={`/readings/${r.id}`}
                            >

                            {r.title}

                            </Link>


                        </h3>


                        <p>

                            {r.status}

                        </p>


                    </div>


                    )
                )
            }


        </div>

    )


}


export default ReadingList;