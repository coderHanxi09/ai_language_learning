const API_BASE_URL = "http://127.0.0.1:8000";


// =========================
// Create reading
// =========================

export async function createReading(data) {

    const response = await fetch(
        `${API_BASE_URL}/readings`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(data),
        }
    );


    if (!response.ok) {

        throw new Error(
            "Failed to create reading"
        );

    }


    return await response.json();

}



// =========================
// Get reading list
// =========================

export async function getReadings() {


    const response = await fetch(
        `${API_BASE_URL}/readings`
    );


    if (!response.ok) {

        throw new Error(
            "Failed to fetch readings"
        );

    }


    return await response.json();

}



// =========================
// Get single reading
// =========================

export async function getReading(id) {


    const response = await fetch(
        `${API_BASE_URL}/readings/${id}`
    );


    if (!response.ok) {

        throw new Error(
            "Failed to fetch reading"
        );

    }


    return await response.json();

}