import {
    NavLink
} from "react-router-dom";


function Navbar(){


    const linkStyle = ({isActive}) => ({


        textDecoration:"none",


        color:
            isActive
            ? "#2563eb"
            : "#333",


        fontWeight:
            isActive
            ? "700"
            : "500",


        padding:"8px 12px",


        borderRadius:"6px"


    });





    return (


        <nav

        style={{

            display:"flex",

            alignItems:"center",

            justifyContent:"space-between",

            padding:"15px 30px",

            borderBottom:
                "1px solid #ddd",

            background:"#fff",

            position:"sticky",

            top:0,

            zIndex:1000


        }}

        >



            {/* Logo */}

            <div>


                <NavLink

                to="/"

                style={{

                    textDecoration:"none",

                    color:"#111",

                    fontSize:"22px",

                    fontWeight:"700"

                }}

                >

                    AI Language Learning

                </NavLink>


            </div>







            {/* Navigation */}


            <div

            style={{

                display:"flex",

                gap:"10px"

            }}

            >



                <NavLink

                to="/readings"

                style={linkStyle}

                >

                    📖 Readings

                </NavLink>





                <NavLink

                to="/vocabulary"

                style={linkStyle}

                >

                    📝 Vocabulary

                </NavLink>






                <NavLink

                to="/flashcards"

                style={linkStyle}

                >

                    🎴 Flashcards

                </NavLink>







                <NavLink

                to="/writing"

                style={linkStyle}

                >

                    ✨ AI Writing

                </NavLink>





            </div>




        </nav>


    );


}


export default Navbar;